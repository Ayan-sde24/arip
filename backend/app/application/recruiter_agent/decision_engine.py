"""Decision engine aggregating recruiter evaluations and recommendations."""

from typing import Any

from app.application.recruiter_agent.communication_evaluator import (
    CommunicationEvaluator,
)
from app.application.recruiter_agent.experience_evaluator import (
    ExperienceEvaluator,
)
from app.application.recruiter_agent.leadership_evaluator import (
    LeadershipEvaluator,
)
from app.application.recruiter_agent.presentation_evaluator import (
    PresentationEvaluator,
)
from app.application.recruiter_agent.project_evaluator import ProjectEvaluator
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class DecisionEngine:
    """Combines individual recruiter evaluators to formulate a recruiting report."""

    def __init__(
        self,
        project_eval: ProjectEvaluator | None = None,
        exp_eval: ExperienceEvaluator | None = None,
        pres_eval: PresentationEvaluator | None = None,
        lead_eval: LeadershipEvaluator | None = None,
        comm_eval: CommunicationEvaluator | None = None,
    ) -> None:
        self.project_eval = project_eval or ProjectEvaluator()
        self.exp_eval = exp_eval or ExperienceEvaluator()
        self.pres_eval = pres_eval or PresentationEvaluator()
        self.lead_eval = lead_eval or LeadershipEvaluator()
        self.comm_eval = comm_eval or CommunicationEvaluator()

    def process(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
        ats_report: ATSReport,
    ) -> dict[str, Any]:
        """Aggregate evaluations and render shortlist recommendation verdict."""
        proj_res = self.project_eval.evaluate(resume, job, semantic_report, ats_report)
        exp_res = self.exp_eval.evaluate(resume, job, semantic_report, ats_report)
        pres_res = self.pres_eval.evaluate(resume, job, semantic_report, ats_report)
        lead_res = self.lead_eval.evaluate(resume, job, semantic_report, ats_report)
        comm_res = self.comm_eval.evaluate(resume, job, semantic_report, ats_report)

        proj_score = proj_res["score"]
        exp_score = exp_res["score"]
        pres_score = pres_res["score"]
        lead_score = lead_res["score"]
        comm_score = comm_res["score"]

        # Recruiter Overall Score Weights:
        # Experience: 30%, Projects: 25%, Presentation: 15%, Leadership: 15%, Comm: 15%
        overall_score = round(
            exp_score * 0.30
            + proj_score * 0.25
            + pres_score * 0.15
            + lead_score * 0.15
            + comm_score * 0.15,
            2,
        )

        # shortlisting verdict logic
        if overall_score >= 85.0:
            verdict = "Strong Buy"
            prob = "High"
        elif overall_score >= 70.0:
            verdict = "Buy"
            prob = "High"
        elif overall_score >= 50.0:
            verdict = "Hold"
            prob = "Medium"
        else:
            verdict = "Pass"
            prob = "Low"

        # Confidence score computation based on data density
        # Drops if there is no experience, education or candidate name
        confidence = 95.0
        if not resume.experience:
            confidence -= 30.0
        if not resume.education:
            confidence -= 20.0
        if not resume.candidate:
            confidence -= 15.0
        confidence = max(30.0, confidence)

        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[str] = []

        results = [proj_res, exp_res, pres_res, lead_res, comm_res]
        for r in results:
            strengths.extend(r.get("strengths", []))
            weaknesses.extend(r.get("weaknesses", []))
            recommendations.extend(r.get("recommendations", []))

        strengths = list(dict.fromkeys(strengths))
        weaknesses = list(dict.fromkeys(weaknesses))
        recommendations = list(dict.fromkeys(recommendations))

        # Key concerns are subset of weaknesses pertaining to critical work areas
        key_concerns = [
            w
            for w in weaknesses
            if "missing" in w.lower() or "no " in w.lower() or "short " in w.lower()
        ]
        # Standout factors are high value strengths
        standout_factors = [
            s
            for s in strengths
            if "excellent" in s.lower() or "strong" in s.lower() or "clear" in s.lower()
        ]

        return {
            "overall_score": overall_score,
            "project_score": proj_score,
            "experience_score": exp_score,
            "presentation_score": pres_score,
            "leadership_score": lead_score,
            "communication_score": comm_score,
            "shortlist_probability": prob,
            "recruiter_verdict": verdict,
            "confidence_score": confidence,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "key_concerns": key_concerns,
            "standout_factors": standout_factors,
            "recommendations": recommendations,
        }
