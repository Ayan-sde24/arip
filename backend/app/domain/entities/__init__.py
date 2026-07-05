"""Domain entity definitions."""

from app.domain.entities.agent_result import AgentResult
from app.domain.entities.analysis_context import AnalysisContext
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.evidence import Evidence
from app.domain.entities.job_description import JobDescription
from app.domain.entities.page import Page
from app.domain.entities.recommendation import Recommendation
from app.domain.entities.resume import (
    Achievement,
    Certification,
    Education,
    Experience,
    Project,
    Resume,
)
from app.domain.entities.text_block import TextBlock

__all__ = [
    "Achievement",
    "AgentResult",
    "AnalysisContext",
    "Candidate",
    "Certification",
    "Document",
    "DocumentContent",
    "DocumentStatus",
    "DocumentType",
    "Education",
    "Evidence",
    "Experience",
    "JobDescription",
    "Page",
    "Project",
    "Recommendation",
    "Resume",
    "TextBlock",
]
