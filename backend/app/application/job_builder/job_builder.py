"""Builder class for creating a JobDescription domain entity from the CIR."""

from app.application.job_builder.job_mapper import JobMapper
from app.application.job_builder.job_validator import (
    JobValidationError,
    JobValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.job_description import JobDescription


class JobBuilder:
    """Produces a JobDescription domain entity from a CIR."""

    def __init__(
        self,
        mapper: JobMapper | None = None,
        validator: JobValidator | None = None,
    ) -> None:
        self.mapper = mapper if mapper is not None else JobMapper()
        self.validator = validator if validator is not None else JobValidator()

    def build(self, *, cir: CanonicalIntermediateRepresentation) -> JobDescription:
        """Map, validate, and construct a JobDescription from the CIR.

        Raises:
            JobValidationError: If required fields are missing or invalid.
        """
        if cir is None:
            raise JobValidationError("CIR cannot be null")

        record = self.mapper.map_cir_to_job_record(cir)

        errors = self.validator.validate(record)
        if errors:
            flat = [f"{field}: {'; '.join(msgs)}" for field, msgs in errors.items()]
            raise JobValidationError(f"Validation failed: {', '.join(flat)}")

        return JobDescription(
            document=cir.document,
            title=record["title"],
            company=record["company"],
            location=record["location"],
            employment_type=record["employment_type"],
            experience_required=record["experience_required"],
            education_required=record["education_required"],
            required_skills=record["required_skills"],
            preferred_skills=record["preferred_skills"],
            responsibilities=record["responsibilities"],
            qualifications=record["qualifications"],
            benefits=record["benefits"],
            salary=record["salary"],
            keywords=record["keywords"],
            requirements=record["required_skills"],
        )
