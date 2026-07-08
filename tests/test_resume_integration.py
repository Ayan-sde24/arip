"""End-to-end integration and validation tests for the Resume Builder pipeline."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.resume_integration import (
    ResumeIntegration,
    ResumePipelineError,
)
from app.application.resume_builder.resume_validator import ResumeValidator
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection
from app.domain.entities.page import Page
from app.domain.entities.section_type import SectionType
from app.domain.entities.text_block import TextBlock


def _setup_full_cir() -> CanonicalIntermediateRepresentation:
    """Helper to mock a fully populated valid CIR for a resume."""
    doc_id = uuid4()
    now = datetime.now(UTC)

    document = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="12345abc",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    sections = [
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.CONTACT,
            title="Contact Info",
            content="Alice Smith\nalice@example.com\n+1 (555) 019-2834\nhttps://linkedin.com/in/alice",
            page_number=1,
            start_block=0,
            end_block=0,
            confidence=1.0,
        ),
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.EDUCATION,
            title="Education",
            content=(
                "Stanford University\n"
                "Bachelor of Science in Computer Science\n"
                "2018 - 2022\nGPA: 3.9"
            ),
            page_number=1,
            start_block=1,
            end_block=1,
            confidence=1.0,
        ),
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.EXPERIENCE,
            title="Work Experience",
            content=(
                "Google Inc. - Software Engineer\n"
                "2022 - Present\n"
                "Developed backend services."
            ),
            page_number=1,
            start_block=2,
            end_block=2,
            confidence=1.0,
        ),
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.PROJECTS,
            title="Projects",
            content=(
                "Personal Website (https://alice.dev)\n"
                "Built portfolio using React.\n"
                "Skills: React, Python"
            ),
            page_number=1,
            start_block=3,
            end_block=3,
            confidence=1.0,
        ),
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.SKILLS,
            title="Skills",
            content="Languages: Python, Go, React",
            page_number=1,
            start_block=4,
            end_block=4,
            confidence=1.0,
        ),
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.CERTIFICATIONS,
            title="Certifications",
            content="AWS Solutions Architect - Amazon | 2021",
            page_number=1,
            start_block=5,
            end_block=5,
            confidence=1.0,
        ),
        DocumentSection(
            id=uuid4(),
            section_type=SectionType.ACHIEVEMENTS,
            title="Achievements",
            content="Hackathon Winner - 1st place | 2022",
            page_number=1,
            start_block=6,
            end_block=6,
            confidence=1.0,
        ),
    ]

    full_text = "\n\n".join(sec.content for sec in sections)
    page = Page(
        page_number=1,
        text_blocks=[
            TextBlock(text=sec.content, page=1, block_index=idx, reading_order=idx)
            for idx, sec in enumerate(sections)
        ],
    )

    content = DocumentContent(
        document=document,
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
        average_section_length=len(full_text) / len(sections),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=sections,
        statistics=stats,
        pipeline_version="1.0",
    )


def test_resume_integration_pipeline_success() -> None:
    """Test executing the end-to-end integration pipeline with a valid CIR."""
    cir = _setup_full_cir()
    pipeline = ResumeIntegration()
    resume = pipeline.process(cir)

    assert resume.candidate is not None
    assert resume.candidate.name == "Alice Smith"
    assert resume.candidate.email == "alice@example.com"

    assert len(resume.education) == 1
    assert resume.education[0].institution == "Stanford University"

    assert len(resume.experience) == 1
    assert resume.experience[0].company == "Google Inc."

    assert len(resume.projects) == 1
    assert resume.projects[0].title == "Personal Website"

    assert "Python" in resume.skills
    assert "React" in resume.skills

    assert len(resume.certifications) == 1
    assert resume.certifications[0].name == "AWS Solutions Architect"

    assert len(resume.achievements) == 1
    assert resume.achievements[0].title == "Hackathon Winner"


def test_resume_integration_cross_field_consistency_error() -> None:
    """Test validation fails when project uses a missing skill."""
    import dataclasses

    cir = _setup_full_cir()
    new_sections = []
    for sec in cir.sections:
        if sec.section_type == SectionType.PROJECTS:
            new_sections.append(
                dataclasses.replace(
                    sec,
                    content=(
                        "Personal Website (https://alice.dev)\n"
                        "Built portfolio using React.\n"
                        "Skills: React, Python, Docker"
                    ),
                )
            )
        else:
            new_sections.append(sec)
    cir = dataclasses.replace(cir, sections=new_sections)

    pipeline = ResumeIntegration()
    with pytest.raises(ResumePipelineError, match="Project skill 'Docker' is missing"):
        pipeline.process(cir)


def test_resume_integration_empty_sections() -> None:
    """Test validation fails when a critical section like Skills is empty."""
    import dataclasses

    cir = _setup_full_cir()
    new_sections = [
        sec for sec in cir.sections if sec.section_type != SectionType.SKILLS
    ]
    cir = dataclasses.replace(cir, sections=new_sections)

    pipeline = ResumeIntegration()
    with pytest.raises(ResumePipelineError, match="Skills section cannot be empty"):
        pipeline.process(cir)


def test_resume_validator_duplicate_entities() -> None:
    """Test validator directly raises errors on duplicate entities in Resume."""
    from app.application.resume_builder.resume_assembler import ResumeAssembler
    from app.domain.entities.resume import Education

    cir = _setup_full_cir()
    pipeline = ResumeIntegration()
    candidate = pipeline.candidate_builder.build(cir=cir)
    edu_list = pipeline.education_builder.build(cir=cir)
    exp_list = pipeline.experience_builder.build(cir=cir)
    proj_list = pipeline.project_builder.build(cir=cir)
    skills = pipeline.skill_builder.build(cir=cir)
    certs = pipeline.certification_builder.build(cir=cir)
    achievements = pipeline.achievement_builder.build(cir=cir)

    duplicate_edu = Education(
        institution="Stanford University",
        degree="Bachelor of Science",
        major="Computer Science",
    )
    edu_list.append(duplicate_edu)

    assembler = ResumeAssembler()
    resume = assembler.assemble(
        document=cir.document,
        candidate=candidate,
        education=edu_list,
        experience=exp_list,
        projects=proj_list,
        skills=skills,
        certifications=certs,
        achievements=achievements,
    )

    validator = ResumeValidator()
    result = validator.validate(resume)
    assert not result.is_valid
    assert any(
        "Duplicate education entry" in item
        for err in result.errors.values()
        for item in err
    )
