# doc_system/validator.py
"""
Validator and verification engine for AIEOS specifications.
Validates schemas, links, and builds AIEOS/README.md dynamically.
"""
import os
from doc_system.registry import AIEOS_REGISTRY

def build_aieos_readme(output_root):
    readme_path = os.path.join(output_root, "README.md")
    print(f"Building system index README: {readme_path}")
    
    header = """# AIEOS (Human Intelligence Amplification Runtime)

**AIEOS is a Human Intelligence Amplification Runtime. It augments AI models with modular cognitive capabilities whose primary objective is to strengthen human thinking rather than merely generate answers. Every interaction should improve the user's understanding, expand their knowledge, expose hidden assumptions, identify better alternatives, anticipate future consequences, and transform raw ideas into robust, evidence-based systems. Success is measured not by how quickly the AI responds, but by how much the human's vision, reasoning, and final decisions improve through the collaboration.**

AIEOS exists to ensure that every important conversation makes both participants better: the AI becomes more informed through structured context, and the human becomes more informed through structured knowledge. The output is not merely an answer—it is an improved way of thinking.

---

## Directory Architecture

- **`AIEOS_SPECIFICATION.md`**: [System Specification RFC](file:///{output_root_url}/AIEOS_SPECIFICATION.md) defining engine lifecycles, memory, event, and capability injection schemas.
- **`RFC_0010_COLLABORATIVE_INTELLIGENCE_PROTOCOL.md`**: [RFC-0010: Collaborative Intelligence Protocol](file:///{output_root_url}/RFC_0010_COLLABORATIVE_INTELLIGENCE_PROTOCOL.md) specifying human-AI collaboration loops, assumption matrices, and dialogue strategy pacing.
- **`CONSTITUTION/`**: Immutable guidelines that govern overall AI behaviors and standards.
- **`CAPABILITIES/`**: Model-independent capability packages containing manifests, contract rules, and cognitive effects mapping.
- **`PROFILES/`**: Composition configs defining capability stacks and dialogue styles for specific roles.
- **`ENGINES/`**: Subsystem engines orchestrating scheduler tasks, memory, events, and validation.

---

## Active System Modules

### 🛡️ Core Constitutions
""".replace("{output_root_url}", output_root.replace('\\', '/'))
    
    constitutions = []
    capabilities = []
    profiles = []
    engines = []
    
    for key in sorted(AIEOS_REGISTRY.keys()):
        spec = AIEOS_REGISTRY[key]
        doc_type = spec["type"]
        
        if doc_type == "CONSTITUTION":
            filename = f"{key.replace('Constitution_', '')}.md"
            rel_path = f"CONSTITUTION/{filename}"
            link = f"[{spec['name']}](file:///{output_root.replace('\\', '/')}/{rel_path})"
            constitutions.append(f"- {link}: {spec['purpose']}")
            
        elif doc_type == "CAPABILITY":
            category = spec["category"]
            cap_name = key.replace('Capability_', '')
            rel_path = f"CAPABILITIES/{category}/{cap_name}/workflow.md"
            link = f"[{spec['name']} Workflow](file:///{output_root.replace('\\', '/')}/{rel_path})"
            capabilities.append(f"- {link} (Package: [CAPABILITIES/{category}/{cap_name}](file:///{output_root.replace('\\', '/')}/CAPABILITIES/{category}/{cap_name}/)): {spec['purpose']}")
            
        elif doc_type in ["SERVICE", "PROTOCOL", "POLICY"]:
            if doc_type == "SERVICE":
                filename = f"{key.replace('Service_', '')}.md"
                rel_path = f"SERVICES/{filename}"
                section = "Core Service"
            elif doc_type == "PROTOCOL":
                filename = f"{key.replace('Protocol_', '')}.md"
                rel_path = f"PROTOCOLS/{filename}"
                section = "Cognitive Protocol"
            else:
                filename = f"{key.replace('Policy_', '')}.md"
                rel_path = f"POLICIES/{filename}"
                section = "Learning Policy"
            
            link = f"[{spec['name']}](file:///{output_root.replace('\\', '/')}/{rel_path})"
            engines.append(f"- {link} ({section}): {spec['purpose']}")
            
        elif doc_type == "PROFILE":
            filename = f"{key.replace('Profile_', '')}.yaml"
            rel_path = f"PROFILES/{filename}"
            link = f"[{spec['name']}](file:///{output_root.replace('\\', '/')}/{rel_path})"
            profiles.append(f"- {link}: {spec['purpose']}")
            
    content = (
        header + 
        "\n".join(constitutions) + 
        "\n\n### 🧠 Active Capability Contracts\n" + 
        "\n".join(capabilities) + 
        "\n\n### 👤 Active Profile Configurations\n" + 
        "\n".join(profiles) + 
        "\n\n### ⚙️ Cognitive Modules (Services, Protocols, Policies)\n" + 
        "\n".join(engines) + 
        "\n"
    )
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("AIEOS system README index built successfully.")

