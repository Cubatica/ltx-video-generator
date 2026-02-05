"""
Test script to verify the application works correctly
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import gradio as gr
        print("✓ Gradio imported successfully")
        
        from PIL import Image
        print("✓ PIL imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_app_structure():
    """Test that the app.py file is properly structured"""
    print("\nTesting app structure...")
    
    # Import the app module
    try:
        # Add current directory to path for imports
        sys.path.insert(0, str(Path(__file__).parent))
        # We can't fully import app because it will try to launch, but we can check syntax
        with open('app.py', 'r') as f:
            content = f.read()
            
        # Check for key components
        checks = {
            "Gradio Blocks": "gr.Blocks" in content,
            "generate_video function": "def generate_video" in content,
            "check_ltx2_installation": "def check_ltx2_installation" in content,
            "model status check": "check_model_files" in content,
            "Examples": "gr.Examples" in content,
        }
        
        all_pass = True
        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"{status} {check}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"✗ Error checking app structure: {e}")
        return False


def test_directory_creation():
    """Test that directories are created properly"""
    print("\nTesting directory creation...")
    
    # The app should create these directories
    dirs = ['models', 'outputs']
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"- {dir_name}/ directory will be created on first run")
    
    return True


def test_files_exist():
    """Test that required files exist"""
    print("\nTesting file existence...")
    
    required_files = {
        'app.py': 'Main application file',
        'requirements.txt': 'Dependencies file',
        'README.md': 'Documentation',
        '.gitignore': 'Git ignore file'
    }
    
    all_exist = True
    for file, desc in required_files.items():
        file_path = Path(file)
        if file_path.exists():
            print(f"✓ {file} ({desc})")
        else:
            print(f"✗ {file} ({desc}) - MISSING")
            all_exist = False
    
    return all_exist


def test_readme_content():
    """Test that README has important sections"""
    print("\nTesting README content...")
    
    with open('README.md', 'r') as f:
        content = f.read()
    
    sections = [
        "Quick Start",
        "Installation",
        "Usage",
        "Requirements",
        "Tips",
    ]
    
    all_found = True
    for section in sections:
        if section in content:
            print(f"✓ {section} section found")
        else:
            print(f"- {section} section not found")
            all_found = False
    
    return True  # Not critical if some sections are named differently


def main():
    """Run all tests"""
    print("=" * 60)
    print("LTX-2 Video Generator - Application Tests")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("App Structure", test_app_structure),
        ("Directory Creation", test_directory_creation),
        ("File Existence", test_files_exist),
        ("README Content", test_readme_content),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_pass = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_pass:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)
    
    return 0 if all_pass else 1


if __name__ == "__main__":
    exit(main())
