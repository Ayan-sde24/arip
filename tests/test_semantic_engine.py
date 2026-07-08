"""Minimal unit tests for the Semantic Intelligence Engine."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.semantic_engine.semantic_engine import (
    SemanticEngine,
    SemanticEngineError,
)
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Education, Experience, Resume


def _doc(name: str = "file.pdf") -> Document:
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
    )


def _resume(
    skills: list[str] | None = None,
    experience: list[Experience] | None = None,
    education: list[Education] | None = None,
) -> Resume:
    return Resume(
        document=_doc("resume.pdf"),
        candidate=Candidate(
            candidate_id=uuid4(),
            name="Jane Doe",
            email="jane@example.com",
            phone="555-0000",
        ),
        skills=skills or [],
        experience=experience or [],
        education=education or [],
    )


def _job(
    required_skills: list[str] | None = None,
    preferred_skills: list[str] | None = None,
    keywords: list[str] | None = None,
    education_required: str | None = None,
    experience_required: str | None = None,
) -> JobDescription:
    return JobDescription(
        document=_doc("jd.pdf"),
        title="Senior Python Engineer",
        company="Acme Corp",
        required_skills=required_skills or ["Python", "FastAPI", "PostgreSQL"],
        preferred_skills=preferred_skills or ["Docker", "Kubernetes"],
        keywords=keywords or ["python", "fastapi", "postgresql"],
        education_required=education_required,
        experience_required=experience_required,
        responsibilities=["Build APIs", "Write tests"],
    )


# ── Happy path ────────────────────────────────────────────────────────────────


def test_happy_path_partial_match() -> None:
    resume = _resume(
        skills=["Python", "FastAPI"],
        experience=[
            Experience(
                company="Corp A",
                role="Python Developer",
                start_date="2020",
                end_date="2023",
                skills=["Python", "FastAPI"],
            )
        ],
        education=[
            Education(
                institution="MIT",
                degree="Bachelor of Science",
                major="Computer Science",
            )
        ],
    )
    job = _job(
        education_required="Bachelor in Computer Science", experience_required="3 years"
    )
    engine = SemanticEngine()
    report = engine.analyse(resume, job)

    assert 0.0 <= report.overall_score <= 100.0
    assert "Python" in report.matched_skills
    assert "FastAPI" in report.matched_skills
    assert "PostgreSQL" in report.missing_skills
    assert len(report.evidence) == 4
    assert any(e.component == "Skills" for e in report.evidence)
    assert any(e.component == "Education" for e in report.evidence)


# ── No matching skills ────────────────────────────────────────────────────────


def test_no_matching_skills() -> None:
    resume = _resume(skills=["Java", "Spring"])
    job = _job(required_skills=["Python", "FastAPI", "PostgreSQL"])
    report = SemanticEngine().analyse(resume, job)

    assert report.skill_score < 20.0
    assert report.required_skill_coverage == 0.0
    assert set(report.missing_skills) == {"Python", "FastAPI", "PostgreSQL"}
    assert "Skills" in report.gap_summary.weak_areas


# ── Perfect match ─────────────────────────────────────────────────────────────


def test_perfect_skill_match() -> None:
    skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes"]
    resume = _resume(
        skills=skills,
        experience=[
            Experience(
                company="Corp B",
                role="Senior Python Engineer",
                start_date="2018",
                end_date="2024",
                skills=skills,
            )
        ],
        education=[
            Education(institution="IIT", degree="Master of Science", major="CS")
        ],
    )
    job = _job(
        experience_required="5 years",
        education_required="Bachelor",
    )
    report = SemanticEngine().analyse(resume, job)

    assert report.required_skill_coverage == 100.0
    assert report.preferred_skill_coverage == 100.0
    assert report.missing_skills == []
    assert report.overall_score > 80.0


# ── Missing education ─────────────────────────────────────────────────────────


def test_missing_education() -> None:
    resume = _resume(
        skills=["Python", "FastAPI", "PostgreSQL"],
        education=[],
    )
    job = _job(education_required="PhD in Computer Science")
    report = SemanticEngine().analyse(resume, job)

    assert report.education_score < 80.0
    edu_evidence = next(e for e in report.evidence if e.component == "Education")
    assert "not met" in edu_evidence.reason.lower()
    assert (
        "Education" in report.gap_summary.missing_education
        or report.education_score < 100.0
    )


# ── Engine rejects null inputs ────────────────────────────────────────────────


def test_engine_rejects_null_resume() -> None:
    with pytest.raises(SemanticEngineError, match="Resume cannot be null"):
        SemanticEngine().analyse(None, _job())  # type: ignore[arg-type]


def test_engine_rejects_null_job() -> None:
    with pytest.raises(SemanticEngineError, match="JobDescription cannot be null"):
        SemanticEngine().analyse(_resume(), None)  # type: ignore[arg-type]
