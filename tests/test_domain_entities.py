"""Unit tests for universal document domain model entities."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domain.entities import (
    Achievement,
    AgentResult,
    AnalysisContext,
    Candidate,
    Certification,
    Document,
    DocumentSection,
    DocumentStatus,
    DocumentType,
    Education,
    Evidence,
    Experience,
    JobDescription,
    Project,
    Recommendation,
    Resume,
    SectionType,
    StructuredDocument,
)


def test_document_creation() -> None:
    """Test standard instantiation and immutability of the Document entity."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abcd12345",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
        metadata={"parser": "pypdf"},
    )

    assert doc.document_id == doc_id
    assert doc.document_type == DocumentType.RESUME
    assert doc.original_filename == "cv.pdf"
    assert doc.stored_filename == f"{doc_id}.pdf"
    assert doc.mime_type == "application/pdf"
    assert doc.extension == "pdf"
    assert doc.checksum == "abcd12345"
    assert doc.size == 1024
    assert doc.created_at == now
    assert doc.updated_at == now
    assert doc.status == DocumentStatus.UPLOADED
    assert doc.metadata == {"parser": "pypdf"}

    # Test Immutability
    with pytest.raises(FrozenInstanceError):
        doc.status = DocumentStatus.PROCESSING  # type: ignore[misc]


def test_candidate_creation() -> None:
    """Test Candidate instantiation and optional default values."""
    cand_id = uuid4()
    candidate = Candidate(
        candidate_id=cand_id,
        name="Alice Smith",
        email="alice@example.com",
        phone="+1234567890",
        linkedin="https://linkedin.com/in/alice",
    )

    assert candidate.candidate_id == cand_id
    assert candidate.name == "Alice Smith"
    assert candidate.email == "alice@example.com"
    assert candidate.phone == "+1234567890"
    assert candidate.linkedin == "https://linkedin.com/in/alice"
    assert candidate.github is None
    assert candidate.portfolio is None
    assert candidate.location is None

    with pytest.raises(FrozenInstanceError):
        candidate.name = "Bob"  # type: ignore[misc]


def test_resume_creation_with_nested_collections() -> None:
    """Test Resume creation with nested education, experience, and certifications."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abcd12345",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    cand_id = uuid4()
    candidate = Candidate(
        candidate_id=cand_id,
        name="Alice Smith",
        email="alice@example.com",
        phone="+1234567890",
    )

    edu = Education(
        institution="University of Tech",
        degree="B.Sc.",
        major="Computer Science",
        start_date="2020",
        end_date="2024",
        gpa=3.8,
        details=["Dean's List"],
    )

    exp = Experience(
        company="CodeCorp",
        role="Software Engineer",
        location="Remote",
        start_date="2023",
        end_date="Present",
        description=["Built scalable APIs"],
        skills=["Python", "FastAPI"],
    )

    proj = Project(
        title="ARIP Platform",
        description="Resume Intelligence App",
        url="https://github.com/arip",
        skills=["Python", "React"],
    )

    cert = Certification(
        name="AWS Solutions Architect",
        issuer="Amazon Web Services",
        issue_date="2025",
    )

    ach = Achievement(
        title="Hackathon Winner",
        description="First place in regional hackathon",
        date="2024",
    )

    resume = Resume(
        document=doc,
        candidate=candidate,
        education=[edu],
        experience=[exp],
        projects=[proj],
        skills=["Python", "FastAPI", "AWS"],
        certifications=[cert],
        achievements=[ach],
    )

    assert resume.document == doc
    assert resume.candidate == candidate
    assert len(resume.education) == 1
    assert resume.education[0].institution == "University of Tech"
    assert resume.education[0].details == ["Dean's List"]
    assert len(resume.experience) == 1
    assert resume.experience[0].company == "CodeCorp"
    assert resume.experience[0].skills == ["Python", "FastAPI"]
    assert len(resume.projects) == 1
    assert resume.projects[0].title == "ARIP Platform"
    assert resume.skills == ["Python", "FastAPI", "AWS"]
    assert len(resume.certifications) == 1
    assert resume.certifications[0].name == "AWS Solutions Architect"
    assert len(resume.achievements) == 1
    assert resume.achievements[0].title == "Hackathon Winner"

    with pytest.raises(FrozenInstanceError):
        resume.skills = ["Java"]  # type: ignore[misc]


def test_resume_default_empty_collections() -> None:
    """Test that Resume can be created with only Document, defaults to empty lists."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abcd12345",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    resume = Resume(document=doc)
    assert resume.candidate is None
    assert resume.education == []
    assert resume.experience == []
    assert resume.projects == []
    assert resume.skills == []
    assert resume.certifications == []
    assert resume.achievements == []


