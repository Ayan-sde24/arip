"""Builder class for creating a Candidate domain entity from the CIR."""

from uuid import uuid4

from app.application.resume_builder.candidate_mapper import CandidateMapper
from app.application.resume_builder.candidate_validator import (
    CandidateValidationError,
    CandidateValidator,
)
from app.domain.entities.candidate import Candidate
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)


class CandidateBuilder:
    """Builder class responsible for producing a Candidate from a CIR."""

    def __init__(
        self,
        mapper: CandidateMapper | None = None,
        validator: CandidateValidator | None = None,
    ) -> None:
        """Initialize the Candidate builder.

        Args:
            mapper: Custom candidate mapper.
            validator: Custom candidate validator.
        """
        self.mapper = mapper if mapper is not None else CandidateMapper()
        self.validator = validator if validator is not None else CandidateValidator()

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> Candidate:
        """Extract, validate, and build a Candidate domain entity.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            An immutable Candidate domain entity.

        Raises:
            CandidateValidationError: If candidate validation fails.
        """
        if cir is None:
            raise CandidateValidationError("CIR cannot be null")

        # 1. Map fields from CIR
        raw_data = self.mapper.map_cir_to_candidate_data(cir)

        # 2. Validate mapped fields
        errors = self.validator.validate(raw_data)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise CandidateValidationError(
                f"Validation failed: {', '.join(flat_errors)}"
            )

        # 3. Construct Candidate entity
        return Candidate(
            candidate_id=uuid4(),
            name=raw_data["name"],
            email=raw_data["email"],
            phone=raw_data["phone"],
            linkedin=raw_data["linkedin"],
            github=raw_data["github"],
            portfolio=raw_data["portfolio"],
            location=raw_data["location"],
        )
