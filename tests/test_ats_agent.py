"""Minimal unit tests for the ATS Intelligence Agent."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.ats_agent.ats_agent import ATSAgent, ATSAgentError
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.job_description import JobDescription
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
        name="John Doe",
        email="john@example.com",
        phone="555-1234",
        location="New York, NY",
        linkedin="linkedin.com/in/johndoe",
    )


def _job() -> JobDescription:
    return JobDescription(
        document=_doc("job.pdf"),
        title="Software Engineer",
        company="Tech Corp",
        required_skills=["Python", "FastAPI", "Docker"],
        preferred_skills=["AWS", "Kubernetes"],
        keywords=["python", "fastapi", "docker", "aws"],
    )


def _report(
    req_cov: float = 60.0,
    pref_cov: float = 50.0,
    missing: list[str] | None = None,
) -> SemanticMatchReport:
    return SemanticMatchReport(
        overall_score=75.0,
        skill_score=80.0,
        experience_score=70.0,
        education_score=80.0,
        keyword_score=65.0,
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Docker"],
        extra_skills=[],
        matched_preferred_skills=["AWS"],
        required_skill_coverage=req_cov,
        preferred_skill_coverage=pref_cov,
        matched_keywords=["python", "fastapi"],
        missing_keywords=missing or ["docker", "kubernetes"],
        keyword_coverage=req_cov,
        gap_summary=GapSummary(),
        evidence=[],
    )


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_ats_agent_happy_path() -> None:
    resume = Resume(
        document=_doc("res.pdf", {"has_summary": True}),
        candidate=_cand(),
        skills=["Python", "FastAPI", "Docker", "Git", "SQL"],
        experience=[
            Experience(
                company="Corp A",
                role="Engineer",
                start_date="2022",
                end_date="Present",
                description=[
                    "Built backend APIs with FastAPI",
                    "Containerized with Docker",
                ],
                skills=["Python", "FastAPI", "Docker"],
            )
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
                title="API Service",
                description="FastAPI service description",
                skills=["Python"],
            )
        ],
    )
    job = _job()
    report = _report()

    agent = ATSAgent()
    ats_report = agent.evaluate(resume, job, report)

    assert isinstance(ats_report, ATSReport)
    assert ats_report.overall_ats_score > 50.0
    assert ats_report.resume_parseability in ["High", "Medium", "Low"]
    assert ats_report.ats_shortlisting_probability in ["High", "Medium", "Low"]


def test_ats_agent_perfect_resume() -> None:
    # A perfect resume has all sections, logical ordering metadata,
    # good contact details, and multiple projects/experience entries.
    resume = Resume(
        document=_doc(
            "res.pdf",
            {
                "has_summary": True,
                "sections": [
                    {"section_type": "contact", "title": "Contact Info"},
                    {"section_type": "summary", "title": "Summary"},
                    {"section_type": "experience", "title": "Experience"},
                    {"section_type": "education", "title": "Education"},
                    {"section_type": "skills", "title": "Skills"},
                    {"section_type": "projects", "title": "Projects"},
                ],
            },
        ),
        candidate=_cand(),
        skills=[
            "Python",
            "FastAPI",
            "Docker",
            "AWS",
            "Kubernetes",
            "Git",
            "SQL",
            "CI/CD",
        ],
        experience=[
            Experience(
                company="Corp A",
                role="Software Engineer",
                start_date="2020",
                end_date="2022",
                description=[
                    (
                        "Detailed engineering work to design, develop and "
                        "test high-volume applications."
                    ),
                    (
                        "Collaborate with multi-functional teams to define, "
                        "execute and ship software features."
                    ),
                    (
                        "Responsible for writing unit tests, maintaining code "
                        "quality and refactoring legacy systems."
                    ),
                    (
                        "Implement backend API services using FastAPI and "
                        "clean database architecture patterns."
                    ),
                    (
                        "Optimize database queries and structure to handle "
                        "large-scale concurrent requests effectively."
                    ),
                ],
                skills=["Python", "FastAPI"],
            ),
            Experience(
                company="Corp B",
                role="Senior Engineer",
                start_date="2022",
                end_date="2024",
                description=[
                    (
                        "Led a talented team of developers to design and "
                        "build cloud native API microservices."
                    ),
                    (
                        "Implemented infrastructure deployments using Docker "
                        "containers and cloud infrastructure on AWS."
                    ),
                    (
                        "Participated in agile ceremonies, mentored junior "
                        "developers and conducted code reviews."
                    ),
                    (
                        "Monitored application performance metrics and "
                        "debugged production issues promptly."
                    ),
                    (
                        "Designed system integration components and oversaw "
                        "security compliance guidelines."
                    ),
                ],
                skills=["Python", "AWS", "Docker"],
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
                title="API Engine",
                description="FastAPI microservice for order processing.",
            ),
            Project(
                title="Deployment Orchestrator",
                description="Kubernetes tooling for cloud setups.",
            ),
        ],
    )
    job = _job()
    report = _report(req_cov=100.0, pref_cov=100.0, missing=[])

    agent = ATSAgent()
    ats_report = agent.evaluate(resume, job, report)

    assert ats_report.overall_ats_score >= 85.0
    assert ats_report.resume_parseability == "High"
    assert ats_report.ats_shortlisting_probability == "High"
    assert len(ats_report.weaknesses) == 0 or "keyword stuffing" not in "".join(
        ats_report.weaknesses
    )


def test_ats_agent_poor_resume() -> None:
    # A poor resume lacks a candidate profile/contact, education list,
    # projects, skills, etc.
    resume = Resume(
        document=_doc("res.pdf"),
        candidate=None,
        skills=[],
        experience=[],
        education=[],
        projects=[],
    )
    job = _job()
    report = _report(req_cov=0.0, pref_cov=0.0)

    agent = ATSAgent()
    ats_report = agent.evaluate(resume, job, report)

    assert ats_report.overall_ats_score < 40.0
    assert ats_report.resume_parseability == "Low"
    assert ats_report.ats_shortlisting_probability == "Low"
    assert len(ats_report.weaknesses) > 2


def test_ats_agent_missing_skills() -> None:
    resume = Resume(
        document=_doc("res.pdf", {"has_summary": True}),
        candidate=_cand(),
        skills=[],  # empty
        experience=[
            Experience(
                company="Corp A",
                role="Developer",
                start_date="2022",
                end_date="2023",
                description=["no skills match"],
            )
        ],
        education=[Education(institution="IIT", degree="MS", major="CS")],
    )
    job = _job()
    # 0 coverage
    report = _report(
        req_cov=0.0, pref_cov=0.0, missing=["python", "fastapi", "docker", "aws"]
    )

    ats_report = ATSAgent().evaluate(resume, job, report)
    assert ats_report.keyword_score < 20.0
    assert "Skills section is empty" in "".join(ats_report.weaknesses)


def test_ats_agent_missing_sections() -> None:
    # Missing education & projects sections
    resume = Resume(
        document=_doc("res.pdf", {"has_summary": True}),
        candidate=_cand(),
        skills=["Python"],
        experience=[
            Experience(
                company="Corp A",
                role="Dev",
                start_date="2020",
                end_date="2021",
                description=["Some developer stuff"],
            )
        ],
        education=[],  # Missing
        projects=[],  # Missing
    )
    job = _job()
    report = _report()

    ats_report = ATSAgent().evaluate(resume, job, report)
    assert ats_report.section_score < 70.0
    assert "Missing Education section" in "".join(ats_report.weaknesses)


# ── Error cases ───────────────────────────────────────────────────────────────


def test_ats_agent_rejects_null_inputs() -> None:
    agent = ATSAgent()
    with pytest.raises(ATSAgentError, match="Resume cannot be null"):
        agent.evaluate(None, _job(), _report())  # type: ignore[arg-type]

    with pytest.raises(ATSAgentError, match="JobDescription cannot be null"):
        agent.evaluate(_resume_mock(), None, _report())  # type: ignore[arg-type]

    with pytest.raises(ATSAgentError, match="SemanticMatchReport cannot be null"):
        agent.evaluate(_resume_mock(), _job(), None)  # type: ignore[arg-type]


def _resume_mock() -> Resume:
    return Resume(document=_doc("res.pdf"))
