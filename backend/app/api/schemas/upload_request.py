"""Schemas for document upload and analysis triggers."""

from pydantic import BaseModel, Field


class AnalysisTriggerRequest(BaseModel):
    """Payload to trigger end-to-end multi-agent resume analysis."""

    resume_id: str = Field(description="UUID string of the uploaded resume document.")
    job_id: str = Field(description="UUID string of the uploaded job description.")
