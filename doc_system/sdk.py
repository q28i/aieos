# doc_system/sdk.py
"""
AIEOS SDK helper module for third-party package creators.
"""

def get_capability_templates(pkg_key, pkg_name, category):
    return {
        "manifest.yaml": f"name: {pkg_key}\nversion: 1.4.0\nmaturity: Draft\ncategory: {category}\n",
        "Contract.md": f"# Capability Contract: {pkg_name}\n\n## Entry Requirements\n- Explicit inputs and target values.\n\n## Exit Requirements\n- Auditable outcome logs and verified outputs.\n",
        "Interfaces.md": f"# Interfaces: {pkg_name}\n\n- execute(payload: dict) -> dict\n",
        "Responsibilities.md": f"# Responsibilities: {pkg_name}\n\n- Define core functional logic.\n",
        "Metrics.md": f"# Metrics: {pkg_name}\n\n- execution_latency_ms\n- success_rate\n",
        "Benchmarks.md": f"# Benchmarks: {pkg_name}\n\n- target_accuracy_rating\n",
        "FailureModes.md": f"# Failure Modes: {pkg_name}\n\n- Input malformation bounds.\n",
        "Evolution.md": f"# Evolution: {pkg_name}\n\n- Incremental versioning policies.\n",
        "runtime/hooks.py": "# Runtime executable hooks\n\ndef pre_execute(payload):\n    return payload\n\ndef post_execute(result):\n    return result\n",
        "adapters/claude.py": "# Claude adapter adapter mappings\n\ndef adapt_input(payload):\n    return payload\n",
        "adapters/gemini.py": "# Gemini adapter mappings\n\ndef adapt_input(payload):\n    return payload\n"
    }
