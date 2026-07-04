"""
AIEOS Knowledge Engine

Collects, classifies, and organizes research from multiple authoritative sources.
Each research entry is tagged with trust_level, source_type, and relevance_score.

Trust Levels:
    Tier 1 - Official Documentation, Standards & RFCs
    Tier 2 - Peer-Reviewed Papers, Package Registries, Expert Benchmarks
    Tier 3 - Community Knowledge (GitHub, StackOverflow, Reddit, Blogs)
    Tier 4 - AI Inference (lowest trust, must cite sources)

Source Types:
    official_docs, rfc, paper, registry, benchmark, github, stackoverflow, blog, ai_inference
"""

import sqlite3
import json
import os
import re
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def init_knowledge_db(db_path):
    """Create the Knowledge Engine tables if they don't already exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS research_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        source_url TEXT,
        source_type TEXT,
        trust_level INTEGER,
        title TEXT,
        summary TEXT,
        raw_content TEXT,
        relevance_score REAL,
        collected_at TEXT,
        domain TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_map (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT,
        category TEXT,
        statement TEXT,
        evidence_ids TEXT,
        confidence REAL,
        last_updated TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tradeoffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT,
        option_a TEXT,
        option_b TEXT,
        dimensions TEXT,
        recommendation TEXT,
        rationale TEXT,
        evidence_ids TEXT
    )""")

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Trust-level classification
# ---------------------------------------------------------------------------

SOURCE_TRUST_MAP = {
    "official_docs": 1,
    "rfc":           1,
    "standard":      1,
    "paper":         2,
    "registry":      2,
    "benchmark":     2,
    "github":        3,
    "stackoverflow": 3,
    "reddit":        3,
    "blog":          3,
    "ai_inference":  4,
}


# ---------------------------------------------------------------------------
# Knowledge Engine
# ---------------------------------------------------------------------------

