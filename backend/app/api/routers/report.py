"""Report router for fetching formatted analysis reports."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import ANALYSIS_STORE, get_analysis_presenter
from app.api.schemas.analysis_response import AnalysisResponseSchema
from app.application.dto.analysis_presenter import AnalysisPresenter

router = APIRouter(prefix="/report", tags=["report"])


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_analysis_report(
    analysis_id: str,
    presenter: Annotated[AnalysisPresenter, Depends(get_analysis_presenter)],
) -> AnalysisResponseSchema:
    """Retrieve the formatted analysis report DTO payload by analysis run ID."""
    result = ANALYSIS_STORE.get(analysis_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report {analysis_id} not found.",
        )

    dto = presenter.present(result)
    return AnalysisResponseSchema(
        analysis_id=analysis_id,
        status=result.status,
        result=dto,
    )
