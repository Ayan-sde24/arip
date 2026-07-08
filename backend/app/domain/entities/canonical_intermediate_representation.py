"""Domain entity representing the Canonical Intermediate Representation (CIR)."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.domain.entities.document import Document
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection


@dataclass(frozen=True)
class CanonicalIntermediateRepresentation:
    """Domain entity containing the Canonical Intermediate Representation (CIR).

    This object is the unified representation of a processed document and is
    consumed by downstream specific builders (e.g. Resume Builder).

    Attributes:
        document: The source document entity.
        document_content: The parsed document content.
        sections: List of detected document sections.
        statistics: Qualitative and quantitative CIR metrics.
        metadata: Arbitrary metadata dictionary.
        created_at: The timestamp when this CIR was created.
        pipeline_version: Version of the pipeline used to build this CIR.
    """

    document: Document
    document_content: DocumentContent
    sections: list[DocumentSection]
    statistics: CIRStatistics
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    pipeline_version: str = "1.0"
