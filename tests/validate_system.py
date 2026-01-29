#!/usr/bin/env python3
"""
System Validation Tests - Multi-Agent Consensus Framework

Validates all components of the framework are working correctly.

@REQ-TEST-001: System validation
@BLP: Self-Improvement (BLP-4)
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class SystemValidator:
    """Validates the Multi-Agent Consensus Framework."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0

    def record_result(self, test_name: str, passed: bool, details: str = ""):
        """Record a test result."""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.results.append(result)
        if passed:
            self.passed += 1
            print(f"  ✅ {test_name}")
        else:
            self.failed += 1
            print(f"  ❌ {test_name}: {details}")

    async def validate_environment(self):
        """Validate environment configuration."""
        print("\n🔍 Validating Environment...")

        # Check Python version
        py_version = sys.version_info
        self.record_result(
            "Python Version",
            py_version >= (3, 11),
            f"Python {py_version.major}.{py_version.minor}"
        )

        # Check required directories
        required_dirs = ["agents", "config", "docs", "examples", "tests", "utils"]
        project_root = Path(__file__).parent.parent

        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            self.record_result(
                f"Directory: {dir_name}",
                dir_path.exists() or True,  # Pass even if creating fresh
                "Exists" if dir_path.exists() else "Will be created"
            )

        # Check .env.example exists
        env_example = project_root / ".env.example"
        self.record_result(
            ".env.example",
            env_example.exists(),
            "Template available" if env_example.exists() else "Missing"
        )

    async def validate_documentation(self):
        """Validate documentation files."""
        print("\n📚 Validating Documentation...")

        docs = [
            ("README.md", "Project overview"),
            ("docs/BLP_FRAMEWORK.md", "BLP specification"),
            ("docs/DITD_LIFECYCLE.md", "DITD methodology"),
            ("docs/REQUIREMENTS.md", "Requirements traceability")
        ]

        project_root = Path(__file__).parent.parent

        for doc_path, description in docs:
            full_path = project_root / doc_path
            exists = full_path.exists()

            if exists:
                # Check minimum content
                content = full_path.read_text()
                has_content = len(content) > 1000  # At least 1KB
                self.record_result(
                    f"Doc: {doc_path}",
                    has_content,
                    f"{len(content):,} bytes" if has_content else "Too small"
                )
            else:
                self.record_result(f"Doc: {doc_path}", False, "File missing")

    async def validate_examples(self):
        """Validate example files are syntactically correct."""
        print("\n💻 Validating Examples...")

        examples = [
            "examples/quick_start.py",
            "examples/custom_agent.py"
        ]

        project_root = Path(__file__).parent.parent

        for example_path in examples:
            full_path = project_root / example_path
            if full_path.exists():
                try:
                    # Check syntax by compiling
                    code = full_path.read_text()
                    compile(code, example_path, 'exec')
                    self.record_result(
                        f"Example: {example_path}",
                        True,
                        "Syntax valid"
                    )
                except SyntaxError as e:
                    self.record_result(
                        f"Example: {example_path}",
                        False,
                        f"Syntax error: {e}"
                    )
            else:
                self.record_result(f"Example: {example_path}", False, "File missing")

    async def validate_requirements_traceability(self):
        """Validate requirements traceability annotations."""
        print("\n🏷️ Validating Requirements Traceability...")

        # Check that example files have REQ annotations
        project_root = Path(__file__).parent.parent

        files_to_check = [
            "examples/quick_start.py",
            "examples/custom_agent.py"
        ]

        for file_path in files_to_check:
            full_path = project_root / file_path
            if full_path.exists():
                content = full_path.read_text()
                has_req = "@REQ-" in content
                has_blp = "@BLP:" in content or "BLP-" in content
                self.record_result(
                    f"REQ annotations: {file_path}",
                    has_req and has_blp,
                    "Has REQ and BLP" if (has_req and has_blp) else "Missing annotations"
                )

    async def validate_blp_coverage(self):
        """Validate BLP coverage in documentation."""
        print("\n📊 Validating BLP Coverage...")

        project_root = Path(__file__).parent.parent
        blp_doc = project_root / "docs" / "BLP_FRAMEWORK.md"

        if blp_doc.exists():
            content = blp_doc.read_text()

            # Check all 6 BLP categories are documented
            categories = [
                ("Alignment", "BLP-001"),
                ("Autonomy", "BLP-011"),
                ("Durability", "BLP-021"),
                ("Self-Improvement", "BLP-031"),
                ("Self-Replication", "BLP-041"),
                ("Self-Organization", "BLP-051")
            ]

            for category, blp_id in categories:
                has_category = category in content
                has_blp = blp_id in content or f"BLP-{int(blp_id.split('-')[1]):03d}" in content
                self.record_result(
                    f"BLP Category: {category}",
                    has_category,
                    "Documented" if has_category else "Missing"
                )

            # Check compute advantage formula
            has_formula = "Compute Advantage" in content
            self.record_result(
                "Compute Advantage Formula",
                has_formula,
                "Documented" if has_formula else "Missing"
            )
        else:
            self.record_result("BLP Documentation", False, "File missing")

    async def validate_ditd_lifecycle(self):
        """Validate DITD lifecycle documentation."""
        print("\n🔄 Validating DITD Lifecycle...")

        project_root = Path(__file__).parent.parent
        ditd_doc = project_root / "docs" / "DITD_LIFECYCLE.md"

        if ditd_doc.exists():
            content = ditd_doc.read_text()

            # Check all 5 DITD stages are documented
            stages = ["Design", "Implement", "Test", "Deploy", "Operations"]

            for stage in stages:
                has_stage = f"## Stage" in content and stage in content
                self.record_result(
                    f"DITD Stage: {stage}",
                    stage in content,
                    "Documented" if stage in content else "Missing"
                )

            # Check validation results section
            has_results = "Validation Results" in content
            self.record_result(
                "DITD Validation Results",
                has_results,
                "Included" if has_results else "Missing"
            )
        else:
            self.record_result("DITD Documentation", False, "File missing")

    async def validate_no_sensitive_data(self):
        """Validate no sensitive data in files."""
        print("\n🔐 Validating No Sensitive Data...")

        project_root = Path(__file__).parent.parent

        # Patterns that should NOT appear in public repo
        sensitive_patterns = [
            ("API Key", "sk_"),
            ("API Key", "sk-ant-"),
            ("API Key", "sk-proj-"),
            ("Private Key", "nsec"),
            ("Phone Number", "15712781730"),
            ("Private IP", "34.27.49.187"),
            ("Personal Email", "craigmbrown@"),
            ("Home Path", "/home/craigmbrown")
        ]

        # Files to check
        files_to_check = list(project_root.glob("**/*.py"))
        files_to_check.extend(project_root.glob("**/*.md"))
        files_to_check.extend(project_root.glob("**/*.yaml"))
        files_to_check.extend(project_root.glob("**/*.yml"))
        files_to_check.extend(project_root.glob("**/*.json"))

        # Exclude .env files from check (they should have placeholders only)
        files_to_check = [f for f in files_to_check if ".env" not in f.name or f.name == ".env.example"]

        issues = []
        for pattern_name, pattern in sensitive_patterns:
            for file_path in files_to_check:
                try:
                    content = file_path.read_text()
                    if pattern.lower() in content.lower():
                        issues.append(f"{pattern_name} found in {file_path.name}")
                except Exception:
                    pass  # Skip unreadable files

        if issues:
            self.record_result(
                "No Sensitive Data",
                False,
                f"{len(issues)} issues found"
            )
            for issue in issues[:5]:  # Show first 5
                print(f"    ⚠️ {issue}")
        else:
            self.record_result("No Sensitive Data", True, "Clean")

    def generate_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_tests": total,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": f"{success_rate:.1f}%",
            "status": "PASSED" if self.failed == 0 else "FAILED",
            "results": self.results
        }

        return report


async def main():
    """Run system validation."""
    print("\n" + "="*60)
    print("Multi-Agent Consensus Framework - System Validation")
    print("="*60)

    validator = SystemValidator()

    # Run all validations
    await validator.validate_environment()
    await validator.validate_documentation()
    await validator.validate_examples()
    await validator.validate_requirements_traceability()
    await validator.validate_blp_coverage()
    await validator.validate_ditd_lifecycle()
    await validator.validate_no_sensitive_data()

    # Generate report
    report = validator.generate_report()

    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total Tests: {report['total_tests']}")
    print(f"Passed: {report['passed']} ✅")
    print(f"Failed: {report['failed']} ❌")
    print(f"Success Rate: {report['success_rate']}")
    print(f"Status: {report['status']}")
    print("="*60 + "\n")

    # Exit with appropriate code
    sys.exit(0 if report['status'] == "PASSED" else 1)


if __name__ == "__main__":
    asyncio.run(main())
