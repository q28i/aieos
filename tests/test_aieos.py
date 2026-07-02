# tests/test_aieos.py
"""
Automated unit tests for the AIEOS command-line interface and package managers.
"""
import unittest
import tempfile
import shutil
import os
import sqlite3
from doc_system.cli import AIEOS_CLI

class TestAIEOSCLI(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for workspace tests
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.cli = AIEOS_CLI()

    def tearDown(self):
        # Restore cwd and remove temp directory
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_workspace(self):
        # Execute init command
        success = self.cli.execute(["init"])
        self.assertTrue(success)
        
        # Verify files and folders exist
        self.assertTrue(os.path.exists("aieos.json"))
        self.assertTrue(os.path.exists("workspace.yaml"))
        self.assertTrue(os.path.exists(".aieos"))
        self.assertTrue(os.path.exists("memory/aieos_local.db"))
        self.assertTrue(os.path.exists("packages"))
        self.assertTrue(os.path.exists("profiles"))
        self.assertTrue(os.path.exists("benchmarks"))
        self.assertTrue(os.path.exists("logs"))

    def test_create_package(self):
        # Initialize first
        self.cli.execute(["init"])
        
        # Execute package creation
        success = self.cli.execute(["create", "package", "FuzzyLogic", "Research"])
        self.assertTrue(success)
        
        # Verify template folders and files exist
        pkg_dir = "packages/Capability_FuzzyLogic"
        self.assertTrue(os.path.exists(os.path.join(pkg_dir, "manifest.yaml")))
        self.assertTrue(os.path.exists(os.path.join(pkg_dir, "Contract.md")))
        self.assertTrue(os.path.exists(os.path.join(pkg_dir, "Interfaces.md")))
        self.assertTrue(os.path.exists(os.path.join(pkg_dir, "runtime/hooks.py")))
        self.assertTrue(os.path.exists(os.path.join(pkg_dir, "adapters/claude.py")))

    def test_install_uninstall_package(self):
        self.cli.execute(["init"])
        
        # Install package
        success = self.cli.execute(["install", "@aieos/research"])
        self.assertTrue(success)
        self.assertTrue(os.path.exists("packages/Capability_Research"))
        
        # Check active capabilities list
        with open("workspace.yaml", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Capability_Research", content)
        
        # Remove package
        success = self.cli.execute(["remove", "@aieos/research"])
        self.assertTrue(success)
        self.assertFalse(os.path.exists("packages/Capability_Research"))

    def test_doctor_audit(self):
        self.cli.execute(["init"])
        
        # Doctor command check
        success = self.cli.execute(["doctor"])
        self.assertTrue(success)

    def test_profile_switch(self):
        self.cli.execute(["init"])
        
        # Switch profile
        success = self.cli.execute(["profile", "SoftwareEngineer"])
        self.assertTrue(success)
        
        # Verify profile is updated in workspace.yaml
        with open("workspace.yaml", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("SoftwareEngineer", content)

    def test_config_set(self):
        self.cli.execute(["init"])
        
        # Set config key
        success = self.cli.execute(["config", "custom_key", "custom_value"])
        self.assertTrue(success)
        
        # Verify updated key in aieos.json
        with open("aieos.json", "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("custom_key", data)
        self.assertIn("custom_value", data)

if __name__ == "__main__":
    unittest.main()
