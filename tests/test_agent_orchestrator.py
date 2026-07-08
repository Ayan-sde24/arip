"""Unit tests for the central AgentOrchestrator pipeline."""

from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.document_analysis.pipeline_result import PipelineResult
from app.application.orchestrator.agent_orchestrator import AgentOrchestrator
from app.application.orchestrator.analysis_pipeline import AnalysisPipeline
from app.application.orchestrator.pipeline_executor import PipelineExecutor
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.candidate import Candidate
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.resume_optimization_report import (
    ResumeOptimizationReport,
)
from app.domain.entities.semantic_match_report import GapSummary, SemanticMatchReport


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


# ── Mocks Setup ───────────────────────────────────────────────────────────────


@pytest.fixture
def mock_components() -> dict[str, MagicMock]:
    # Mock DocumentPipeline
    cir_res = CanonicalIntermediateRepresentation(
        document=_doc("res.pdf"),
        document_content=MagicMock(),
        sections=[],
        statistics=MagicMock(),
    )
    mock_doc_pipeline = MagicMock()
    mock_doc_pipeline.run.return_value = PipelineResult(
        success=True, pipeline_version="1.0", processing_time=0.1, cir=cir_res
    )

    # Mock ResumeIntegration
    mock_resume = Resume(
        document=_doc("res.pdf"),
        candidate=Candidate(
            candidate_id=uuid4(),
            name="A",
            email="a@example.com",
            phone="123",
        ),
    )
    mock_resume_int = MagicMock()
    mock_resume_int.process.return_value = mock_resume

    # Mock JobIntegration
    mock_job = JobDescription(
        document=_doc("job.pdf"),
        title="Engineer",
        company="Tech",
    )
    mock_job_int = MagicMock()
    mock_job_int.process.return_value = mock_job

    # Mock SemanticEngine
    mock_sem_report = SemanticMatchReport(
        overall_score=80.0,
        skill_score=80.0,
        experience_score=80.0,
        education_score=80.0,
        keyword_score=80.0,
        matched_skills=[],
        missing_skills=[],
        extra_skills=[],
        matched_preferred_skills=[],
        required_skill_coverage=80.0,
        preferred_skill_coverage=0.0,
        matched_keywords=[],
        missing_keywords=[],
        keyword_coverage=80.0,
        gap_summary=GapSummary(),
        evidence=[],
    )
    mock_sem_engine = MagicMock()
    mock_sem_engine.analyse.return_value = mock_sem_report

    # Mock ATSAgent
    mock_ats_report = ATSReport(
        overall_ats_score=80.0,
        keyword_score=80.0,
        format_score=80.0,
        section_score=80.0,
        completeness_score=80.0,
        resume_parseability="High",
        ats_shortlisting_probability="High",
    )
    mock_ats_agent = MagicMock()
    mock_ats_agent.evaluate.return_value = mock_ats_report

    # Mock RecruiterAgent
    mock_rec_report = RecruiterReport(
        overall_recruiter_score=80.0,
        project_score=80.0,
        experience_score=80.0,
        presentation_score=80.0,
        leadership_score=80.0,
        communication_score=80.0,
        shortlist_probability="High",
        recruiter_verdict="Buy",
    )
    mock_recruiter_agent = MagicMock()
    mock_recruiter_agent.evaluate.return_value = mock_rec_report

    # Mock ResumeCoachAgent
    mock_coach_report = ResumeOptimizationReport(optimization_score=80.0)
    mock_coach_agent = MagicMock()
    mock_coach_agent.optimize.return_value = mock_coach_report

    return {
        "doc_pipeline": mock_doc_pipeline,
        "resume_int": mock_resume_int,
        "job_int": mock_job_int,
        "semantic_engine": mock_sem_engine,
        "ats_agent": mock_ats_agent,
        "recruiter_agent": mock_recruiter_agent,
        "coach_agent": mock_coach_agent,
    }


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_orchestrator_successful_pipeline(
    mock_components: dict[str, MagicMock],
) -> None:
    executor = PipelineExecutor(**mock_components)
    orchestrator = AgentOrchestrator(executor=executor)
    pipeline = AnalysisPipeline(orchestrator=orchestrator)

    result = pipeline.run(
        resume_doc=_doc("res.pdf"),
        resume_bytes=b"res_bytes",
        job_doc=_doc("job.pdf"),
        job_bytes=b"job_bytes",
    )

    assert result.status == "success"
    assert result.resume is not None
    assert result.job_description is not None
    assert result.semantic_report is not None
    assert result.ats_report is not None
    assert result.recruiter_report is not None
    assert result.optimization_report is not None
    assert len(result.errors) == 0


