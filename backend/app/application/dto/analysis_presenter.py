"""Presenter class mapping AnalysisResult entities into frontend-friendly DTOs."""

from app.application.dto.analysis_response import AnalysisResponseDTO
from app.application.dto.chart_response import ChartResponseDTO
from app.application.dto.recommendation_response import RecommendationResponseDTO
from app.application.dto.score_response import ScoreResponseDTO
from app.application.dto.summary_response import SummaryResponseDTO
from app.application.orchestrator.analysis_result import AnalysisResult


class AnalysisPresenter:
    """Presenter converting pipeline AnalysisResult to serializable REST DTOs."""

    def present(self, result: AnalysisResult) -> AnalysisResponseDTO:
        """Map domain AnalysisResult to frontend DTO structures.

        Handles missing fields and null parameters gracefully (e.g. for failed
        pipeline stages).
        """
        if result is None:
            return AnalysisResponseDTO(
                summary=None,
                scores=None,
                recommendations=None,
                charts=None,
                status="failed",
                errors=["Analysis result is null."],
            )

        # ── 1. Map SummaryResponseDTO ─────────────────────────────────────────
        cand_name = "N/A"
        if result.resume and result.resume.candidate:
            cand_name = result.resume.candidate.name or "N/A"

        overall_match = 0.0
        if result.semantic_report:
            overall_match = result.semantic_report.overall_score

        ats_score = 0.0
        if result.ats_report:
            ats_score = result.ats_report.overall_ats_score

        recruiter_score = 0.0
        if result.recruiter_report:
            recruiter_score = result.recruiter_report.overall_recruiter_score

        semantic_score = 0.0
        if result.semantic_report:
            semantic_score = result.semantic_report.overall_score

        opt_score = 0.0
        if result.optimization_report:
            opt_score = result.optimization_report.optimization_score

        verdict = "Pass"
        if result.recruiter_report:
            verdict = result.recruiter_report.recruiter_verdict

        summary_dto = SummaryResponseDTO(
            candidate_name=cand_name,
            overall_match=overall_match,
            ats_score=ats_score,
            recruiter_score=recruiter_score,
            semantic_score=semantic_score,
            optimization_score=opt_score,
            overall_recommendation=verdict,
        )

        # ── 2. Map ScoreResponseDTO ───────────────────────────────────────────
        res_quality = 0.0
        if result.ats_report:
            res_quality = result.ats_report.format_score

        overall_score = 0.0
        if result.optimization_report:
            overall_score = result.optimization_report.optimization_score
        else:
            overall_score = round(
                (ats_score + recruiter_score + semantic_score) / 3.0, 2
            )

        score_dto = ScoreResponseDTO(
            ats=ats_score,
            semantic=semantic_score,
            recruiter=recruiter_score,
            resume_quality=res_quality,
            overall=overall_score,
        )

        # ── 3. Map RecommendationResponseDTO ──────────────────────────────────
        strengths: list[str] = []
        weaknesses: list[str] = []
        critical_improvements: list[str] = []
        suggested_skills: list[str] = []
        missing_keywords: list[str] = []
        career_suggestions: list[str] = []

        if result.recruiter_report:
            strengths = result.recruiter_report.strengths
            weaknesses = result.recruiter_report.weaknesses
            career_suggestions = result.recruiter_report.recommendations

        if result.optimization_report:
            critical_improvements = result.optimization_report.critical_issues
            opt_res = result.optimization_report.optimized_resume
            if opt_res:
                suggested_skills = opt_res.suggested_skills

        if result.semantic_report:
            missing_keywords = result.semantic_report.missing_keywords

        rec_dto = RecommendationResponseDTO(
            strengths=strengths,
            weaknesses=weaknesses,
            critical_improvements=critical_improvements,
            suggested_skills=suggested_skills,
            missing_keywords=missing_keywords,
            career_suggestions=career_suggestions,
        )

        # ── 4. Map ChartResponseDTO ───────────────────────────────────────────
        # Skill Coverage chart data
        matched_s_count = 0
        missing_s_count = 0
        if result.semantic_report:
            matched_s_count = len(result.semantic_report.matched_skills)
            missing_s_count = len(result.semantic_report.missing_skills)

        skill_coverage_chart = {
            "labels": ["Matched Skills", "Missing Skills"],
            "datasets": [{"data": [matched_s_count, missing_s_count]}],
        }

        # Score Breakdown chart data
        score_breakdown_chart = {
            "labels": ["ATS Score", "Semantic Match", "Recruiter Score"],
            "datasets": [{"data": [ats_score, semantic_score, recruiter_score]}],
        }

        # Experience Comparison chart data
        candidate_years = 0.0
        required_years = 0.0
        if result.resume and result.resume.experience:
            candidate_years = len(result.resume.experience) * 1.5  # approximation
        if result.job_description:
            # We can extract or mock experience duration required
            required_years = 5.0

        experience_comparison_chart = {
            "labels": ["Candidate", "Required"],
            "datasets": [{"data": [candidate_years, required_years]}],
        }

        # Education Comparison chart data
        candidate_edu_tier = "Bachelors"
        required_edu_tier = "Bachelors"
        if result.resume and result.resume.education:
            candidate_edu_tier = result.resume.education[0].degree or "Bachelors"

        education_comparison_chart = {
            "candidate_tier": candidate_edu_tier,
            "required_tier": required_edu_tier,
        }

        # Gap Analysis chart data
        gap_analysis_chart = {
            "missing_skills_count": missing_s_count,
            "critical_fixes_count": len(critical_improvements),
            "recommendations_count": len(career_suggestions),
        }

        chart_dto = ChartResponseDTO(
            skill_coverage=skill_coverage_chart,
            score_breakdown=score_breakdown_chart,
            experience_comparison=experience_comparison_chart,
            education_comparison=education_comparison_chart,
            gap_analysis=gap_analysis_chart,
        )

        return AnalysisResponseDTO(
            summary=summary_dto,
            scores=score_dto,
            recommendations=rec_dto,
            charts=chart_dto,
            status=result.status,
            errors=result.errors,
            warnings=result.warnings,
        )
