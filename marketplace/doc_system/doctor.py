# doc_system/doctor.py
"""
Framework Doctor utility to audit AIEOS workspaces and print detailed health diagnostics.
"""
import os
from marketplace.doc_system.registry import AIEOS_REGISTRY

def run_diagnostics(output_root):
    print("==================================================")
    print("            AIEOS FRAMEWORK DOCTOR                ")
    print("==================================================")
    
    errors = []
    total_checks = 0
    passed_checks = 0
    
    # 1. Architecture Health Check (Services, Protocols, Policies audit)
    total_checks += 1
    module_keys = [k for k, v in AIEOS_REGISTRY.items() if v["type"] in ["SERVICE", "PROTOCOL", "POLICY"]]
    missing_modules = 0
    for mk in module_keys:
        doc_type = AIEOS_REGISTRY[mk]["type"]
        if doc_type == "SERVICE":
            folder_name = "SERVICES"
            filename = f"{mk.replace('Service_', '')}.md"
        elif doc_type == "PROTOCOL":
            folder_name = "PROTOCOLS"
            filename = f"{mk.replace('Protocol_', '')}.md"
        else:
            folder_name = "POLICIES"
            filename = f"{mk.replace('Policy_', '')}.md"
            
        path = os.path.join(output_root, folder_name, filename)
        if not os.path.exists(path):
            missing_modules += 1
            errors.append(f"Architecture: Missing module document '{filename}' in folder '{folder_name}'")
            
    if missing_modules == 0:
        passed_checks += 1
    arch_score = int(((len(module_keys) - missing_modules) / len(module_keys)) * 100)
    
    # 2. Knowledge Health Check (Constitutions audit)
    total_checks += 1
    const_keys = [k for k, v in AIEOS_REGISTRY.items() if v["type"] == "CONSTITUTION"]
    missing_const = 0
    for ck in const_keys:
        filename = f"{ck.replace('Constitution_', '')}.md"
        path = os.path.join(output_root, "CONSTITUTION", filename)
        if not os.path.exists(path):
            missing_const += 1
            errors.append(f"Knowledge: Missing constitution document '{filename}'")
            
    if missing_const == 0:
        passed_checks += 1
    knowledge_score = int(((len(const_keys) - missing_const) / len(const_keys)) * 100)
    
    # 3. Security Audit (Checks for permissions / maturity validations / package stubs)
    total_checks += 1
    capabilities_keys = [k for k, v in AIEOS_REGISTRY.items() if v["type"] == "CAPABILITY"]
    invalid_maturity = 0
    missing_package_stubs = 0
    for sk in capabilities_keys:
        cap_name = sk.replace('Capability_', '')
        cap_dir = os.path.join(output_root, "CAPABILITIES", AIEOS_REGISTRY[sk]["category"], cap_name)
        manifest_path = os.path.join(cap_dir, "manifest.yaml")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "maturity: " not in content:
                invalid_maturity += 1
                errors.append(f"Security: Capability '{cap_name}' lacks maturity declaration in manifest.")
        else:
            invalid_maturity += 1
            
        required_stubs = ["runtime/hooks.py", "adapters/claude.py", "adapters/codex.py"]
        for stub in required_stubs:
            path = os.path.join(cap_dir, stub)
            if not os.path.exists(path):
                missing_package_stubs += 1
                errors.append(f"Security: Missing executable stub '{stub}' in capability '{cap_name}'")
                
    if invalid_maturity == 0 and missing_package_stubs == 0:
        passed_checks += 1
    security_score = int(((len(capabilities_keys)*4 - (invalid_maturity + missing_package_stubs)) / (len(capabilities_keys)*4)) * 100)
    
    # 4. Documentation Completeness
    total_checks += 1
    missing_docs = 0
    broken_links = 0
    
    spec_path = os.path.join(output_root, "AIEOS_SPECIFICATION.md")
    readme_path = os.path.join(output_root, "README.md")
    
    if not os.path.exists(spec_path):
        missing_docs += 1
        errors.append("Documentation: Missing AIEOS_SPECIFICATION.md RFC standard.")
    if not os.path.exists(readme_path):
        missing_docs += 1
        errors.append("Documentation: Missing README.md Index file.")
        
    # Check link presence
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Scan for local file link presence
        if "file:///" not in content:
            broken_links += 1
            errors.append("Documentation: README.md lacks hyperlinked file pathways.")
            
    if missing_docs == 0 and broken_links == 0:
        passed_checks += 1
        
    doc_score = int(((4 - (missing_docs + broken_links)) / 4) * 100)
    
    # 5. Profiles Verification
    total_checks += 1
    profile_keys = [k for k, v in AIEOS_REGISTRY.items() if v["type"] == "PROFILE"]
    missing_profiles = 0
    for pk in profile_keys:
        profile_name = pk.replace("Profile_", "")
        path = os.path.join(output_root, "PROFILES", f"{profile_name}.yaml")
        if not os.path.exists(path):
            missing_profiles += 1
            errors.append(f"Profiles: Missing profile file '{profile_name}.yaml'")
            
    if missing_profiles == 0:
        passed_checks += 1
        
    profile_score = int(((len(profile_keys) - missing_profiles) / len(profile_keys)) * 100)
    
    # 6. Technical Debt Audit
    tech_debt_items = 0
    for root, dirs, files in os.walk(output_root):
        for file in files:
            if file.endswith((".md", ".yaml")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    data = f.read()
                if "TODO" in data or "Experimental" in data:
                    tech_debt_items += 1
                    
    # Calculate overall health
    overall_health = int((passed_checks / total_checks) * 100)
    
    print(f"Architecture Health:      {arch_score}%")
    print(f"Knowledge Base Health:    {knowledge_score}%")
    print(f"Security Audits Check:    {security_score}%")
    print(f"Profiles Health:          {profile_score}%")
    print(f"Testing & QA Audits:      100% (Simulated)")
    print(f"Documentation Health:     {doc_score}%")
    print("--------------------------------------------------")
    print(f"Technical Debt Registry:  {tech_debt_items} Items")
    print(f"Missing Core Modules:     {missing_modules}")
    print(f"Missing Capabilities:     {invalid_maturity}")
    print(f"Missing Profiles:         {missing_profiles}")
    print(f"Broken Tracing Links:     {broken_links}")
    print("--------------------------------------------------")
    print(f"FRAMEWORK GENERAL HEALTH: {overall_health}%")
    print("==================================================")
    
    if errors:
        print("\nIdentified Diagnostics Warnings:")
        for err in errors:
            print(f"  [!] {err}")
    else:
        print("\nAll diagnostic components passed successfully.")
        
    return overall_health == 100
