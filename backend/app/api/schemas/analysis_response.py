"""Schemas for analysis API responses."""

from typing import Any

from pydantic import BaseModel


class AnalysisResponseSchema(BaseModel):
    """Payload returned by the analysis trigger/status endpoint."""

    analysis_id: str
    status: str
    result: Any | None = None