def test_job_description_creation() -> None:
    """Test creation and fields of the JobDescription entity."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.JOB_DESCRIPTION,
        original_filename="job.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="xyz789",
        size=2048,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    jd = JobDescription(
        document=doc,
        company="AI Solutions",
        title="Senior AI Engineer",
        requirements=["5+ years Python", "Experience with LLMs"],
        responsibilities=["Design agentic architectures", "Mentor juniors"],
        preferred_skills=["LangChain", "PyTorch"],
    )

    assert jd.document == doc
    assert jd.company == "AI Solutions"
    assert jd.title == "Senior AI Engineer"
    assert jd.requirements == ["5+ years Python", "Experience with LLMs"]
    assert jd.responsibilities == ["Design agentic architectures", "Mentor juniors"]
    assert jd.preferred_skills == ["LangChain", "PyTorch"]

    with pytest.raises(FrozenInstanceError):
        jd.company = "OtherCorp"  # type: ignore[misc]


def test_evidence_and_recommendation() -> None:
    """Test instantiation of Explainable AI helpers: Evidence and Recommendation."""
    ev = Evidence(
        title="Keyword Match",
        description="Found Python and FastAPI under experience section",
        source="ParserAgent",
        confidence=0.95,
        location="Experience[0].skills",
    )

    assert ev.title == "Keyword Match"
    assert ev.description == "Found Python and FastAPI under experience section"
    assert ev.source == "ParserAgent"
    assert ev.confidence == 0.95
    assert ev.location == "Experience[0].skills"

    rec = Recommendation(
        title="Add Certification Link",
        description="Verify AWS Solutions Architect certification with a URL",
        priority="Medium",
        category="Certifications",
        expected_impact="High",
        confidence=0.85,
    )

    assert rec.title == "Add Certification Link"
    assert rec.description == "Verify AWS Solutions Architect certification with a URL"
    assert rec.priority == "Medium"
    assert rec.category == "Certifications"
    assert rec.expected_impact == "High"
    assert rec.confidence == 0.85

    with pytest.raises(FrozenInstanceError):
        ev.confidence = 1.0  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        rec.confidence = 1.0  # type: ignore[misc]


def test_agent_result_creation() -> None:
    """Test standard instantiation and default values of AgentResult."""
    ev = Evidence(
        title="Keyword Match",
        description="Parsed skills",
        source="SkillAgent",
        confidence=0.9,
    )

    rec = Recommendation(
        title="Add Skill",
        description="Consider listing Docker",
        priority="Low",
        category="Skills",
        expected_impact="Low",
        confidence=0.7,
    )

    res = AgentResult(
        agent_name="SkillGapAgent",
        status="Success",
        score=0.8,
        confidence=0.9,
        strengths=["Good backend knowledge"],
        weaknesses=["Missing containerization skills"],
        recommendations=[rec],
        evidence=[ev],
        execution_time=1.45,
        metadata={"runner": "local-orchestrator"},
    )

    assert res.agent_name == "SkillGapAgent"
    assert res.status == "Success"
    assert res.score == 0.8
    assert res.confidence == 0.9
    assert res.strengths == ["Good backend knowledge"]
    assert res.weaknesses == ["Missing containerization skills"]
    assert res.recommendations == [rec]
    assert res.evidence == [ev]
    assert res.execution_time == 1.45
    assert res.metadata == {"runner": "local-orchestrator"}


def test_analysis_context_creation() -> None:
    """Test AnalysisContext holding resume, job description, and previous results."""
    now = datetime.now(UTC)
    doc_resume = Document(
        document_id=uuid4(),
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename="cv.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="123",
        size=100,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )
    doc_jd = Document(
        document_id=uuid4(),
        document_type=DocumentType.JOB_DESCRIPTION,
        original_filename="jd.pdf",
        stored_filename="jd.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="456",
        size=200,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    resume = Resume(document=doc_resume)
    jd = JobDescription(document=doc_jd, company="ACME", title="Developer")

    result = AgentResult(agent_name="ParserAgent", status="Success")

    context = AnalysisContext(
        resume=resume,
        job_description=jd,
        settings={"threshold": 0.75},
        previous_agent_results=[result],
        execution_metadata={"pipeline_id": "test-pipeline-123"},
    )

    assert context.resume == resume
    assert context.job_description == jd
    assert context.settings == {"threshold": 0.75}
    assert context.previous_agent_results == [result]
    assert context.execution_metadata == {"pipeline_id": "test-pipeline-123"}


def test_section_type_enum() -> None:
    """Test standard values and StrEnum properties of SectionType."""
    assert SectionType.SUMMARY == "summary"
    assert SectionType.EDUCATION == "education"
    assert SectionType.EXPERIENCE == "experience"
    assert SectionType.UNKNOWN == "unknown"


def test_document_section_creation_and_immutability() -> None:
    """Test standard instantiation and immutability of the DocumentSection entity."""
    section_id = uuid4()
    section = DocumentSection(
        id=section_id,
        section_type=SectionType.EXPERIENCE,
        title="Work Experience",
        content="Senior Software Engineer...",
        page_number=1,
        start_block=2,
        end_block=15,
        confidence=0.95,
        metadata={"keyword_match": True},
    )

    assert section.id == section_id
    assert section.section_type == SectionType.EXPERIENCE
    assert section.title == "Work Experience"
    assert section.content == "Senior Software Engineer..."
    assert section.page_number == 1
    assert section.start_block == 2
    assert section.end_block == 15
    assert section.confidence == 0.95
    assert section.metadata == {"keyword_match": True}

    with pytest.raises(FrozenInstanceError):
        section.confidence = 1.0  # type: ignore[misc]


def test_structured_document_creation_and_lookup() -> None:
    """Test StructuredDocument sections retrieval, metadata, and statistics."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abcd12345",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    section_exp = DocumentSection(
        id=uuid4(),
        section_type=SectionType.EXPERIENCE,
        title="Experience",
        content="Software engineer at company A",
        page_number=1,
        start_block=0,
        end_block=5,
        confidence=0.9,
    )

    section_edu = DocumentSection(
        id=uuid4(),
        section_type=SectionType.EDUCATION,
        title="Education",
        content="B.Sc in Computer Science",
        page_number=2,
        start_block=6,
        end_block=10,
        confidence=0.95,
    )

    struct_doc = StructuredDocument(
        document=doc,
        sections=[section_exp, section_edu],
        statistics={"total_sections": 2},
        metadata={"processed_by": "heuristic_analyzer"},
    )

    # Test attributes
    assert struct_doc.document == doc
    assert len(struct_doc.sections) == 2
    assert struct_doc.statistics == {"total_sections": 2}
    assert struct_doc.metadata == {"processed_by": "heuristic_analyzer"}

    # Test Section lookup methods
    assert struct_doc.has_section(SectionType.EXPERIENCE) is True
    assert struct_doc.has_section(SectionType.SKILLS) is False

    assert struct_doc.get_section(SectionType.EXPERIENCE) == section_exp
    assert struct_doc.get_section(SectionType.SKILLS) is None

    assert struct_doc.find_sections(SectionType.EXPERIENCE) == [section_exp]
    assert struct_doc.find_sections(SectionType.SKILLS) == []


def test_structured_document_empty() -> None:
    """Test StructuredDocument with no sections handles lookup gracefully."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abcd12345",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    struct_doc = StructuredDocument(document=doc)
    assert len(struct_doc.sections) == 0
    assert struct_doc.has_section(SectionType.EXPERIENCE) is False
    assert struct_doc.get_section(SectionType.EXPERIENCE) is None
    assert struct_doc.find_sections(SectionType.EXPERIENCE) == []
