"""Unit tests for the Analysis Presentation layer and DTO mapping."""

from app.application.dto.analysis_presenter import AnalysisPresenter
from app.application.dto.analysis_response import AnalysisResponseDTO
from app.application.orchestrator.analysis_result import AnalysisResult
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.candidate import Candidate
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.resume_optimization_report import (
    OptimizedResume,
    ResumeOptimizationReport,
)
from app.domain.entities.semantic_match_report import SemanticMatchReport


def test_presentation_dto_mapping() -> None:
    # Set up mock entities
    resume = Resume(
        document=None,  # type: ignore[arg-type]
        candidate=Candidate(
            candidate_id=None,  # type: ignore[arg-type]
            name="Alice Smith",
            email="alice@example.com",
            phone="123",
        ),
    )
    job = JobDescription(document=None, title="SDE", company="Startup")  # type: ignore[arg-type]

    semantic = SemanticMatchReport(
        overall_score=85.0,
        skill_score=80.0,
        experience_score=80.0,
        education_score=80.0,
        keyword_score=80.0,
        matched_skills=["Python"],
        missing_skills=["Docker"],
        extra_skills=[],
        matched_preferred_skills=[],
        required_skill_coverage=80.0,
        preferred_skill_coverage=0.0,
        matched_keywords=["python"],
        missing_keywords=["docker"],
        keyword_coverage=80.0,
        gap_summary=None,  # type: ignore[arg-type]
        evidence=[],
    )

    ats = ATSReport(
        overall_ats_score=90.0,
        keyword_score=80.0,
        format_score=95.0,
        section_score=90.0,
        completeness_score=90.0,
        resume_parseability="High",
        ats_shortlisting_probability="High",
    )

    recruiter = RecruiterReport(
        overall_recruiter_score=75.0,
        project_score=80.0,
        experience_score=80.0,
        presentation_score=80.0,
        leadership_score=80.0,
        communication_score=80.0,
        shortlist_probability="High",
        recruiter_verdict="Buy",
        strengths=["Good formatting"],
        weaknesses=["Missing projects"],
        recommendations=["Add personal projects"],
    )

    coach = ResumeOptimizationReport(
        optimization_score=82.0,
        critical_issues=["No projects"],
        optimized_resume=OptimizedResume(
            summary="Optimized summary",
            suggested_skills=["Kubernetes"],
        ),
    )

    result = AnalysisResult(
        resume=resume,
        job_description=job,
        semantic_report=semantic,
        ats_report=ats,
        recruiter_report=recruiter,
        optimization_report=coach,
        execution_time=1.2,
        status="success",
    )

    presenter = AnalysisPresenter()
    dto = presenter.present(result)

    assert isinstance(dto, AnalysisResponseDTO)
    assert dto.status == "success"
    assert dto.summary is not None
    assert dto.summary.candidate_name == "Alice Smith"
    assert dto.summary.overall_match == 85.0
    assert dto.summary.ats_score == 90.0
    assert dto.summary.recruiter_score == 75.0
    assert dto.summary.optimization_score == 82.0
    assert dto.summary.overall_recommendation == "Buy"

    assert dto.scores is not None
    assert dto.scores.ats == 90.0
    assert dto.scores.semantic == 85.0
    assert dto.scores.recruiter == 75.0
    assert dto.scores.resume_quality == 95.0
    assert dto.scores.overall == 82.0

    assert dto.recommendations is not None
    assert "Good formatting" in dto.recommendations.strengths
    assert "Missing projects" in dto.recommendations.weaknesses
    assert "No projects" in dto.recommendations.critical_improvements
    assert "Kubernetes" in dto.recommendations.suggested_skills
    assert "docker" in dto.recommendations.missing_keywords
    assert "Add personal projects" in dto.recommendations.career_suggestions

    assert dto.charts is not None
    assert dto.charts.skill_coverage["datasets"][0]["data"] == [1, 1]
    assert dto.charts.score_breakdown["datasets"][0]["data"] == [90.0, 85.0, 75.0]


def test_presentation_missing_fields_and_null_results() -> None:
    # Test completely null result mapping
    presenter = AnalysisPresenter()
    dto_null = presenter.present(None)  # type: ignore[arg-type]

    assert dto_null.status == "failed"
    assert dto_null.summary is None
    assert dto_null.scores is None
    assert len(dto_null.errors) == 1

    # Test partial / missing fields
    partial_result = AnalysisResult(
        resume=None,
        job_description=None,
        semantic_report=None,
        ats_report=None,
        recruiter_report=None,
        optimization_report=None,
        execution_time=0.1,
        status="failed",
        errors=["Early pipeline error"],
    )

    dto_partial = presenter.present(partial_result)

    assert dto_partial.status == "failed"
    assert len(dto_partial.errors) == 1
    assert dto_partial.summary is not None
    assert dto_partial.summary.candidate_name == "N/A"
    assert dto_partial.summary.overall_match == 0.0
    assert dto_partial.summary.ats_score == 0.0
    assert dto_partial.summary.recruiter_score == 0.0

    assert dto_partial.scores is not None
    assert dto_partial.scores.ats == 0.0
    assert dto_partial.scores.overall == 0.0

    assert dto_partial.recommendations is not None
    assert len(dto_partial.recommendations.strengths) == 0

    assert dto_partial.charts is not None
    assert dto_partial.charts.skill_coverage["datasets"][0]["data"] == [0, 0]
