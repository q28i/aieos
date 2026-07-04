# doc_system/sdk.py
"""
AIEOS SDK helper module for third-party package creators.
"""

def get_capability_templates(pkg_key, pkg_name, category):
    import json
    return {
        "skill.json": json.dumps({
            "name": pkg_name,
            "version": "1.0.0",
            "category": category,
            "requires": []
        }, indent=2),
        "workflow.md": f"# Workflow: {pkg_name}\n\n## Entry Requirements\n- Explicit inputs and target values.\n\n## Exit Requirements\n- Auditable outcome logs and verified outputs.\n",
        "persona.md": f"# Persona: {pkg_name}\n\n- Define core functional logic.\n",
        "tools.json": json.dumps({"allowed": [], "forbidden": []}, indent=2),
        "hooks/pre_run.py": "# Runtime executable hooks\n\ndef pre_execute(payload):\n    return payload\n"
    }
