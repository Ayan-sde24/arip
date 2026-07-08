"""Orchestrator for the complete Document Intelligence Pipeline."""

import time

from app.application.document_analysis.boundary_detector import BoundaryDetector
from app.application.document_analysis.cir_builder import CIRBuilder
from app.application.document_analysis.heading_detector import HeadingDetector
from app.application.document_analysis.pipeline_result import PipelineResult
from app.application.document_analysis.pipeline_validator import PipelineValidator
from app.application.document_analysis.section_detector_service import (
    SectionDetectorService,
)
from app.core.logger import get_logger
from app.domain.entities.document import Document
from app.infrastructure.parser.document_reader import DocumentIntelligencePipeline

logger = get_logger(__name__)


class DocumentPipeline:
    """End-to-end pipeline coordinating layout analysis and CIR construction."""

    def __init__(
        self,
        reader_pipeline: DocumentIntelligencePipeline | None = None,
        heading_detector: HeadingDetector | None = None,
        boundary_detector: BoundaryDetector | None = None,
        section_detector: SectionDetectorService | None = None,
        cir_builder: CIRBuilder | None = None,
        validator: PipelineValidator | None = None,
        version: str = "1.0",
    ) -> None:
        """Initialize pipeline with components."""
        self.reader_pipeline = (
            reader_pipeline
            if reader_pipeline is not None
            else DocumentIntelligencePipeline()
        )
        self.heading_detector = (
            heading_detector if heading_detector is not None else HeadingDetector()
        )
        self.boundary_detector = (
            boundary_detector if boundary_detector is not None else BoundaryDetector()
        )
        self.section_detector = (
            section_detector
            if section_detector is not None
            else SectionDetectorService()
        )
        self.cir_builder = (
            cir_builder if cir_builder is not None else CIRBuilder(version)
        )
        self.validator = validator if validator is not None else PipelineValidator()
        self.version = version

    def run(self, *, document: Document, content_bytes: bytes) -> PipelineResult:
        """Execute the pipeline stages end-to-end with validation, timing, and logging.

        Args:
            document: Source document metadata.
            content_bytes: Raw binary content of the document.

        Returns:
            A PipelineResult containing the successfully built CIR or captured errors.
        """
        start_time = time.perf_counter()
        warnings: list[str] = []
        errors: list[str] = []

        logger.info(
            "Document pipeline started for document_id={doc_id}",
            doc_id=document.document_id,
        )

        try:
            # 0. Validate Input
            warnings.extend(self.validator.validate_input(document, content_bytes))

            # 1. Document Reader Stage
            logger.info("Pipeline Stage 1: Running Document Reader & Layout Parser")
            content = self.reader_pipeline.run(
                document=document,
                content_bytes=content_bytes,
            )
            warnings.extend(self.validator.validate_reader_output(content))
            logger.info(
                "Pipeline Stage 1 Completed: pages={pages}",
                pages=len(content.pages),
            )

            # 2. Heading Detection Stage
            logger.info("Pipeline Stage 2: Running Heading Detection")
            headings = self.heading_detector.detect(content=content)
            warnings.extend(self.validator.validate_headings(headings))
            logger.info(
                "Pipeline Stage 2 Completed: headings_found={count}",
                count=len(headings),
            )

            # 3. Boundary Detection Stage
            logger.info("Pipeline Stage 3: Running Section Boundary Detection")
            boundaries = self.boundary_detector.detect(
                content=content,
                headings=headings,
            )
            warnings.extend(self.validator.validate_boundaries(boundaries))
            logger.info(
                "Pipeline Stage 3 Completed: boundaries_resolved={count}",
                count=len(boundaries),
            )

            # 4. Section Detection & Mapping Stage
            logger.info("Pipeline Stage 4: Running Section Classification & Extraction")
            sections = self.section_detector.detect_sections(
                content=content,
                boundaries=boundaries,
            )
            warnings.extend(self.validator.validate_sections(sections))
            logger.info(
                "Pipeline Stage 4 Completed: sections_classified={count}",
                count=len(sections),
            )

            # 5. CIR Builder Stage
            logger.info(
                "Pipeline Stage 5: Building Canonical Intermediate Representation"
            )
            cir = self.cir_builder.build(
                document=document,
                document_content=content,
                sections=sections,
            )
            warnings.extend(self.validator.validate_cir(cir))
            logger.info("Pipeline Stage 5 Completed: CIR successfully built")

            processing_time = time.perf_counter() - start_time
            logger.info(
                "Pipeline completed successfully in {duration:.4f}s",
                duration=processing_time,
            )

            return PipelineResult(
                success=True,
                pipeline_version=self.version,
                processing_time=round(processing_time, 4),
                cir=cir,
                warnings=warnings,
                errors=errors,
            )

        except Exception as e:
            processing_time = time.perf_counter() - start_time
            error_msg = f"Pipeline execution failed: {e.__class__.__name__}: {str(e)}"
            errors.append(error_msg)
            logger.exception(
                "Pipeline execution error for document_id={doc_id}",
                doc_id=document.document_id,
            )
            return PipelineResult(
                success=False,
                pipeline_version=self.version,
                processing_time=round(processing_time, 4),
                cir=None,
                warnings=warnings,
                errors=errors,
            )