def validate_aieos_system(output_root):
    print("Starting validation of AIEOS system...")
    errors = []
    
    for key, spec in AIEOS_REGISTRY.items():
        doc_type = spec["type"]
        
        if doc_type == "CONSTITUTION":
            target_path = os.path.join(output_root, "CONSTITUTION", f"{key.replace('Constitution_', '')}.md")
            if not os.path.exists(target_path):
                errors.append(f"Missing file: {target_path} is registered but not found on disk.")
                continue
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "# " not in content or "## Purpose" not in content or "## Immutable Principles" not in content:
                errors.append(f"Format anomaly: Constitution '{target_path}' lacks immutable/purpose headers.")
                
        elif doc_type == "CAPABILITY":
            category = spec["category"]
            cap_name = key.replace("Capability_", "")
            cap_dir = os.path.join(output_root, "CAPABILITIES", category, cap_name)
            
            # Sub-package checklist
            files_to_check = ["skill.json", "persona.md", "workflow.md", "triggers.json", "questions.json", "tools.json", "memory.json"]
            for f_name in files_to_check:
                p = os.path.join(cap_dir, f_name)
                if not os.path.exists(p):
                    errors.append(f"Missing capability file: {p} is required under execution specification.")
                    
            skill_json_path = os.path.join(cap_dir, "skill.json")
            if not os.path.exists(skill_json_path):
                errors.append(f"Missing capability manifest: {skill_json_path} is required.")
            else:
                import json
                try:
                    with open(skill_json_path, "r", encoding="utf-8") as f:
                        skill_data = json.load(f)
                    if not skill_data.get("name") or not skill_data.get("version"):
                        errors.append(f"Manifest anomaly: {skill_json_path} lacks name/version attributes.")
                    if skill_data.get("maturity") not in ["Draft", "Experimental", "Validated", "Production", "Optimized", "Autonomous"]:
                        errors.append(f"Manifest anomaly: {skill_json_path} contains invalid maturity level '{skill_data.get('maturity')}'")
                except Exception as e:
                    errors.append(f"Failed to parse skill.json at {skill_json_path}: {e}")
                    
            # Check related capability dependencies
            for rs in spec.get("related_capabilities", []):
                if rs not in AIEOS_REGISTRY:
                    errors.append(f"Broken link in related capabilities: '{key}' links to non-existent capability '{rs}'")
                    
        elif doc_type in ["SERVICE", "PROTOCOL", "POLICY"]:
            if doc_type == "SERVICE":
                folder_name = "SERVICES"
                filename = f"{key.replace('Service_', '')}.md"
            elif doc_type == "PROTOCOL":
                folder_name = "PROTOCOLS"
                filename = f"{key.replace('Protocol_', '')}.md"
            else:
                folder_name = "POLICIES"
                filename = f"{key.replace('Policy_', '')}.md"
                
            target_path = os.path.join(output_root, folder_name, filename)
            if not os.path.exists(target_path):
                errors.append(f"Missing file: {target_path} is registered but not found on disk.")
                continue
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "# " not in content or "## Purpose" not in content or "## Operational Loop Workflow" not in content:
                errors.append(f"Format anomaly: Module '{target_path}' lacks operational/purpose headers.")
                
        elif doc_type == "PROFILE":
            profile_name = key.replace("Profile_", "")
            target_path = os.path.join(output_root, "PROFILES", f"{profile_name}.yaml")
            if not os.path.exists(target_path):
                errors.append(f"Missing file: {target_path} is registered but not found on disk.")
                continue
            with open(target_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            has_capabilities = False
            has_dialogue_style = False
            for line in lines:
                if "capabilities:" in line:
                    has_capabilities = True
                if "dialogue_style:" in line:
                    has_dialogue_style = True
            if not has_capabilities:
                errors.append(f"Profile anomaly: {target_path} is missing capabilities key list.")
            if not has_dialogue_style:
                errors.append(f"Profile anomaly: {target_path} is missing dialogue_style configuration.")

    # Validate RFC-0010 exists
    rfc10_file = os.path.join(output_root, "RFC_0010_COLLABORATIVE_INTELLIGENCE_PROTOCOL.md")
    if not os.path.exists(rfc10_file):
        errors.append(f"Missing file: {rfc10_file} is required for Collaborative Intelligence loops.")
                
    if errors:
        print("AIEOS Validation failed with the following errors:")
        for err in errors:
            print(f"- {err}")
        return False
        
    print("AIEOS Validation passed successfully! No errors found.")
    return True
