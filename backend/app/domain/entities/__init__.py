"""Domain entity definitions."""

from app.domain.entities.agent_result import AgentResult
from app.domain.entities.analysis_context import AnalysisContext
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.evidence import Evidence
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recommendation import Recommendation
from app.domain.entities.resume import (
    Achievement,
    Certification,
    Education,
    Experience,
    Project,
    Resume,
)

__all__ = [
    "AgentResult",
    "AnalysisContext",
    "Candidate",
    "Document",
    "DocumentStatus",
    "DocumentType",
    "Evidence",
    "JobDescription",
    "Recommendation",
    "Resume",
    "Education",
    "Experience",
    "Project",
    "Certification",
    "Achievement",
]
