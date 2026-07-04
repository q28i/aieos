"""
AIEOS Learning Engine

Transforms raw research into structured, reusable project knowledge.
This is the missing lifecycle phase between Research and Architecture.

Pipeline:
    Research Database
        → Knowledge Map
            → Tradeoffs
                → Decision Candidates
                    → Recommended Architecture

The Learning Engine does NOT just summarize. It:
    - Extracts patterns and anti-patterns from research entries
    - Identifies tradeoffs between competing approaches
    - Ranks decision candidates by evidence strength
    - Detects when knowledge becomes stale
    - Incrementally updates the project knowledge graph
"""

import sqlite3
import json
from datetime import datetime, timezone, timedelta
from .knowledge import KnowledgeEngine


class LearningEngine:
    """
    Synthesises raw research into structured project knowledge.
    Bridges the gap between collecting information and making decisions.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.knowledge = KnowledgeEngine(db_path)

    def synthesize(self, project_id, query=None, domain=None):
        """
        From raw collected entries, produce:
            - Extracted patterns and anti-patterns
            - Identified tradeoffs between approaches
            - Ranked decision candidates
            - Knowledge gaps requiring further research

        Returns a synthesis report dict.
        """
        entries = self.knowledge.get_entries(query=query, domain=domain)

        if not entries:
            return {
                "project_id": project_id,
                "patterns": [],
                "anti_patterns": [],
                "tradeoffs": [],
                "candidates": [],
                "gaps": ["No research entries found. Run 'aieos research <topic>' first."],
                "entry_count": 0,
            }

        # Build knowledge map
        kmap = self.knowledge.build_knowledge_map(project_id, entries)

        # Extract patterns (from high-trust entries)
        patterns = []
        anti_patterns = []
        for item in kmap.get("known", []):
            stmt = item.get("statement", "")
            stmt_lower = stmt.lower()
            # Heuristic: positive patterns vs anti-patterns
            if any(w in stmt_lower for w in ["best practice", "recommended", "standard",
                                              "proven", "efficient", "secure", "scalable"]):
                patterns.append({
                    "pattern": stmt,
                    "source": item.get("source", "unknown"),
                    "trust": item.get("trust", 4),
                })
            if any(w in stmt_lower for w in ["avoid", "deprecated", "anti-pattern",
                                              "vulnerable", "slow", "insecure", "legacy"]):
                anti_patterns.append({
                    "anti_pattern": stmt,
                    "source": item.get("source", "unknown"),
                    "trust": item.get("trust", 4),
                })

        # Identify tradeoffs by grouping entries with competing claims
        tradeoffs = []
        for contradiction in kmap.get("contradicted", []):
            tradeoffs.append({
                "domain": contradiction.get("domain", "general"),
                "description": contradiction.get("statement", ""),
                "requires_decision": True,
            })

        # Rank candidates – group by domain, score by evidence strength
        domain_groups = {}
        for entry in entries:
            d = entry.get("domain", "general")
            domain_groups.setdefault(d, []).append(entry)

        candidates = []
        for domain_name, domain_entries in domain_groups.items():
            avg_trust = sum(e.get("trust_level", 4) for e in domain_entries) / len(domain_entries)
            avg_relevance = sum(e.get("relevance_score", 0.5) for e in domain_entries) / len(domain_entries)
            evidence_score = int(min(95, (5 - avg_trust) * 20 + avg_relevance * 30))

            candidates.append({
                "domain": domain_name,
                "entry_count": len(domain_entries),
                "avg_trust": round(avg_trust, 1),
                "evidence_score": evidence_score,
                "top_sources": [e.get("title", "untitled") for e in sorted(
                    domain_entries, key=lambda x: x.get("trust_level", 4)
                )[:3]],
            })

        candidates.sort(key=lambda c: c["evidence_score"], reverse=True)

        # Identify gaps (assumed items with no high-trust backing)
        gaps = []
        for item in kmap.get("assumed", []):
            gaps.append(f"Assumed: {item.get('statement', 'unknown')} (source: {item.get('source', 'unknown')}, trust: Tier {item.get('trust', 4)})")
        for item in kmap.get("unknown", []):
            gaps.append(f"Unknown: {item.get('statement', 'unknown')}")

        return {
            "project_id": project_id,
            "patterns": patterns,
            "anti_patterns": anti_patterns,
            "tradeoffs": tradeoffs,
            "candidates": candidates,
            "gaps": gaps if gaps else ["No significant knowledge gaps detected."],
            "entry_count": len(entries),
            "knowledge_summary": {
                "known": len(kmap.get("known", [])),
                "assumed": len(kmap.get("assumed", [])),
                "contradicted": len(kmap.get("contradicted", [])),
                "unknown": len(kmap.get("unknown", [])),
            },
        }

    def update_knowledge_graph(self, project_id, new_entries):
        """
        Incrementally update the project's knowledge base with new evidence.

        Parameters:
            project_id:  the project identifier
            new_entries: list of research entry dicts to add

        Returns the updated coverage scores.
        """
        if new_entries:
            self.knowledge.collect(
                query=f"update:{project_id}",
                entries=new_entries,
            )

        # Rebuild the knowledge map with all entries
        all_entries = self.knowledge.get_entries()
        self.knowledge.build_knowledge_map(project_id, all_entries)

        return self.knowledge.evaluate_coverage()

    def detect_staleness(self, project_id, max_age_days=30):
        """
        Flag knowledge entries that may be outdated.

        Checks:
            - Research entries older than max_age_days
            - Entries from fast-moving domains (security, dependencies)
            - Entries with source_type 'blog' or 'ai_inference' (decay faster)

        Returns list of stale entry summaries.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cutoff = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).isoformat()

        # Time-based staleness
        cursor.execute("""
            SELECT id, title, source_type, trust_level, collected_at, domain
            FROM research_entries
            WHERE collected_at < ?
            ORDER BY collected_at ASC
        """, (cutoff,))

        stale = []
        for row in cursor.fetchall():
            entry = dict(row)
            reason = f"Entry is older than {max_age_days} days"

            # Faster decay for low-trust sources
            if entry["source_type"] in ("blog", "ai_inference", "reddit"):
                reason += " (low-trust source — decays faster)"
            if entry["domain"] in ("security", "dependencies", "vulnerabilities"):
                reason += " (fast-moving domain — check for updates)"

            stale.append({
                "id": entry["id"],
                "title": entry["title"],
                "source_type": entry["source_type"],
                "domain": entry["domain"],
                "collected_at": entry["collected_at"],
                "reason": reason,
            })

        conn.close()
        return stale

    def generate_learning_report(self, project_id, query=None, domain=None):
        """
        Produce a complete learning report combining synthesis and coverage.

        This is the output of the Learning phase in the lifecycle.
        """
        synthesis = self.synthesize(project_id, query=query, domain=domain)
        coverage = self.knowledge.evaluate_coverage(domain=domain)
        staleness = self.detect_staleness(project_id)

        return {
            "project_id": project_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "synthesis": synthesis,
            "evidence_profile": coverage,
            "stale_entries": staleness,
            "stale_count": len(staleness),
            "recommendation": _build_recommendation(synthesis, coverage),
        }


def _build_recommendation(synthesis, coverage):
    """Build a natural-language recommendation from synthesis and coverage data."""
    lines = []

    if coverage["evidence_score"] < 40:
        lines.append("Evidence is weak. Most knowledge comes from low-trust sources. Prioritize official documentation and peer-reviewed papers.")
    elif coverage["evidence_score"] < 70:
        lines.append("Evidence is moderate. Some claims lack high-trust backing. Consider verifying assumed items against official sources.")

    if coverage["research_depth"] < 30:
        lines.append("Research is shallow. Only surface-level information has been collected. Deepen analysis in key domains.")

    if synthesis["tradeoffs"]:
        lines.append(f"{len(synthesis['tradeoffs'])} unresolved tradeoff(s) detected. Run the Decision Engine to compare approaches.")

    if synthesis["anti_patterns"]:
        lines.append(f"{len(synthesis['anti_patterns'])} anti-pattern(s) identified. Review before proceeding to architecture.")

    if not lines:
        lines.append("Knowledge base is in good shape. Ready to proceed to architecture phase.")

    return " ".join(lines)
