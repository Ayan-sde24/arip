"""Validator for checking Resume structural integrity and cross-field consistency."""

import re
from dataclasses import dataclass, field

from app.domain.entities.resume import Resume


@dataclass
class ResumeValidationResult:
    """Result of running validation on a complete Resume domain entity."""

    is_valid: bool
    errors: dict[str, list[str]] = field(default_factory=dict)


class ResumeValidator:
    """Validator class for validating Resume domains and cross-field constraints."""

    YEAR_RE = re.compile(r"\b(19\d{2}|2\d{3})\b")

    def validate(self, resume: Resume) -> ResumeValidationResult:
        """Validate the compiled Resume domain entity.

        Args:
            resume: The Resume object to validate.

        Returns:
            A ResumeValidationResult indicating success or specific errors.
        """
        errors: dict[str, list[str]] = {}

        # 1. Candidate validation
        if resume.candidate is None:
            errors.setdefault("candidate", []).append("Candidate is required")
        else:
            if not resume.candidate.name:
                errors.setdefault("candidate.name", []).append(
                    "Candidate name cannot be empty"
                )
            if not resume.candidate.email:
                errors.setdefault("candidate.email", []).append(
                    "Candidate email cannot be empty"
                )
            if not resume.candidate.phone:
                errors.setdefault("candidate.phone", []).append(
                    "Candidate phone cannot be empty"
                )

        # 2. Education validation
        for idx, edu in enumerate(resume.education):
            if not edu.institution:
                errors.setdefault(f"education_{idx}.institution", []).append(
                    "Institution is required"
                )
            if not edu.degree:
                errors.setdefault(f"education_{idx}.degree", []).append(
                    "Degree is required"
                )
            # Check chronological year order
            if edu.start_date and edu.end_date:
                self._check_years(
                    edu.start_date,
                    edu.end_date,
                    f"education_{idx}.dates",
                    errors,
                )

        # 3. Experience validation
        for idx, exp in enumerate(resume.experience):
            if not exp.company:
                errors.setdefault(f"experience_{idx}.company", []).append(
                    "Company is required"
                )
            if not exp.role:
                errors.setdefault(f"experience_{idx}.role", []).append(
                    "Role/Job Title is required"
                )
            # Check chronological year order
            if exp.start_date and exp.end_date:
                self._check_years(
                    exp.start_date,
                    exp.end_date,
                    f"experience_{idx}.dates",
                    errors,
                )

        # 4. Project validation
        for idx, proj in enumerate(resume.projects):
            if not proj.title:
                errors.setdefault(f"projects_{idx}.title", []).append(
                    "Project Title is required"
                )

        # 5. Skills validation
        if not resume.skills:
            errors.setdefault("skills", []).append("Skills list cannot be empty")

        # 6. Cross-field consistency
        # Verify that all skills used in projects are present in the master skills list
        master_skills = {s.lower() for s in resume.skills}
        for idx, proj in enumerate(resume.projects):
            for skill in proj.skills:
                if skill.lower() not in master_skills:
                    errors.setdefault(f"projects_{idx}.consistency", []).append(
                        f"Project skill '{skill}' is missing "
                        "from the master skills list"
                    )

        # Verify duplicate records
        # Duplicate Education
        edu_keys = set()
        for idx, edu in enumerate(resume.education):
            key = (
                edu.institution.lower().strip() if edu.institution else "",
                edu.degree.lower().strip() if edu.degree else "",
                edu.major.lower().strip() if edu.major else "",
            )
            if key in edu_keys:
                errors.setdefault(f"education_{idx}.duplicate", []).append(
                    f"Duplicate education entry: {edu.institution}, {edu.degree}"
                )
            edu_keys.add(key)

        # Duplicate Experience
        exp_keys = set()
        for idx, exp in enumerate(resume.experience):
            exp_key = (
                exp.company.lower().strip() if exp.company else "",
                exp.role.lower().strip() if exp.role else "",
            )
            if exp_key in exp_keys:
                errors.setdefault(f"experience_{idx}.duplicate", []).append(
                    f"Duplicate experience entry: {exp.company}, {exp.role}"
                )
            exp_keys.add(exp_key)

        is_valid = len(errors) == 0
        return ResumeValidationResult(is_valid=is_valid, errors=errors)

    def _check_years(
        self,
        start: str,
        end: str,
        key: str,
        errors: dict[str, list[str]],
    ) -> None:
        """Verify start year is <= end year if both are years."""
        start_match = self.YEAR_RE.search(start)
        end_match = self.YEAR_RE.search(end)
        if start_match and end_match:
            try:
                start_yr = int(start_match.group(1))
                end_yr = int(end_match.group(1))
                if start_yr > end_yr:
                    errors.setdefault(key, []).append(
                        f"Start year ({start_yr}) cannot be after end year ({end_yr})"
                    )
            except ValueError:
                pass
