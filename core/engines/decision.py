"""
AIEOS Decision Engine

Compares approaches, generates tradeoff matrices, and produces
structured Decision Contracts backed by evidence from the Knowledge Engine.

A Decision Contract contains:
    - Objective
    - Success Criteria
    - Constraints
    - Alternatives Considered (with evidence citations)
    - Tradeoffs
    - Selected Approach (with rationale)
    - Risks and Mitigations
    - Reversibility Assessment
"""

import sqlite3
import json
from datetime import datetime, timezone


class DecisionEngine:
    """
    Evaluates decision candidates against evidence from the Knowledge Engine.
    Produces structured Decision Contracts.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def compare(self, candidates, criteria, evidence_entries=None):
        """
        Generate a tradeoff matrix comparing N candidates across M criteria.

        Parameters:
            candidates: list of str – option names (e.g. ["PostgreSQL", "MongoDB", "SQLite"])
            criteria:   list of str – evaluation dimensions (e.g. ["performance", "scalability", "maintainability"])
            evidence_entries: optional list of research_entry dicts from the Knowledge Engine

        Returns dict:
            matrix   – dict of {candidate: {criterion: {score, rationale, evidence_ids}}}
            summary  – human-readable comparison text
        """
        matrix = {}
        evidence_index = {}

        # Index evidence by domain keywords
        if evidence_entries:
            for entry in evidence_entries:
                keywords = (entry.get("summary", "") + " " + entry.get("title", "")).lower().split()
                for kw in keywords:
                    evidence_index.setdefault(kw, []).append(entry)

        for candidate in candidates:
            matrix[candidate] = {}
            candidate_lower = candidate.lower()

            for criterion in criteria:
                criterion_lower = criterion.lower()

                # Find evidence mentioning both candidate and criterion
                relevant_evidence = []
                if evidence_entries:
                    for entry in evidence_entries:
                        text = (entry.get("summary", "") + " " + entry.get("title", "")).lower()
                        if candidate_lower in text or criterion_lower in text:
                            relevant_evidence.append(entry)

                # Score based on evidence quality
                score = 50  # Neutral default
                rationale = f"No specific evidence found for {candidate} on {criterion}."

                if relevant_evidence:
                    # Higher trust = higher score
                    avg_trust = sum(e.get("trust_level", 4) for e in relevant_evidence) / len(relevant_evidence)
                    avg_relevance = sum(e.get("relevance_score", 0.5) for e in relevant_evidence) / len(relevant_evidence)

                    score = int(min(95, max(10, (5 - avg_trust) * 20 + avg_relevance * 30)))
                    top_source = min(relevant_evidence, key=lambda e: e.get("trust_level", 4))
                    rationale = f"Based on {len(relevant_evidence)} source(s). Best: [{top_source.get('source_type', 'unknown')}] {top_source.get('title', 'untitled')}"

                matrix[candidate][criterion] = {
                    "score": score,
                    "rationale": rationale,
                    "evidence_ids": [e.get("id") for e in relevant_evidence],
                }

        # Build summary
        summary_lines = [f"Comparison of {len(candidates)} candidates across {len(criteria)} criteria:\n"]
        for candidate in candidates:
            total = sum(matrix[candidate][c]["score"] for c in criteria)
            avg = total // len(criteria) if criteria else 0
            summary_lines.append(f"  {candidate}: avg score {avg}/100")
        summary = "\n".join(summary_lines)

        return {
            "matrix": matrix,
            "summary": summary,
            "candidates": candidates,
            "criteria": criteria,
        }

    def recommend(self, tradeoff_result):
        """
        Select the strongest candidate from a tradeoff comparison.

        Returns dict:
            recommendation  – name of the best candidate
            score           – composite score
            rationale       – why this was chosen
            risks           – identified weaknesses
            evidence_count  – how many sources back this choice
        """
        matrix = tradeoff_result["matrix"]
        candidates = tradeoff_result["candidates"]
        criteria = tradeoff_result["criteria"]

        if not candidates or not criteria:
            return {
                "recommendation": None,
                "score": 0,
                "rationale": "No candidates or criteria provided.",
                "risks": [],
                "evidence_count": 0,
            }

        # Score each candidate
        scores = {}
        for candidate in candidates:
            total = 0
            evidence_set = set()
            weak_criteria = []
            for criterion in criteria:
                cell = matrix[candidate].get(criterion, {"score": 50, "evidence_ids": []})
                total += cell["score"]
                evidence_set.update(cell.get("evidence_ids", []))
                if cell["score"] < 40:
                    weak_criteria.append(criterion)
            scores[candidate] = {
                "total": total,
                "avg": total // len(criteria),
                "evidence_count": len(evidence_set),
                "weak_criteria": weak_criteria,
            }

        # Pick the best
        best = max(scores.items(), key=lambda x: x[1]["total"])
        best_name = best[0]
        best_data = best[1]

        # Build risks from weak criteria
        risks = []
        for weak in best_data["weak_criteria"]:
            risks.append(f"Low score on '{weak}' — requires further validation.")

        # Build rationale
        runner_ups = sorted(
            [(c, s) for c, s in scores.items() if c != best_name],
            key=lambda x: x[1]["total"],
            reverse=True,
        )
        rationale = f"{best_name} scored highest at {best_data['avg']}/100 average across {len(criteria)} criteria."
        if runner_ups:
            ru_name, ru_data = runner_ups[0]
            rationale += f" Runner-up: {ru_name} at {ru_data['avg']}/100."

        return {
            "recommendation": best_name,
            "score": best_data["avg"],
            "rationale": rationale,
            "risks": risks,
            "evidence_count": best_data["evidence_count"],
        }

    def generate_decision_contract(self, objective, candidates, criteria,
                                   constraints=None, evidence_entries=None):
        """
        Produce a complete Decision Contract.

        Returns a structured dict suitable for persistence and rendering.
        """
        # Run comparison
        comparison = self.compare(candidates, criteria, evidence_entries)
        recommendation = self.recommend(comparison)

        # Build the contract
        contract = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "objective": objective,
            "success_criteria": criteria,
            "constraints": constraints or [],
            "candidates_evaluated": candidates,
            "tradeoff_matrix": comparison["matrix"],
            "recommendation": recommendation["recommendation"],
            "recommendation_score": recommendation["score"],
            "rationale": recommendation["rationale"],
            "risks": recommendation["risks"],
            "evidence_count": recommendation["evidence_count"],
            "reversibility": "reversible" if recommendation["score"] > 60 else "requires_validation",
        }

        # Persist to tradeoffs table
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                dims = {}
                for c in criteria:
                    score_a = comparison["matrix"][candidates[i]][c]["score"]
                    score_b = comparison["matrix"][candidates[j]][c]["score"]
                    if score_a > score_b:
                        dims[c] = f"{candidates[i]} wins ({score_a} vs {score_b})"
                    elif score_b > score_a:
                        dims[c] = f"{candidates[j]} wins ({score_b} vs {score_a})"
                    else:
                        dims[c] = f"Tie ({score_a})"

                cursor.execute("""
                    INSERT INTO tradeoffs
                        (project_id, option_a, option_b, dimensions,
                         recommendation, rationale, evidence_ids)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    objective,
                    candidates[i],
                    candidates[j],
                    json.dumps(dims),
                    recommendation["recommendation"],
                    recommendation["rationale"],
                    json.dumps([]),
                ))
        conn.commit()
        conn.close()

        return contract
