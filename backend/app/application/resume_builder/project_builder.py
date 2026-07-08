"""Builder class for creating Project domain entities from the CIR."""

from app.application.resume_builder.project_mapper import ProjectMapper
from app.application.resume_builder.project_validator import (
    ProjectValidationError,
    ProjectValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.resume import Project


class ProjectBuilder:
    """Builder class responsible for producing Project domain entities from a CIR."""

    def __init__(
        self,
        mapper: ProjectMapper | None = None,
        validator: ProjectValidator | None = None,
    ) -> None:
        """Initialize the Project builder.

        Args:
            mapper: Custom project mapper.
            validator: Custom project validator.
        """
        self.mapper = mapper if mapper is not None else ProjectMapper()
        self.validator = validator if validator is not None else ProjectValidator()

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[Project]:
        """Extract, validate, and build a list of Project domain entities.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of validated Project domain entities.

        Raises:
            ProjectValidationError: If project validation fails.
        """
        if cir is None:
            raise ProjectValidationError("CIR cannot be null")

        # 1. Map records from CIR
        raw_records = self.mapper.map_cir_to_project_records(cir)

        # 2. Validate mapped records
        errors = self.validator.validate(raw_records)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise ProjectValidationError(f"Validation failed: {', '.join(flat_errors)}")

        # 3. Construct list of Project entities
        project_list: list[Project] = []
        for rec in raw_records:
            proj = Project(
                title=rec["title"],
                description=rec["description"],
                url=rec["url"],
                skills=rec["skills"],
            )
            project_list.append(proj)

        return project_list
