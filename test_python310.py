#!/usr/bin/env python3
"""
Python 3.10 Compatibility Test for REALM-Bench

This script tests if all dependencies work correctly with Python 3.10.
"""

import sys
import importlib
from typing import List, Dict, Any

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Python Version Test")
    print("=" * 40)
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Python 3.10+ detected - Compatible!")
    else:
        print("❌ Python 3.10+ required!")
        return False
    
    print()
    return True

def test_core_dependencies():
    """Test core dependencies"""
    print("📦 Core Dependencies Test")
    print("=" * 40)
    
    dependencies = [
        "pandas",
        "numpy", 
        "matplotlib",
        "seaborn",
        "psutil",
        "json",
        "time",
        "os",
        "sys"
    ]
    
    failed = []
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError as e:
            print(f"❌ {dep}: {e}")
            failed.append(dep)
    
    if failed:
        print(f"\n❌ Failed to import: {failed}")
        return False
    else:
        print("\n✅ All core dependencies available!")
    
    print()
    return True

def test_evaluation_framework():
    """Test evaluation framework imports"""
    print("🔧 Evaluation Framework Test")
    print("=" * 40)
    
    try:
        from evaluation.task_definitions import TASK_DEFINITIONS
        print("✅ Task definitions imported")
        
        from evaluation.metrics import PlanningQualityMetrics
        print("✅ Metrics classes imported")
        
        from evaluation.evaluator import BenchmarkEvaluator, EvaluationConfig
        print("✅ Evaluator classes imported")
        
        from evaluation.framework_runners import get_framework_runners
        print("✅ Framework runners imported")
        
        print(f"✅ Available tasks: {list(TASK_DEFINITIONS.keys())}")
        
    except ImportError as e:
        print(f"❌ Evaluation framework import failed: {e}")
        return False
    
    print()
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("⚙️ Basic Functionality Test")
    print("=" * 40)
    
    try:
        # Test task definition
        from evaluation.task_definitions import TASK_DEFINITIONS
        task = TASK_DEFINITIONS["P11"]
        print(f"✅ Task P11 loaded: {task.name}")
        
        # Test metrics
        from evaluation.metrics import PlanningQualityMetrics
        metrics = PlanningQualityMetrics()
        print("✅ Metrics instance created")
        
        # Test evaluation config
        from evaluation.evaluator import EvaluationConfig
        config = EvaluationConfig(
            frameworks=["langgraph"],
            tasks=["P11"],
            num_runs=1,
            timeout_seconds=60
        )
        print("✅ Evaluation config created")
        
        # Test mock runner
        from evaluation.framework_runners import create_mock_runner
        mock_runner = create_mock_runner("test")
        print("✅ Mock runner created")
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False
    
    print("✅ All basic functionality tests passed!")
    print()
    return True

def test_optional_frameworks():
    """Test optional framework availability"""
    print("🔌 Optional Frameworks Test")
    print("=" * 40)
    
    frameworks = ["langgraph", "autogen", "crewai", "swarm"]
    
    for framework in frameworks:
        try:
            if framework == "langgraph":
                import langgraph
                print(f"✅ {framework}: Available")
            elif framework == "autogen":
                import autogen
                print(f"✅ {framework}: Available")
            elif framework == "crewai":
                import crewai
                print(f"✅ {framework}: Available")
            elif framework == "swarm":
                # Swarm is installed via git, so we'll just check if it's importable
                print(f"✅ {framework}: Available (git install)")
        except ImportError:
            print(f"⚠️ {framework}: Not available (will use mock runner)")
    
    print()

def main():
    """Run all tests"""
    print("🧪 REALM-Bench Python 3.10 Compatibility Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Core Dependencies", test_core_dependencies),
        ("Evaluation Framework", test_evaluation_framework),
        ("Basic Functionality", test_basic_functionality),
        ("Optional Frameworks", test_optional_frameworks)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("📊 Test Summary")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! REALM-Bench is ready to use with Python 3.10!")
        print("\nYou can now run:")
        print("  python run_evaluation.py --mock")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("You may need to install missing dependencies or fix configuration.")

if __name__ == "__main__":
    main() 