"""Builder class for creating Education domain entities from the CIR."""

from app.application.resume_builder.education_mapper import EducationMapper
from app.application.resume_builder.education_validator import (
    EducationValidationError,
    EducationValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.resume import Education


class EducationBuilder:
    """Builder class responsible for producing Education domain entities from a CIR."""

    def __init__(
        self,
        mapper: EducationMapper | None = None,
        validator: EducationValidator | None = None,
    ) -> None:
        """Initialize the Education builder.

        Args:
            mapper: Custom education mapper.
            validator: Custom education validator.
        """
        self.mapper = mapper if mapper is not None else EducationMapper()
        self.validator = validator if validator is not None else EducationValidator()

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[Education]:
        """Extract, validate, and build a list of Education domain entities.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of validated Education domain entities.

        Raises:
            EducationValidationError: If education validation fails.
        """
        if cir is None:
            raise EducationValidationError("CIR cannot be null")

        # 1. Map records from CIR
        raw_records = self.mapper.map_cir_to_education_records(cir)

        # 2. Validate mapped records
        errors = self.validator.validate(raw_records)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise EducationValidationError(
                f"Validation failed: {', '.join(flat_errors)}"
            )

        # 3. Construct list of Education entities
        education_list: list[Education] = []
        for rec in raw_records:
            edu = Education(
                institution=rec["institution"],
                degree=rec["degree"],
                major=rec["major"],
                start_date=rec["start_date"],
                end_date=rec["end_date"],
                gpa=rec["gpa"],
                details=rec["details"],
            )
            education_list.append(edu)

        return education_list
