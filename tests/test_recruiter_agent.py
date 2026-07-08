"""Minimal unit tests for the Recruiter Intelligence Agent."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.recruiter_agent.recruiter_agent import (
    RecruiterAgent,
    RecruiterAgentError,
)
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Education, Experience, Project, Resume
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
        location="San Francisco, CA",
        github="github.com/janedoe",
    )


def _job() -> JobDescription:
    return JobDescription(
        document=_doc("job.pdf"),
        title="Senior Developer",
        company="Global Tech",
        required_skills=["Python", "SQL", "Docker"],
        preferred_skills=["AWS"],
        keywords=["python", "sql", "docker", "aws"],
    )


def _sem_report() -> SemanticMatchReport:
    return SemanticMatchReport(
        overall_score=85.0,
        skill_score=90.0,
        experience_score=80.0,
        education_score=90.0,
        keyword_score=80.0,
        matched_skills=["Python", "SQL"],
        missing_skills=["Docker"],
        extra_skills=[],
        matched_preferred_skills=[],
        required_skill_coverage=80.0,
        preferred_skill_coverage=0.0,
        matched_keywords=["python", "sql"],
        missing_keywords=["docker"],
        keyword_coverage=80.0,
        gap_summary=GapSummary(),
        evidence=[],
    )


def _ats_report(format_score: float = 90.0, section_score: float = 90.0) -> ATSReport:
    return ATSReport(
        overall_ats_score=85.0,
        keyword_score=80.0,
        format_score=format_score,
        section_score=section_score,
        completeness_score=90.0,
        resume_parseability="High",
        ats_shortlisting_probability="High",
        strengths=[],
        weaknesses=[],
        missing_keywords=[],
        recommendations=[],
    )


# ── Evaluator tests ───────────────────────────────────────────────────────────


def test_recruiter_agent_strong_resume() -> None:
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=_cand(),
        skills=["Python", "SQL", "Docker", "AWS"],
        experience=[
            Experience(
                company="Startup Inc",
                role="Senior Developer",
                start_date="2022",
                end_date="2026",
                description=[
                    (
                        "Led a team of engineers to build API services "
                        "saving $100k in hosting costs."
                    ),
                    (
                        "Designed microservices using Python and Docker, "
                        "resulting in 30ms latency reduction."
                    ),
                    (
                        "Mentored junior developers, and conducted tech talks "
                        "on database optimization."
                    ),
                ],
                skills=["Python", "SQL", "Docker"],
            ),
            Experience(
                company="Corp B",
                role="Developer",
                start_date="2020",
                end_date="2022",
                description=[
                    "Developed application features using Python.",
                    "Improved query speeds by 20% in PostgreSQL database.",
                ],
                skills=["Python", "SQL"],
            ),
        ],
        education=[
            Education(
                institution="State Univ",
                degree="Bachelor of Science",
                major="Computer Science",
            )
        ],
        projects=[
            Project(
                title="Database Wrapper",
                description=(
                    "Created an open-source Python wrapper with "
                    "GitHub integration links."
                ),
                url="github.com/janedoe/db",
                skills=["Python", "SQL"],
            )
        ],
    )

    agent = RecruiterAgent()
    report = agent.evaluate(resume, _job(), _sem_report(), _ats_report())

    assert isinstance(report, RecruiterReport)
    assert report.overall_recruiter_score >= 80.0
    assert report.recruiter_verdict in ["Strong Buy", "Buy"]
    assert report.shortlist_probability == "High"
    assert len(report.strengths) > 0


def test_recruiter_agent_weak_resume() -> None:
    # Lacks content, details, metrics, only base structures
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=None,
        skills=[],
        experience=[
            Experience(
                company="Corp A",
                role="Dev",
                start_date="2022",
                end_date="2023",
                description=["Worked on projects"],
            )
        ],
        education=[],
        projects=[],
    )

    agent = RecruiterAgent()
    report = agent.evaluate(resume, _job(), _sem_report(), _ats_report())

    assert report.overall_recruiter_score < 60.0
    assert report.recruiter_verdict in ["Hold", "Pass"]


def test_recruiter_agent_excellent_projects() -> None:
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=_cand(),
        skills=["Python"],
        experience=[
            Experience(
                company="Corp A",
                role="Dev",
                start_date="2022",
                end_date="2023",
                description=["Worked here"],
            )
        ],
        education=[],
        projects=[
            Project(
                title="Project Alpha",
                description="Built high-performance engine improving speed by 50%.",
                url="github.com/janedoe/alpha",
                skills=["Python", "Docker", "AWS"],
            ),
            Project(
                title="Project Beta",
                description="Designed open source database tool with 200 stars.",
                url="github.com/janedoe/beta",
                skills=["Python", "SQL"],
            ),
        ],
    )

    agent = RecruiterAgent()
    report = agent.evaluate(resume, _job(), _sem_report(), _ats_report())
    assert report.project_score >= 85.0


def test_recruiter_agent_poor_presentation() -> None:
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=_cand(),
        skills=["Python"],
        experience=[
            Experience(
                company="Corp A",
                role="Dev",
                start_date="2022",
                end_date="2023",
                description=["Worked here"],
            )
        ],
        education=[],
        projects=[],
    )

    agent = RecruiterAgent()
    # Bad format and section scores
    report = agent.evaluate(
        resume,
        _job(),
        _sem_report(),
        _ats_report(format_score=40.0, section_score=40.0),
    )
    assert report.presentation_score < 70.0


def test_recruiter_agent_missing_experience() -> None:
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=_cand(),
        skills=["Python"],
        experience=[],  # Missing
        education=[],
        projects=[],
    )

    agent = RecruiterAgent()
    report = agent.evaluate(resume, _job(), _sem_report(), _ats_report())
    assert report.experience_score == 0.0
    assert report.recruiter_verdict == "Pass"


# ── Error propagation ──


def test_recruiter_agent_rejects_null_inputs() -> None:
    agent = RecruiterAgent()
    res = Resume(document=_doc("res.pdf"))
    job = _job()
    sem = _sem_report()
    ats = _ats_report()

    with pytest.raises(RecruiterAgentError, match="Resume cannot be null"):
        agent.evaluate(None, job, sem, ats)  # type: ignore[arg-type]

    with pytest.raises(RecruiterAgentError, match="JobDescription cannot be null"):
        agent.evaluate(res, None, sem, ats)  # type: ignore[arg-type]

    with pytest.raises(RecruiterAgentError, match="SemanticMatchReport cannot be null"):
        agent.evaluate(res, job, None, ats)  # type: ignore[arg-type]

    with pytest.raises(RecruiterAgentError, match="ATSReport cannot be null"):
        agent.evaluate(res, job, sem, None)  # type: ignore[arg-type]
