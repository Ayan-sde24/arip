"""Builder class for creating Certification domain entities from the CIR."""

from app.application.resume_builder.certification_mapper import (
    CertificationMapper,
)
from app.application.resume_builder.certification_validator import (
    CertificationValidationError,
    CertificationValidator,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.resume import Certification


class CertificationBuilder:
    """Builder class responsible for producing Certifications from a CIR."""

    def __init__(
        self,
        mapper: CertificationMapper | None = None,
        validator: CertificationValidator | None = None,
    ) -> None:
        """Initialize the Certification builder.

        Args:
            mapper: Custom certification mapper.
            validator: Custom certification validator.
        """
        self.mapper = mapper if mapper is not None else CertificationMapper()
        self.validator = (
            validator if validator is not None else CertificationValidator()
        )

    def build(
        self,
        *,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[Certification]:
        """Extract, validate, and build a list of Certification domain entities.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of validated Certification domain entities.

        Raises:
            CertificationValidationError: If certification validation fails.
        """
        if cir is None:
            raise CertificationValidationError("CIR cannot be null")

        # 1. Map records from CIR
        raw_records = self.mapper.map_cir_to_certification_records(cir)

        # 2. Validate mapped records
        errors = self.validator.validate(raw_records)
        if errors:
            flat_errors = []
            for field_name, field_errs in errors.items():
                flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
            raise CertificationValidationError(
                f"Validation failed: {', '.join(flat_errors)}"
            )

        # 3. Construct list of Certification entities
        certification_list: list[Certification] = []
        for rec in raw_records:
            cert = Certification(
                name=rec["name"],
                issuer=rec["issuer"],
                issue_date=rec["issue_date"],
                expiration_date=rec["expiration_date"],
                url=rec["url"],
            )
            certification_list.append(cert)

        return certification_list
