#!/usr/bin/env python3
"""
Verification Script for Zero CRM Skill Installation

Checks:
- Python version
- Required dependencies
- API key configuration
- API connectivity
- Skill installation

Usage:
    python3 verify.py
"""

import sys
import os
import subprocess


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def check_python_version():
    """Check Python version."""
    print_section("Checking Python Version")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print(f"Python version: {version_str}")

    if version.major >= 3 and version.minor >= 6:
        print("✅ Python version is compatible (3.6+)")
        return True
    else:
        print("❌ Python 3.6+ required")
        return False


def check_dependencies():
    """Check required Python packages."""
    print_section("Checking Dependencies")

    required_packages = {
        'requests': '2.28.0',
        'python-dotenv': '0.19.0'
    }

    all_installed = True

    for package, min_version in required_packages.items():
        try:
            if package == 'python-dotenv':
                import dotenv
                module_name = 'dotenv'
            else:
                module_name = package

            module = __import__(module_name)
            installed_version = getattr(module, '__version__', 'unknown')

            print(f"✅ {package}: {installed_version} (required: {min_version}+)")

        except ImportError:
            print(f"❌ {package}: NOT INSTALLED (required: {min_version}+)")
            all_installed = False

    if not all_installed:
        print("\n💡 Install missing dependencies:")
        print("   pip install -r requirements.txt")

    return all_installed


def check_api_key():
    """Check API key configuration."""
    print_section("Checking API Key Configuration")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("ZERO_CRM_API_KEY")

    if not api_key:
        print("❌ ZERO_CRM_API_KEY not found in environment")
        print("\n💡 Set your API key:")
        print("   echo 'ZERO_CRM_API_KEY=zero_your_key_here' > .env")
        return False

    if not api_key.startswith("zero_"):
        print(f"⚠️  API key format unexpected: {api_key[:10]}...")
        print("   Expected format: zero_<hash>")
        return False

    print(f"✅ API key found: {api_key[:10]}...{api_key[-5:]}")
    return True


def check_api_connectivity():
    """Test API connectivity."""
    print_section("Checking API Connectivity")

    try:
        import requests
        from dotenv import load_dotenv

        load_dotenv()

        BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

        # Test health endpoint (no auth)
        print("Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

        # Test authenticated endpoint
        api_key = os.getenv("ZERO_CRM_API_KEY")
        if api_key:
            print("\nTesting authenticated endpoint...")
            headers = {"x-api-key": api_key}

            response = requests.get(
                f"{BASE_URL}/api/user/profile",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Authentication successful")
                print(f"   User: {data.get('email', 'N/A')}")
                return True
            elif response.status_code == 401:
                print(f"❌ Authentication failed: Invalid API key")
                return False
            else:
                print(f"❌ API error: {response.status_code}")
                return False

        return True

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error: Cannot reach API")
        return False

    except requests.exceptions.Timeout:
        print(f"❌ Request timeout: API not responding")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_skill_files():
    """Check that all required skill files exist."""
    print_section("Checking Skill Files")

    required_files = [
        "SKILL.md",
        "README.md",
        "package.json",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
        "references/api_reference.md",
        "examples/basic_operations.py",
        "examples/bulk_import.py",
        "examples/pipeline_report.py",
        "examples/error_handling.py"
    ]

    all_exist = True

    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path:<40} ({size:>6} bytes)")
        else:
            print(f"❌ {file_path:<40} MISSING")
            all_exist = False

    return all_exist


def check_npm_package():
    """Check npm package configuration."""
    print_section("Checking npm Package")

    if not os.path.exists("package.json"):
        print("❌ package.json not found")
        return False

    try:
        import json

        with open("package.json", "r") as f:
            package = json.load(f)

        print(f"Package name: {package.get('name', 'N/A')}")
        print(f"Version:      {package.get('version', 'N/A')}")
        print(f"Description:  {package.get('description', 'N/A')}")

        if 'bin' in package:
            print(f"✅ CLI binaries configured: {list(package['bin'].keys())}")
        else:
            print(f"⚠️  No CLI binaries configured")

        return True

    except Exception as e:
        print(f"❌ Error reading package.json: {e}")
        return False


def run_verification():
    """Run all verification checks."""
    print("\n" + "="*70)
    print("ZERO CRM SKILL - INSTALLATION VERIFICATION")
    print("="*70)

    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "API Key": check_api_key(),
        "API Connectivity": check_api_connectivity(),
        "Skill Files": check_skill_files(),
        "npm Package": check_npm_package()
    }

    # Summary
    print_section("Verification Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check:<25} {status}")

    print(f"\n{'='*70}")
    print(f"Result: {passed}/{total} checks passed")
    print(f"{'='*70}")

    if passed == total:
        print("\n🎉 All checks passed! Skill is properly installed.")
        print("\n💡 Next steps:")
        print("   • Run examples: python3 examples/basic_operations.py")
        print("   • Run tests: python3 scripts/test_comprehensive.py")
        print("   • Read docs: cat SKILL.md")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. See details above.")
        return 1


def main():
    """Main entry point."""
    try:
        exit_code = run_verification()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
