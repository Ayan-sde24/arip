"""Builder class for creating Achievement domain entities from the CIR."""

from app.application.resume_builder.achievement_mapper import (
    AchievementMapper,
)
from app.application.resume_builder.achievement_validator import (
    AchievementValidationError,
    AchievementValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.resume import Achievement


class AchievementBuilder:
    """Builder class responsible for producing Achievements from a CIR."""

    def __init__(
        self,
        mapper: AchievementMapper | None = None,
        validator: AchievementValidator | None = None,
    ) -> None:
        """Initialize the Achievement builder.

        Args:
            mapper: Custom achievement mapper.
            validator: Custom achievement validator.
        """
        self.mapper = mapper if mapper is not None else AchievementMapper()
        self.validator = validator if validator is not None else AchievementValidator()

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[Achievement]:
        """Extract, validate, and build a list of Achievement domain entities.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of validated Achievement domain entities.

        Raises:
            AchievementValidationError: If achievement validation fails.
        """
        if cir is None:
            raise AchievementValidationError("CIR cannot be null")

        # 1. Map records from CIR
        raw_records = self.mapper.map_cir_to_achievement_records(cir)

        # 2. Validate mapped records
        errors = self.validator.validate(raw_records)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise AchievementValidationError(
                f"Validation failed: {', '.join(flat_errors)}"
            )

        # 3. Construct list of Achievement entities
        achievement_list: list[Achievement] = []
        for rec in raw_records:
            ach = Achievement(
                title=rec["title"],
                description=rec["description"],
                date=rec["date"],
            )
            achievement_list.append(ach)

        return achievement_list
