"""Minimal unit tests for the Resume Coach Agent."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.resume_coach.llm_provider import MockLLMProvider
from app.application.resume_coach.resume_coach_agent import (
    ResumeCoachAgent,
    ResumeCoachAgentError,
)
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Education, Experience, Resume
from app.domain.entities.resume_optimization_report import (
    ResumeOptimizationReport,
)
from app.domain.entities.semantic_match_report import GapSummary, SemanticMatchReport


def _doc(name: str = "file.pdf", metadata: dict | None = None) -> Document:
    doc_id = uuid4()
    now = datetime.now(UTC)
    return Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename=name,
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="x",
        size=512,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
        metadata=metadata or {},
    )


def _cand() -> Candidate:
    return Candidate(
        candidate_id=uuid4(),
        name="Jane Doe",
        email="jane@example.com",
        phone="555-0000",
        location="New York, NY",
    )


def _job() -> JobDescription:
    return JobDescription(
        document=_doc("job.pdf"),
        title="Developer",
        company="Big Tech",
        required_skills=["Python", "Docker"],
        preferred_skills=["AWS"],
        keywords=["python", "docker"],
    )


def _sem_report(overall: float = 80.0, req_cov: float = 80.0) -> SemanticMatchReport:
    return SemanticMatchReport(
        overall_score=overall,
        skill_score=80.0,
        experience_score=80.0,
        education_score=80.0,
        keyword_score=80.0,
        matched_skills=["Python"],
        missing_skills=["Docker"],
        extra_skills=[],
        matched_preferred_skills=[],
        required_skill_coverage=req_cov,
        preferred_skill_coverage=0.0,
        matched_keywords=["python"],
        missing_keywords=["docker"],
        keyword_coverage=80.0,
        gap_summary=GapSummary(),
        evidence=[],
    )


def _ats_report(overall: float = 80.0) -> ATSReport:
    return ATSReport(
        overall_ats_score=overall,
        keyword_score=80.0,
        format_score=overall,
        section_score=80.0,
        completeness_score=80.0,
        resume_parseability="High",
        ats_shortlisting_probability="High",
        strengths=[],
        weaknesses=[],
        missing_keywords=[],
        recommendations=["Add missing Docker required skill."],
    )


def _rec_report(overall: float = 80.0, exp: float = 80.0) -> RecruiterReport:
    return RecruiterReport(
        overall_recruiter_score=overall,
        project_score=80.0,
        experience_score=exp,
        presentation_score=80.0,
        leadership_score=80.0,
        communication_score=80.0,
        shortlist_probability="High",
        recruiter_verdict="Buy",
        reasons=[],
        recommendations=["Add experience bullet details."],
        strengths=[],
        weaknesses=[],
        key_concerns=[],
        standout_factors=[],
        improvement_suggestions=[],
    )


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_resume_coach_basic_optimization() -> None:
    resume = Resume(
        document=_doc("res.pdf", {"summary": "Experienced programmer."}),
        candidate=_cand(),
        skills=["Python"],
        experience=[
            Experience(
                company="Corp A",
                role="Dev",
                start_date="2022",
                end_date="2023",
                description=["Wrote python APIs."],
            )
        ],
        education=[],
    )

    llm = MockLLMProvider(
        response_map={
            "optimize this summary": "Optimized Senior Software Engineer summary.",
            "popular certifications": "AWS Certified Developer, Certified Kubernetes",
        }
    )
    agent = ResumeCoachAgent(llm=llm)
    report = agent.optimize(resume, _job(), _sem_report(), _ats_report(), _rec_report())

    assert isinstance(report, ResumeOptimizationReport)
    assert report.optimization_score == 80.0
    assert "Senior Software Engineer" in report.optimized_resume.summary
    assert len(report.priority_fixes) > 0


def test_resume_coach_no_improvements_needed() -> None:
    # A perfect scoring candidate
    resume = Resume(
        document=_doc("res.pdf", {"summary": "Expert programmer."}),
        candidate=_cand(),
        skills=["Python", "Docker"],
        experience=[
            Experience(
                company="Corp A",
                role="Senior Dev",
                start_date="2020",
                end_date="2026",
                description=["Led dev work"],
            )
        ],
        education=[Education(institution="IIT", degree="MS", major="CS")],
    )

    agent = ResumeCoachAgent()
    # High overall scores (100)
    report = agent.optimize(
        resume,
        _job(),
        _sem_report(overall=100.0, req_cov=100.0),
        _ats_report(overall=100.0),
        _rec_report(overall=100.0),
    )

    assert report.optimization_score == 100.0
    assert len(report.critical_issues) == 0


def test_resume_coach_weak_resume() -> None:
    # Lacks sections, experience, and has low reports
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=None,
        skills=[],
        experience=[],
        education=[],
    )

    agent = ResumeCoachAgent()
    report = agent.optimize(
        resume,
        _job(),
        _sem_report(overall=30.0, req_cov=10.0),
        _ats_report(overall=40.0),
        _rec_report(overall=35.0, exp=0.0),
    )

    assert report.optimization_score < 50.0
    assert any("Low ATS" in issue for issue in report.critical_issues)
    assert any("lack of professional" in issue for issue in report.critical_issues)


def test_resume_coach_strong_resume() -> None:
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=_cand(),
        skills=["Python", "Docker"],
        experience=[
            Experience(
                company="Corp A",
                role="Dev",
                start_date="2020",
                end_date="2024",
                description=["Built backend"],
            )
        ],
    )

    agent = ResumeCoachAgent()
    report = agent.optimize(
        resume,
        _job(),
        _sem_report(overall=90.0),
        _ats_report(overall=92.0),
        _rec_report(overall=91.0),
    )

    assert report.optimization_score >= 90.0
    assert len(report.critical_issues) == 0


# ── Error cases ──


def test_resume_coach_rejects_null_inputs() -> None:
    agent = ResumeCoachAgent()
    res = Resume(document=_doc("res.pdf"))
    job = _job()
    sem = _sem_report()
    ats = _ats_report()
    rec = _rec_report()

    with pytest.raises(ResumeCoachAgentError, match="Resume cannot be null"):
        agent.optimize(None, job, sem, ats, rec)  # type: ignore[arg-type]

    with pytest.raises(ResumeCoachAgentError, match="JobDescription cannot be null"):
        agent.optimize(res, None, sem, ats, rec)  # type: ignore[arg-type]

    with pytest.raises(
        ResumeCoachAgentError, match="SemanticMatchReport cannot be null"
    ):
        agent.optimize(res, job, None, ats, rec)  # type: ignore[arg-type]

    with pytest.raises(ResumeCoachAgentError, match="ATSReport cannot be null"):
        agent.optimize(res, job, sem, None, rec)  # type: ignore[arg-type]

    with pytest.raises(ResumeCoachAgentError, match="RecruiterReport cannot be null"):
        agent.optimize(res, job, sem, ats, None)  # type: ignore[arg-type]
