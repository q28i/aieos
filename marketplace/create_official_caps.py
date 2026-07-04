# marketplace/create_official_caps.py
import os
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAPS_DIR = os.path.join(ROOT, "official-capabilities")

# Core capabilities definition
CAPABILITIES = {
    "research": {
        "name": "Capability_Research",
        "category": "Research",
        "version": "1.4.0",
        "purpose": "General research and statistical analysis capability package.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["research", "analytics", "analysis"],
        "supports": ["research", "planning"],
        "project_types": ["computation_engine", "data_science", "saas", "library"]
    },
    "testing": {
        "name": "Capability_Testing",
        "category": "Quality",
        "version": "1.4.0",
        "purpose": "QA execution and validation capabilities.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["testing", "quality", "ci/cd"],
        "supports": ["verification", "validation"],
        "project_types": ["saas", "library", "backend"]
    },
    "trading": {
        "name": "Capability_Trading",
        "category": "Finance",
        "version": "1.4.0",
        "purpose": "Autonomous trading engine and simulation tools.",
        "dependencies": ["Capability_Research", "Capability_Risk"],
        "tags": ["trading", "quant", "exchange", "portfolio"],
        "supports": ["execution", "research"],
        "project_types": ["trading_bot", "fintech"]
    },
    "risk": {
        "name": "Capability_Risk",
        "category": "Risk",
        "version": "1.4.0",
        "purpose": "Exposure monitoring and risk controllers.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["risk", "drawdown", "exposure", "position-sizing"],
        "supports": ["planning", "execution"],
        "project_types": ["trading_bot", "fintech"]
    },
    "security": {
        "name": "Capability_Security",
        "category": "Security",
        "version": "1.4.0",
        "purpose": "Auditing and credential security rules.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["security", "auth", "jwt", "rate-limiting"],
        "supports": ["auditing", "verification"],
        "project_types": ["saas", "backend", "computation_engine"]
    },
    "datapipeline": {
        "name": "Capability_Datapipeline",
        "category": "Data",
        "version": "1.4.0",
        "purpose": "Data pipeline and database streams management.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["database", "postgres", "sql", "ingest", "pipeline"],
        "supports": ["data", "architecture"],
        "project_types": ["computation_engine", "saas", "backend"]
    },
    "performance": {
        "name": "Capability_Performance",
        "category": "Performance",
        "version": "1.4.0",
        "purpose": "Performance audit and caching optimization mechanisms.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["performance", "bottleneck", "cache", "indexing"],
        "supports": ["architecture", "verification"],
        "project_types": ["saas", "backend"]
    },
    "validation": {
        "name": "Capability_Validation",
        "category": "Quality",
        "version": "1.4.0",
        "purpose": "Validation and compliance gate checks.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["validation", "constraints", "audit", "compliance"],
        "supports": ["planning", "execution"],
        "project_types": ["computation_engine", "data_science"]
    },
    "memory": {
        "name": "Capability_Memory",
        "category": "Memory",
        "version": "1.4.0",
        "purpose": "Context graph database memory adapter.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["memory", "graph", "sqlite", "context"],
        "supports": ["data", "planning"],
        "project_types": ["saas", "ai_agent", "computation_engine"]
    },
    "docs": {
        "name": "Capability_Docs",
        "category": "Documentation",
        "version": "1.4.0",
        "purpose": "Documentation and standards compile helper.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["docs", "standards", "compile"],
        "supports": ["documentation"],
        "project_types": ["saas", "library", "ai_agent"]
    },
    "robotics": {
        "name": "Capability_Robotics",
        "category": "Hardware",
        "version": "1.4.0",
        "purpose": "Robotics control, kinematic solvers, and driver interfaces.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["robotics", "kinematics", "driver", "hardware"],
        "supports": ["execution", "planning"],
        "project_types": ["robotics", "embedded"]
    },
    "compiler": {
        "name": "Capability_Compiler",
        "category": "Development",
        "version": "1.4.0",
        "purpose": "AST traversal, parsers, and custom code generation capabilities.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["compiler", "ast", "parser", "codegen"],
        "supports": ["architecture", "implementation"],
        "project_types": ["compiler", "library"]
    },
    "ecommerce": {
        "name": "Capability_Ecommerce",
        "category": "Business",
        "version": "1.4.0",
        "purpose": "Cart flows, payment integrations, and catalog management.",
        "dependencies": ["Capability_BaseCognitive"],
        "tags": ["ecommerce", "payments", "cart", "business"],
        "supports": ["execution", "business"],
        "project_types": ["saas", "ecommerce"]
    }
}

def scaffold():
    os.makedirs(CAPS_DIR, exist_ok=True)
    for cap_id, info in CAPABILITIES.items():
        cap_path = os.path.join(CAPS_DIR, cap_id)
        os.makedirs(cap_path, exist_ok=True)
        os.makedirs(os.path.join(cap_path, "hooks"), exist_ok=True)
        os.makedirs(os.path.join(cap_path, "examples"), exist_ok=True)
        
        # 1. skill.json
        skill = {
            "name": info["name"],
            "version": info["version"],
            "description": info["purpose"],
            "category": info["category"],
            "requires": info["dependencies"],
            "tags": info["tags"],
            "supports": info["supports"],
            "project_types": info["project_types"],
            "maturity": "Validated"
        }
        with open(os.path.join(cap_path, "skill.json"), "w", encoding="utf-8") as f:
            json.dump(skill, f, indent=2)
            
        # 2. persona.md
        with open(os.path.join(cap_path, "persona.md"), "w", encoding="utf-8") as f:
            f.write(f"# {info['name']} Persona\n\n{info['purpose']}\n")
            
        # 3. workflow.md
        with open(os.path.join(cap_path, "workflow.md"), "w", encoding="utf-8") as f:
            f.write(f"# {info['name']} Workflow\n\n1. Define input objectives.\n2. Perform analysis.\n3. Validate outputs.\n")
            
        # 4. JSONs
        with open(os.path.join(cap_path, "triggers.json"), "w", encoding="utf-8") as f:
            json.dump({"triggers": info["tags"]}, f, indent=2)
        with open(os.path.join(cap_path, "questions.json"), "w", encoding="utf-8") as f:
            json.dump({"questions": []}, f, indent=2)
        with open(os.path.join(cap_path, "tools.json"), "w", encoding="utf-8") as f:
            json.dump({"allowed": ["python", "bash"], "forbidden": []}, f, indent=2)
        with open(os.path.join(cap_path, "memory.json"), "w", encoding="utf-8") as f:
            json.dump({"context": []}, f, indent=2)
            
        # 5. hooks/pre_run.py
        with open(os.path.join(cap_path, "hooks", "pre_run.py"), "w", encoding="utf-8") as f:
            f.write("def run():\n    pass\n")
            
        # 6. examples/example_1.md
        with open(os.path.join(cap_path, "examples", "example_1.md"), "w", encoding="utf-8") as f:
            f.write("# Example Scenario\n\nSimple mock run scenario.\n")
            
        print(f"Scaffolded capability: {info['name']} in {cap_path}")

if __name__ == "__main__":
    scaffold()
