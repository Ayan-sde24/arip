"""Builder class for creating Skill entities from the CIR."""

from dataclasses import dataclass

from app.application.resume_builder.skill_mapper import SkillMapper
from app.application.resume_builder.skill_validator import (
    SkillValidationError,
    SkillValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)


@dataclass(frozen=True)
class Skill:
    """Represents a candidate skill."""

    name: str
    category: str | None = None
    proficiency: str | None = None


class SkillBuilder:
    """Builder class responsible for producing Skill entities from a CIR."""

    def __init__(
        self,
        mapper: SkillMapper | None = None,
        validator: SkillValidator | None = None,
    ) -> None:
        """Initialize the Skill builder.

        Args:
            mapper: Custom skill mapper.
            validator: Custom skill validator.
        """
        self.mapper = mapper if mapper is not None else SkillMapper()
        self.validator = validator if validator is not None else SkillValidator()

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[Skill]:
        """Extract, validate, and build a list of Skill entities.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of validated Skill entities.

        Raises:
            SkillValidationError: If skill validation fails.
        """
        if cir is None:
            raise SkillValidationError("CIR cannot be null")

        # 1. Map records from CIR
        raw_records = self.mapper.map_cir_to_skill_records(cir)

        # 2. Validate mapped records
        errors = self.validator.validate(raw_records)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise SkillValidationError(f"Validation failed: {', '.join(flat_errors)}")

        # 3. Construct list of Skill entities
        skill_list: list[Skill] = []
        for rec in raw_records:
            skill = Skill(
                name=rec["name"],
                category=rec["category"],
                proficiency=rec["proficiency"],
            )
            skill_list.append(skill)

        return skill_list
