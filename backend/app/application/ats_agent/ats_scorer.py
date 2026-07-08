"""ATS Scorer running formatting, section, completeness, and keyword rules."""

from typing import Any

from app.application.ats_agent.ats_rule_engine import ATSRuleEngine
from app.application.ats_agent.completeness_score import CompletenessScoreRule
from app.application.ats_agent.format_score import FormatScoreRule
from app.application.ats_agent.keyword_score import KeywordScoreRule
from app.application.ats_agent.section_score import SectionScoreRule
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class ATSScorer:
    """Orchestrates ATS rules execution and compiles aggregated metrics."""

    def __init__(
        self,
        keyword_rule: KeywordScoreRule | None = None,
        format_rule: FormatScoreRule | None = None,
        section_rule: SectionScoreRule | None = None,
        completeness_rule: CompletenessScoreRule | None = None,
    ) -> None:
        self.keyword_rule = keyword_rule or KeywordScoreRule()
        self.format_rule = format_rule or FormatScoreRule()
        self.section_rule = section_rule or SectionScoreRule()
        self.completeness_rule = completeness_rule or CompletenessScoreRule()

        self.engine = ATSRuleEngine(
            [
                self.keyword_rule,
                self.format_rule,
                self.section_rule,
                self.completeness_rule,
            ]
        )

    def score(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, Any]:
        """Execute all rules and calculate overall ATS score.

        Returns:
            A dictionary containing:
                - overall_score: float
                - keyword_score: float
                - format_score: float
                - section_score: float
                - completeness_score: float
                - strengths: list[str]
                - weaknesses: list[str]
                - recommendations: list[str]
                - rule_details: dict[str, Any]
        """
        results = self.engine.run(resume, job, semantic_report)

        keyword_res = results[0]
        format_res = results[1]
        section_res = results[2]
        completeness_res = results[3]

        keyword_score = keyword_res["score"]
        format_score = format_res["score"]
        section_score = section_res["score"]
        completeness_score = completeness_res["score"]

        # Calculate overall ATS score:
        # 40% Keyword Match, 20% Formatting, 20% Sections, 20% Completeness
        overall_score = round(
            keyword_score * 0.40
            + format_score * 0.20
            + section_score * 0.20
            + completeness_score * 0.20,
            2,
        )

        strengths = []
        weaknesses = []
        recommendations = []

        for r in results:
            strengths.extend(r.get("strengths", []))
            weaknesses.extend(r.get("weaknesses", []))
            recommendations.extend(r.get("recommendations", []))

        # Remove duplicate strings to keep feedback clean
        strengths = list(dict.fromkeys(strengths))
        weaknesses = list(dict.fromkeys(weaknesses))
        recommendations = list(dict.fromkeys(recommendations))

        return {
            "overall_score": overall_score,
            "keyword_score": keyword_score,
            "format_score": format_score,
            "section_score": section_score,
            "completeness_score": completeness_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "rule_details": {
                "keyword": keyword_res.get("details", {}),
                "format": format_res.get("details", {}),
                "section": section_res.get("details", {}),
                "completeness": completeness_res.get("details", {}),
            },
        }
