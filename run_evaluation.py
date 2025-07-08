#!/usr/bin/env python3
"""
REALM-Bench Evaluation Runner

This script runs the complete evaluation benchmark for multi-agent planning tasks
across different frameworks and generates comprehensive results and visualizations.

Usage:
    python run_evaluation.py [options]

Options:
    --frameworks FRAMEWORKS    Comma-separated list of frameworks to evaluate
    --tasks TASKS             Comma-separated list of tasks to evaluate
    --runs RUNS               Number of runs per task (default: 3)
    --timeout TIMEOUT         Timeout in seconds per task (default: 300)
    --output-dir DIR          Output directory for results (default: evaluation_results)
    --no-viz                  Disable visualization generation
    --mock                    Use mock runners for testing
    --help                    Show this help message
"""

import argparse
import sys
import os
from typing import List, Dict

# Add project paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from evaluation.evaluator import BenchmarkEvaluator, EvaluationConfig
from evaluation.framework_runners import get_framework_runners, create_mock_runner
from evaluation.task_definitions import TASK_DEFINITIONS


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Run REALM-Bench evaluation for multi-agent planning tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run full benchmark with all frameworks and tasks
    python run_evaluation.py
    
    # Run only specific frameworks
    python run_evaluation.py --frameworks langgraph,crewai
    
    # Run only specific tasks
    python run_evaluation.py --tasks P11,P1,P2
    
    # Run with mock runners for testing
    python run_evaluation.py --mock
    
    # Run with custom settings
    python run_evaluation.py --runs 5 --timeout 600 --output-dir my_results
        """
    )
    
    parser.add_argument(
        '--frameworks',
        type=str,
        help='Comma-separated list of frameworks to evaluate (langgraph,autogen,crewai,swarm)'
    )
    
    parser.add_argument(
        '--tasks',
        type=str,
        help='Comma-separated list of tasks to evaluate (P0-P10)'
    )
    
    parser.add_argument(
        '--runs',
        type=int,
        default=3,
        help='Number of runs per task (default: 3)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='Timeout in seconds per task (default: 300)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='evaluation_results',
        help='Output directory for results (default: evaluation_results)'
    )
    
    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='Disable visualization generation'
    )
    
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock runners for testing (when frameworks are not available)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def validate_config(args, available_frameworks: List[str], available_tasks: List[str]):
    """Validate the evaluation configuration"""
    # Validate frameworks
    if args.frameworks:
        requested_frameworks = [f.strip() for f in args.frameworks.split(',')]
        invalid_frameworks = [f for f in requested_frameworks if f not in available_frameworks]
        if invalid_frameworks:
            print(f"Warning: Invalid frameworks: {invalid_frameworks}")
            print(f"Available frameworks: {available_frameworks}")
            return False
    else:
        requested_frameworks = available_frameworks
    
    # Validate tasks
    if args.tasks:
        requested_tasks = [t.strip() for t in args.tasks.split(',')]
        invalid_tasks = [t for t in requested_tasks if t not in available_tasks]
        if invalid_tasks:
            print(f"Warning: Invalid tasks: {invalid_tasks}")
            print(f"Available tasks: {available_tasks}")
            return False
    else:
        requested_tasks = available_tasks
    
    return True


def print_evaluation_info(config: EvaluationConfig, available_frameworks: List[str]):
    """Print evaluation configuration information"""
    print("=" * 60)
    print("REALM-Bench Evaluation Configuration")
    print("=" * 60)
    print(f"Frameworks to evaluate: {config.frameworks}")
    print(f"Tasks to evaluate: {config.tasks}")
    print(f"Number of runs per task: {config.num_runs}")
    print(f"Timeout per task: {config.timeout_seconds} seconds")
    print(f"Output directory: {config.output_dir}")
    print(f"Visualization enabled: {config.enable_visualization}")
    print(f"Available frameworks: {available_frameworks}")
    print("=" * 60)
    print()


def main():
    """Main evaluation function"""
    args = parse_arguments()
    
    print("🚀 Starting REALM-Bench Evaluation")
    print("=" * 60)
    
    # Get available frameworks
    if args.mock:
        print("Using mock runners for testing...")
        available_frameworks = ["langgraph", "autogen", "crewai", "swarm"]
        framework_runners = {
            framework: create_mock_runner(framework)
            for framework in available_frameworks
        }
    else:
        framework_runners = get_framework_runners()
        available_frameworks = list(framework_runners.keys())
    
    if not available_frameworks:
        print("❌ No frameworks available for evaluation!")
        print("Please ensure at least one framework is properly installed and configured.")
        return 1
    
    # Get available tasks
    available_tasks = list(TASK_DEFINITIONS.keys())
    
    # Validate configuration
    if not validate_config(args, available_frameworks, available_tasks):
        return 1
    
    # Create evaluation configuration
    config = EvaluationConfig(
        frameworks=args.frameworks.split(',') if args.frameworks else available_frameworks,
        tasks=args.tasks.split(',') if args.tasks else available_tasks,
        num_runs=args.runs,
        timeout_seconds=args.timeout,
        output_dir=args.output_dir,
        enable_visualization=not args.no_viz,
        save_detailed_results=True
    )
    
    # Print configuration
    print_evaluation_info(config, available_frameworks)
    
    # Create benchmark evaluator
    evaluator = BenchmarkEvaluator(config)
    
    try:
        # Run the benchmark
        print("🔄 Running benchmark evaluation...")
        results = evaluator.run_benchmark(framework_runners)
        
        # Print summary
        evaluator.print_summary()
        
        print("✅ Evaluation completed successfully!")
        print(f"📁 Results saved to: {config.output_dir}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Evaluation interrupted by user")
        return 1
        
    except Exception as e:
        print(f"❌ Evaluation failed with error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 