class KnowledgeEngine:
    """
    Collects, classifies, and organises research from multiple sources.
    Stores everything in the project's SQLite research database.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        init_knowledge_db(db_path)

    # ---- collection -------------------------------------------------------

    def collect(self, query, entries):
        """
        Persist a list of raw research entries into the database.

        Each entry in *entries* is a dict with at minimum:
            title, summary, source_url, source_type
        Optional: raw_content, relevance_score, domain
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()

        inserted_ids = []
        for entry in entries:
            source_type = entry.get("source_type", "ai_inference")
            trust_level = SOURCE_TRUST_MAP.get(source_type, 4)
            relevance   = entry.get("relevance_score", 0.5)
            domain      = entry.get("domain", "general")

            cursor.execute("""
                INSERT INTO research_entries
                    (query, source_url, source_type, trust_level,
                     title, summary, raw_content,
                     relevance_score, collected_at, domain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                query,
                entry.get("source_url", ""),
                source_type,
                trust_level,
                entry.get("title", ""),
                entry.get("summary", ""),
                entry.get("raw_content", ""),
                relevance,
                now,
                domain,
            ))
            inserted_ids.append(cursor.lastrowid)

        conn.commit()
        conn.close()
        return inserted_ids

    def get_entries(self, query=None, domain=None, min_trust=None):
        """Retrieve research entries with optional filters."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = "SELECT * FROM research_entries WHERE 1=1"
        params = []

        if query:
            sql += " AND query LIKE ?"
            params.append(f"%{query}%")
        if domain:
            sql += " AND domain = ?"
            params.append(domain)
        if min_trust is not None:
            sql += " AND trust_level <= ?"
            params.append(min_trust)

        sql += " ORDER BY trust_level ASC, relevance_score DESC"
        cursor.execute(sql, params)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    # ---- knowledge map ----------------------------------------------------

    def build_knowledge_map(self, project_id, entries=None):
        """
        Synthesise collected research entries into a Knowledge Map.

        Returns a dict with four categories:
            known        – statements backed by Tier-1/2 evidence
            unknown      – identified gaps requiring further research
            assumed      – statements based on Tier-3/4 evidence only
            contradicted – entries where sources disagree
        """
        if entries is None:
            entries = self.get_entries()

        knowledge = {
            "known":        [],
            "unknown":      [],
            "assumed":      [],
            "contradicted": [],
        }

        # Group by trust level
        high_trust = [e for e in entries if e["trust_level"] <= 2]
        low_trust  = [e for e in entries if e["trust_level"] > 2]

        # Detect contradictions – same domain, opposing summaries
        seen_domains = {}
        for entry in entries:
            d = entry.get("domain", "general")
            seen_domains.setdefault(d, []).append(entry)

        for domain, domain_entries in seen_domains.items():
            if len(domain_entries) > 1:
                summaries = [e["summary"].lower() for e in domain_entries if e.get("summary")]
                # Simple negation heuristic
                for i, s1 in enumerate(summaries):
                    for s2 in summaries[i + 1:]:
                        if _detect_contradiction(s1, s2):
                            knowledge["contradicted"].append({
                                "domain": domain,
                                "statement": f"Conflicting evidence in domain '{domain}'",
                                "entries": [e["id"] for e in domain_entries],
                            })

        # Classify entries
        for entry in high_trust:
            knowledge["known"].append({
                "statement": entry["summary"],
                "evidence_ids": [entry["id"]],
                "trust": entry["trust_level"],
                "source": entry["source_type"],
            })

        for entry in low_trust:
            knowledge["assumed"].append({
                "statement": entry["summary"],
                "evidence_ids": [entry["id"]],
                "trust": entry["trust_level"],
                "source": entry["source_type"],
            })

        # Persist to knowledge_map table
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()

        for category, items in knowledge.items():
            for item in items:
                stmt = item.get("statement", "")
                eids = json.dumps(item.get("evidence_ids", item.get("entries", [])))
                conf = 0.9 if category == "known" else (0.4 if category == "assumed" else 0.1)
                cursor.execute("""
                    INSERT INTO knowledge_map
                        (project_id, category, statement, evidence_ids, confidence, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (project_id, category, stmt, eids, conf, now))

        conn.commit()
        conn.close()
        return knowledge

    # ---- coverage scoring -------------------------------------------------

    def evaluate_coverage(self, domain=None):
        """
        Calculate multi-dimensional Evidence Profile scores.

        Returns dict:
            evidence_score          – % backed by Tier 1-2 sources
            knowledge_coverage      – % of identified topics researched
            research_depth          – average entries per topic
            contradiction_count     – number of unresolved conflicts
        """
        entries = self.get_entries(domain=domain)

        if not entries:
            return {
                "evidence_score": 0,
                "knowledge_coverage": 0,
                "research_depth": 0,
                "contradiction_count": 0,
            }

        total = len(entries)
        high_trust_count = sum(1 for e in entries if e["trust_level"] <= 2)
        evidence_score = int((high_trust_count / total) * 100) if total else 0

        # Count unique domains/topics covered
        domains_covered = set(e.get("domain", "general") for e in entries)
        # Rough heuristic: assume 10 core domains per project
        expected_domains = max(10, len(domains_covered))
        knowledge_coverage = int((len(domains_covered) / expected_domains) * 100)

        # Research depth = avg entries per domain
        depth_per_domain = total / max(1, len(domains_covered))
        # Normalise: 1 entry = shallow, 5+ = deep
        research_depth = int(min(100, (depth_per_domain / 5.0) * 100))

        # Count contradictions from knowledge_map
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM knowledge_map WHERE category = 'contradicted'")
        contradiction_count = cursor.fetchone()[0]
        conn.close()

        return {
            "evidence_score": min(100, evidence_score),
            "knowledge_coverage": min(100, knowledge_coverage),
            "research_depth": min(100, research_depth),
            "contradiction_count": contradiction_count,
        }


# ---------------------------------------------------------------------------
# Content quality analysis (for intelligent inspect)
# ---------------------------------------------------------------------------

def evaluate_readme_quality(readme_path):
    """
    Score a README against quality dimensions using heuristic content analysis.

    Returns dict of scores (0-100) for:
        problem_statement   – Has a clear problem description
        target_users        – Describes who this is for
        prerequisites       – Lists dependencies/constraints
        alternatives        – References existing solutions
        architecture        – Contains structural overview
        overall             – Weighted composite
    """
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return _empty_readme_scores()

    content_lower = content.lower()
    lines = content.split("\n")
    word_count = len(content.split())

    # --- Problem statement ---
    problem_keywords = ["problem", "motivation", "why", "purpose", "goal",
                        "objective", "challenge", "pain point", "gap"]
    problem_score = _keyword_density_score(content_lower, problem_keywords, base=20, per_hit=15, cap=95)
    # Bonus for having an actual "## Problem" or "## Motivation" section
    if re.search(r"^#{1,3}\s*(problem|motivation|why|purpose)", content_lower, re.MULTILINE):
        problem_score = min(95, problem_score + 25)

    # --- Target users ---
    user_keywords = ["user", "developer", "team", "audience", "for whom",
                     "use case", "persona", "stakeholder", "customer"]
    user_score = _keyword_density_score(content_lower, user_keywords, base=15, per_hit=18, cap=95)

    # --- Prerequisites ---
    prereq_keywords = ["require", "prerequisite", "dependency", "install",
                       "setup", "configuration", "environment", "node", "python",
                       "docker", "database"]
    prereq_score = _keyword_density_score(content_lower, prereq_keywords, base=10, per_hit=12, cap=95)
    # Bonus for code blocks (installation instructions)
    code_block_count = content.count("```")
    prereq_score = min(95, prereq_score + code_block_count * 5)

    # --- Alternatives ---
    alt_keywords = ["alternative", "existing", "competitor", "comparison",
                    "similar", "inspired by", "unlike", "compared to",
                    "vs", "versus"]
    alt_score = _keyword_density_score(content_lower, alt_keywords, base=5, per_hit=20, cap=95)

    # --- Architecture ---
    arch_keywords = ["architecture", "design", "component", "module", "layer",
                     "service", "api", "interface", "diagram", "flow",
                     "structure", "system"]
    arch_score = _keyword_density_score(content_lower, arch_keywords, base=10, per_hit=12, cap=95)
    # Bonus for mermaid diagrams or images
    if "```mermaid" in content_lower or "![" in content:
        arch_score = min(95, arch_score + 20)

    # --- Overall (weighted) ---
    overall = int(
        problem_score * 0.30 +
        user_score * 0.15 +
        prereq_score * 0.15 +
        alt_score * 0.20 +
        arch_score * 0.20
    )

    # Length penalty: very short READMEs can't be comprehensive
    if word_count < 50:
        overall = min(overall, 25)
    elif word_count < 150:
        overall = min(overall, 55)

    return {
        "problem_statement": problem_score,
        "target_users": user_score,
        "prerequisites": prereq_score,
        "alternatives": alt_score,
        "architecture": arch_score,
        "overall": overall,
        "word_count": word_count,
    }


def evaluate_test_quality(test_dir):
    """
    Score the testing strategy beyond folder existence.

    Returns dict with:
        file_count        – number of test files found
        has_integration   – whether integration tests exist
        has_unit          – whether unit tests exist
        framework_detected – detected test framework name
        coverage_indicator – rough heuristic of coverage breadth
        overall           – composite score 0-100
    """
    if not os.path.exists(test_dir):
        return {"file_count": 0, "has_integration": False, "has_unit": False,
                "framework_detected": None, "coverage_indicator": 0, "overall": 0}

    test_files = []
    for root, dirs, files in os.walk(test_dir):
        for f in files:
            if f.endswith((".py", ".js", ".ts", ".go", ".rs", ".java")):
                test_files.append(os.path.join(root, f))

    file_count = len(test_files)
    has_integration = any("integration" in f.lower() or "e2e" in f.lower() for f in test_files)
    has_unit = any("unit" in f.lower() or f.startswith("test_") or f.endswith("_test.py") for f in test_files)

    # Detect framework
    framework = None
    all_content = ""
    for tf in test_files[:10]:  # Sample first 10
        try:
            with open(tf, "r", encoding="utf-8") as fh:
                all_content += fh.read()
        except Exception:
            pass

    if "pytest" in all_content or "import pytest" in all_content:
        framework = "pytest"
    elif "unittest" in all_content:
        framework = "unittest"
    elif "jest" in all_content or "describe(" in all_content:
        framework = "jest"
    elif "mocha" in all_content:
        framework = "mocha"

    # Coverage indicator: count unique assert/expect statements
    assert_count = all_content.lower().count("assert") + all_content.lower().count("expect(")
    coverage_indicator = min(100, int((assert_count / max(1, file_count)) * 10))

    # Overall
    overall = 0
    if file_count > 0:
        overall += 30
    if file_count > 3:
        overall += 15
    if has_unit:
        overall += 15
    if has_integration:
        overall += 20
    if framework:
        overall += 10
    overall += min(10, coverage_indicator // 10)
    overall = min(100, overall)

    return {
        "file_count": file_count,
        "has_integration": has_integration,
        "has_unit": has_unit,
        "framework_detected": framework,
        "coverage_indicator": coverage_indicator,
        "overall": overall,
    }


def evaluate_security_posture(workspace_root):
    """
    Evaluate security beyond .env.example existence.

    Checks:
        - .env.example exists (credential schema)
        - No hardcoded secrets in source files
        - .gitignore excludes sensitive files
        - Dependency audit markers exist
    """
    scores = {
        "credential_schema": 0,
        "no_hardcoded_secrets": 100,  # Start high, deduct if found
        "gitignore_coverage": 0,
        "dependency_audit": 0,
        "overall": 0,
    }

    # Credential schema
    if os.path.exists(os.path.join(workspace_root, ".env.example")):
        scores["credential_schema"] = 90
    elif os.path.exists(os.path.join(workspace_root, "security.json")):
        scores["credential_schema"] = 70

    # Scan for hardcoded secrets (simple heuristic)
    secret_patterns = [
        r'(?:api[_-]?key|secret|password|token)\s*[=:]\s*["\'][^"\']{8,}["\']',
        r'sk_live_[a-zA-Z0-9]{20,}',
        r'AKIA[A-Z0-9]{16}',
    ]
    source_extensions = (".py", ".js", ".ts", ".go", ".rs", ".java", ".env")
    violations = 0

    for root, dirs, files in os.walk(workspace_root):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in {
            "node_modules", ".git", "__pycache__", ".venv", "venv",
            ".aieos", "AIEOS", ".github"
        }]
        depth = root[len(workspace_root):].count(os.sep)
        if depth > 3:
            continue
        for fname in files:
            if not fname.endswith(source_extensions):
                continue
            if fname == ".env.example":
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                for pattern in secret_patterns:
                    violations += len(re.findall(pattern, content, re.IGNORECASE))
            except Exception:
                pass

    if violations > 0:
        scores["no_hardcoded_secrets"] = max(0, 100 - violations * 25)

    # .gitignore coverage
    gitignore_path = os.path.join(workspace_root, ".gitignore")
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                gi = f.read().lower()
            sensitive_patterns = [".env", "*.pem", "*.key", "credentials", "secret"]
            matches = sum(1 for p in sensitive_patterns if p in gi)
            scores["gitignore_coverage"] = int((matches / len(sensitive_patterns)) * 100)
        except Exception:
            pass

    # Dependency audit markers
    dep_audit_markers = ["package-lock.json", "yarn.lock", "Pipfile.lock",
                         "poetry.lock", "Cargo.lock", "go.sum"]
    for marker in dep_audit_markers:
        if os.path.exists(os.path.join(workspace_root, marker)):
            scores["dependency_audit"] = 80
            break

    scores["overall"] = int(
        scores["credential_schema"] * 0.25 +
        scores["no_hardcoded_secrets"] * 0.35 +
        scores["gitignore_coverage"] * 0.20 +
        scores["dependency_audit"] * 0.20
    )

    return scores


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _keyword_density_score(text, keywords, base=10, per_hit=15, cap=95):
    """Score based on keyword presence in text."""
    hits = sum(1 for k in keywords if k in text)
    return min(cap, base + hits * per_hit)


def _detect_contradiction(s1, s2):
    """Very simple heuristic for detecting contradicting summaries."""
    negation_pairs = [
        ("recommended", "not recommended"),
        ("fast", "slow"),
        ("secure", "insecure"),
        ("scalable", "not scalable"),
        ("better", "worse"),
        ("advantage", "disadvantage"),
        ("should", "should not"),
    ]
    for pos, neg in negation_pairs:
        if (pos in s1 and neg in s2) or (neg in s1 and pos in s2):
            return True
    return False


def _empty_readme_scores():
    return {
        "problem_statement": 0,
        "target_users": 0,
        "prerequisites": 0,
        "alternatives": 0,
        "architecture": 0,
        "overall": 0,
        "word_count": 0,
    }
