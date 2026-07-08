"""Minimal unit tests for the Job Description Builder."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.job_builder.job_builder import JobBuilder
from app.application.job_builder.job_integration import (
    JobIntegration,
    JobPipelineError,
)
from app.application.job_builder.job_validator import JobValidationError
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection
from app.domain.entities.page import Page
from app.domain.entities.section_type import SectionType
from app.domain.entities.text_block import TextBlock


def _make_doc() -> Document:
    doc_id = uuid4()
    now = datetime.now(UTC)
    return Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="jd.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abc123",
        size=512,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )


def _make_section(
    section_type: SectionType, title: str, content: str
) -> DocumentSection:
    return DocumentSection(
        id=uuid4(),
        section_type=section_type,
        title=title,
        content=content,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )


def _make_cir(sections: list[DocumentSection]) -> CanonicalIntermediateRepresentation:
    doc = _make_doc()
    full_text = "\n\n".join(s.content for s in sections)
    page = Page(
        page_number=1,
        text_blocks=[
            TextBlock(text=s.content, page=1, block_index=i, reading_order=i)
            for i, s in enumerate(sections)
        ],
    )
    content = DocumentContent(
        document=doc,
        pages=[page],
        raw_text=full_text,
        clean_text=full_text,
    )
    stats = CIRStatistics(
        total_pages=1,
        total_sections=len(sections),
        total_text_blocks=len(sections),
        total_characters=len(full_text),
        total_words=len(full_text.split()),
        detected_languages=["en"],
        average_section_length=len(full_text) / max(len(sections), 1),
    )
    return CanonicalIntermediateRepresentation(
        document=doc,
        document_content=content,
        sections=sections,
        statistics=stats,
        pipeline_version="1.0",
    )


def _full_jd_cir() -> CanonicalIntermediateRepresentation:
    return _make_cir(
        [
            _make_section(SectionType.JOB_TITLE, "Job Title", "Senior Python Engineer"),
            _make_section(SectionType.COMPANY, "Company", "Acme Corp"),
            _make_section(SectionType.LOCATION, "Location", "Remote"),
            _make_section(SectionType.EMPLOYMENT_TYPE, "Employment Type", "Full-time"),
            _make_section(
                SectionType.EXPERIENCE_REQUIRED,
                "Experience Required",
                "5+ years",
            ),
            _make_section(
                SectionType.EDUCATION_REQUIRED,
                "Education Required",
                "Bachelor's in Computer Science",
            ),
            _make_section(
                SectionType.REQUIRED_SKILLS,
                "Required Skills",
                "Python, FastAPI, PostgreSQL",
            ),
            _make_section(
                SectionType.PREFERRED_SKILLS,
                "Preferred Skills",
                "Docker, Kubernetes",
            ),
            _make_section(
                SectionType.RESPONSIBILITIES,
                "Responsibilities",
                "- Design backend services\n- Write unit tests\n- Review PRs",
            ),
            _make_section(
                SectionType.QUALIFICATIONS,
                "Qualifications",
                "- BS/MS in CS or equivalent",
            ),
        ]
    )


# ── Happy path ────────────────────────────────────────────────────────────────


def test_job_builder_happy_path() -> None:
    cir = _full_jd_cir()
    builder = JobBuilder()
    jd = builder.build(cir=cir)

    assert jd.title == "Senior Python Engineer"
    assert jd.company == "Acme Corp"
    assert jd.location == "Remote"
    assert jd.employment_type == "Full-time"
    assert jd.experience_required == "5+ years"
    assert "Python" in jd.required_skills
    assert "FastAPI" in jd.required_skills
    assert "Docker" in jd.preferred_skills
    assert len(jd.responsibilities) == 3
    assert len(jd.qualifications) == 1


def test_job_integration_happy_path() -> None:
    cir = _full_jd_cir()
    pipeline = JobIntegration()
    jd = pipeline.process(cir)
    assert jd.title == "Senior Python Engineer"
    assert "python" in jd.keywords


# ── Missing title ─────────────────────────────────────────────────────────────


def test_job_builder_missing_title() -> None:
    cir = _make_cir(
        [
            _make_section(SectionType.COMPANY, "Company", "Acme Corp"),
            _make_section(
                SectionType.REQUIRED_SKILLS, "Required Skills", "Python, Django"
            ),
            _make_section(
                SectionType.RESPONSIBILITIES,
                "Responsibilities",
                "- Build APIs",
            ),
        ]
    )
    with pytest.raises(JobValidationError, match="Job Title is required"):
        JobBuilder().build(cir=cir)


# ── Missing skills ────────────────────────────────────────────────────────────


def test_job_builder_missing_required_skills() -> None:
    cir = _make_cir(
        [
            _make_section(SectionType.JOB_TITLE, "Job Title", "Backend Engineer"),
            _make_section(SectionType.COMPANY, "Company", "Acme Corp"),
            _make_section(
                SectionType.RESPONSIBILITIES,
                "Responsibilities",
                "- Build APIs",
            ),
        ]
    )
    with pytest.raises(
        JobValidationError, match="At least one required skill must be present"
    ):
        JobBuilder().build(cir=cir)


# ── Duplicate skills ──────────────────────────────────────────────────────────


def test_job_validator_duplicate_required_skills() -> None:
    from app.application.job_builder.job_validator import JobValidator

    validator = JobValidator()
    errors = validator.validate(
        {
            "title": "Engineer",
            "company": "Corp",
            "required_skills": ["Python", "Python", "Go"],
            "preferred_skills": [],
            "responsibilities": ["Build APIs"],
        }
    )
    assert "required_skills.duplicate" in errors


# ── Empty responsibilities ────────────────────────────────────────────────────


def test_job_validator_empty_responsibilities() -> None:
    from app.application.job_builder.job_validator import JobValidator

    validator = JobValidator()
    errors = validator.validate(
        {
            "title": "Engineer",
            "company": "Corp",
            "required_skills": ["Python"],
            "preferred_skills": [],
            "responsibilities": [],
        }
    )
    assert "responsibilities" in errors


# ── Pipeline error propagation ────────────────────────────────────────────────


def test_job_pipeline_raises_on_invalid_cir() -> None:
    with pytest.raises(JobPipelineError):
        JobIntegration().process(None)  # type: ignore[arg-type]
