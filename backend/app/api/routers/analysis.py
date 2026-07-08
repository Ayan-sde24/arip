"""Analysis router for executing and retrieving resume analyses."""

import glob
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    ANALYSIS_STORE,
    get_agent_orchestrator,
    get_analysis_presenter,
)
from app.api.schemas.analysis_response import AnalysisResponseSchema
from app.api.schemas.upload_request import AnalysisTriggerRequest
from app.application.dto.analysis_presenter import AnalysisPresenter
from app.application.orchestrator.agent_orchestrator import AgentOrchestrator
from app.core.config import Settings, get_settings
from app.core.logger import get_logger
from app.domain.entities.document import Document, DocumentStatus, DocumentType

router = APIRouter(tags=["analysis"])
logger = get_logger(__name__)


def _find_file_and_read(
    file_id: str, directory: Path, doc_type: DocumentType
) -> tuple[Document, bytes]:
    """Find file matching file_id.* and return metadata + content bytes."""
    pattern = str(directory / f"{file_id}.*")
    matches = glob.glob(pattern)
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Uploaded file {file_id} not found in {directory}",
        )

    file_path = Path(matches[0])
    content_bytes = file_path.read_bytes()

    now = datetime.now(UTC)
    doc = Document(
        document_id=uuid4(),
        document_type=doc_type,
        original_filename=file_path.name,
        stored_filename=file_path.name,
        mime_type="application/octet-stream",
        extension=file_path.suffix.lstrip("."),
        checksum="sha256",
        size=len(content_bytes),
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )
    return doc, content_bytes


@router.post(
    "/api/analyze",
    response_model=AnalysisResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def analyze_documents(
    payload: AnalysisTriggerRequest,
    settings: Annotated[Settings, Depends(get_settings)],
    orchestrator: Annotated[AgentOrchestrator, Depends(get_agent_orchestrator)],
    presenter: Annotated[AnalysisPresenter, Depends(get_analysis_presenter)],
) -> AnalysisResponseSchema:
    """Trigger the multi-agent analysis flow on uploaded files."""
    # 1. Retrieve files
    resume_doc, resume_bytes = _find_file_and_read(
        payload.resume_id, settings.resume_upload_dir, DocumentType.RESUME
    )
    job_doc, job_bytes = _find_file_and_read(
        payload.job_id, settings.job_upload_dir, DocumentType.JOB_DESCRIPTION
    )

    # 2. Run analysis
    try:
        result = orchestrator.analyse(
            resume_doc=resume_doc,
            resume_bytes=resume_bytes,
            job_doc=job_doc,
            job_bytes=job_bytes,
        )
    except Exception as exc:
        logger.exception("Analysis execution failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {exc}",
        ) from exc

    # 3. Store result in-memory
    analysis_id = str(uuid4())
    ANALYSIS_STORE[analysis_id] = result

    # 4. Present as DTO payload
    dto = presenter.present(result)

    return AnalysisResponseSchema(
        analysis_id=analysis_id,
        status=result.status,
        result=dto,
    )


@router.get(
    "/api/analysis/{analysis_id}",
    response_model=AnalysisResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_analysis_result(
    analysis_id: str,
    presenter: Annotated[AnalysisPresenter, Depends(get_analysis_presenter)],
) -> AnalysisResponseSchema:
    """Retrieve a completed multi-agent analysis report by ID."""
    result = ANALYSIS_STORE.get(analysis_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis run {analysis_id} not found.",
        )

    dto = presenter.present(result)
    return AnalysisResponseSchema(
        analysis_id=analysis_id,
        status=result.status,
        result=dto,
    )