def test_orchestrator_semantic_failure(
    mock_components: dict[str, MagicMock],
) -> None:
    # Set semantic engine to fail
    mock_components["semantic_engine"].analyse.side_effect = Exception(
        "Semantic matching database timeout"
    )

    executor = PipelineExecutor(**mock_components)
    orchestrator = AgentOrchestrator(executor=executor)

    result = orchestrator.analyse(
        resume_doc=_doc("res.pdf"),
        resume_bytes=b"res_bytes",
        job_doc=_doc("job.pdf"),
        job_bytes=b"job_bytes",
    )

    assert result.status == "partial_success"
    assert result.resume is not None
    assert result.job_description is not None
    assert result.semantic_report is None
    # Subsequent stages should be skipped due to missing prerequisites
    assert result.ats_report is None
    assert result.recruiter_report is None
    assert result.optimization_report is None
    assert any("Semantic Engine match error" in err for err in result.errors)


def test_orchestrator_ats_failure(mock_components: dict[str, MagicMock]) -> None:
    # Set ATS agent to fail
    mock_components["ats_agent"].evaluate.side_effect = Exception("ATS scoring error")

    executor = PipelineExecutor(**mock_components)
    orchestrator = AgentOrchestrator(executor=executor)

    result = orchestrator.analyse(
        resume_doc=_doc("res.pdf"),
        resume_bytes=b"res_bytes",
        job_doc=_doc("job.pdf"),
        job_bytes=b"job_bytes",
    )

    assert result.status == "partial_success"
    assert result.resume is not None
    assert result.job_description is not None
    assert result.semantic_report is not None
    assert result.ats_report is None
    # Recruiter and Coach skipped because they need ATSReport
    assert result.recruiter_report is None
    assert result.optimization_report is None
    assert any("ATS Agent evaluation error" in err for err in result.errors)


def test_orchestrator_recruiter_failure(
    mock_components: dict[str, MagicMock],
) -> None:
    # Set recruiter agent to fail
    mock_components["recruiter_agent"].evaluate.side_effect = Exception(
        "Recruiter evaluation crash"
    )

    executor = PipelineExecutor(**mock_components)
    orchestrator = AgentOrchestrator(executor=executor)

    result = orchestrator.analyse(
        resume_doc=_doc("res.pdf"),
        resume_bytes=b"res_bytes",
        job_doc=_doc("job.pdf"),
        job_bytes=b"job_bytes",
    )

    assert result.status == "partial_success"
    assert result.resume is not None
    assert result.job_description is not None
    assert result.semantic_report is not None
    assert result.ats_report is not None
    assert result.recruiter_report is None
    # Coach skipped because it needs RecruiterReport
    assert result.optimization_report is None
    assert any("Recruiter Agent evaluation error" in err for err in result.errors)


def test_orchestrator_coach_failure(mock_components: dict[str, MagicMock]) -> None:
    # Set coach agent to fail
    mock_components["coach_agent"].optimize.side_effect = Exception(
        "Optimization timeout"
    )

    executor = PipelineExecutor(**mock_components)
    orchestrator = AgentOrchestrator(executor=executor)

    result = orchestrator.analyse(
        resume_doc=_doc("res.pdf"),
        resume_bytes=b"res_bytes",
        job_doc=_doc("job.pdf"),
        job_bytes=b"job_bytes",
    )

    assert result.status == "partial_success"
    assert result.resume is not None
    assert result.job_description is not None
    assert result.semantic_report is not None
    assert result.ats_report is not None
    assert result.recruiter_report is not None
    assert result.optimization_report is None
    assert any("Resume Coach optimization error" in err for err in result.errors)
