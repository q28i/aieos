# doc_system/adapter.py
"""
AIEOS Client Adapter and IDE hook wrapper interface.
Exposes capability orchestration interfaces to external AI frameworks.
"""
import os
import json
import sqlite3

class AIEOSAdapter:
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "memory", "aieos_local.db")

    def has_db(self):
        return os.path.exists(self.db_path)

    def log_decision_contract(self, contract):
        """
        Logs a Decision Contract to the local SQLite DB registry.
        """
        if not self.has_db():
            return False
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO decisions (
                decision_text, objective, success_criteria, constraints, 
                values_discovered, reversibility, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                contract.get("decision", ""),
                contract.get("objective", ""),
                contract.get("success_criteria", ""),
                json.dumps(contract.get("constraints", {})),
                json.dumps(contract.get("values", {})),
                contract.get("reversibility", "Type-2"),
                str(contract.get("confidence", {}))
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AIEOS Adapter] Warning: Could not log decision contract: {e}")
            return False

    def check_disagreement(self, user_assumption, evidence_favors_alt, silent_cost_high, objective_aligned):
        """
        Calculates Disagreement Protocol veto check.
        """
        should_disagree = (
            user_assumption and 
            evidence_favors_alt and 
            silent_cost_high and 
            objective_aligned
        )
        return should_disagree

    def calculate_split_confidence(self, evidence_val, reasoning_val, prediction_val, execution_val):
        """
        Calculates split confidence profiles.
        """
        return {
            "evidence_confidence": evidence_val,
            "reasoning_confidence": reasoning_val,
            "prediction_confidence": prediction_val,
            "execution_confidence": execution_val
        }

    def record_experience_lesson(self, lesson, pattern):
        """
        Records a new Lesson and Pattern inside the experience memory graph database.
        """
        if not self.has_db():
            return False
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO lessons (lesson, pattern) VALUES (?, ?)", (lesson, pattern))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AIEOS Adapter] Warning: Could not log experience loop: {e}")
            return False
