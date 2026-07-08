"""Builder class for creating Experience domain entities from the CIR."""

from app.application.resume_builder.experience_mapper import ExperienceMapper
from app.application.resume_builder.experience_validator import (
    ExperienceValidationError,
    ExperienceValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.resume import Experience


class ExperienceBuilder:
    """Builder class responsible for producing Experience domain entities from a CIR."""

    def __init__(
        self,
        mapper: ExperienceMapper | None = None,
        validator: ExperienceValidator | None = None,
    ) -> None:
        """Initialize the Experience builder.

        Args:
            mapper: Custom experience mapper.
            validator: Custom experience validator.
        """
        self.mapper = mapper if mapper is not None else ExperienceMapper()
        self.validator = validator if validator is not None else ExperienceValidator()

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[Experience]:
        """Extract, validate, and build a list of Experience domain entities.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of validated Experience domain entities.

        Raises:
            ExperienceValidationError: If experience validation fails.
        """
        if cir is None:
            raise ExperienceValidationError("CIR cannot be null")

        # 1. Map records from CIR
        raw_records = self.mapper.map_cir_to_experience_records(cir)

        # 2. Validate mapped records
        errors = self.validator.validate(raw_records)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise ExperienceValidationError(
                f"Validation failed: {', '.join(flat_errors)}"
            )

        # 3. Construct list of Experience entities
        experience_list: list[Experience] = []
        for rec in raw_records:
            exp = Experience(
                company=rec["company"],
                role=rec["role"],
                location=rec["location"],
                start_date=rec["start_date"],
                end_date=rec["end_date"],
                description=rec["description"],
                skills=rec["skills"],
            )
            experience_list.append(exp)

        return experience_list
