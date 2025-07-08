#!/usr/bin/env python3
"""
Example: Using REALM-Bench Evaluation Framework

This example demonstrates how to use the evaluation framework to assess
multi-agent planning performance on a simple task.
"""

import sys
import os
import time

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from evaluation.evaluator import BenchmarkEvaluator, EvaluationConfig
from evaluation.framework_runners import create_mock_runner
from evaluation.task_definitions import TASK_DEFINITIONS


def run_simple_evaluation():
    """Run a simple evaluation with mock runners"""
    print("🚀 REALM-Bench Evaluation Example")
    print("=" * 50)
    
    # Create evaluation configuration
    config = EvaluationConfig(
        frameworks=["langgraph", "autogen", "crewai", "swarm"],
        tasks=["P11", "P1"],  # Just test with first two tasks
        num_runs=2,  # Fewer runs for quick testing
        timeout_seconds=60,
        output_dir="example_results",
        enable_visualization=True,
        save_detailed_results=True
    )
    
    # Create mock runners for demonstration
    framework_runners = {
        "langgraph": create_mock_runner("langgraph"),
        "autogen": create_mock_runner("autogen"),
        "crewai": create_mock_runner("crewai"),
        "swarm": create_mock_runner("swarm")
    }
    
    # Create benchmark evaluator
    evaluator = BenchmarkEvaluator(config)
    
    print(f"Evaluating {len(config.frameworks)} frameworks on {len(config.tasks)} tasks")
    print(f"Number of runs per task: {config.num_runs}")
    print(f"Output directory: {config.output_dir}")
    print()
    
    try:
        # Run the benchmark
        print("🔄 Running evaluation...")
        results = evaluator.run_benchmark(framework_runners)
        
        # Print summary
        evaluator.print_summary()
        
        print("✅ Example evaluation completed!")
        print(f"📁 Results saved to: {config.output_dir}")
        
        return results
        
    except Exception as e:
        print(f"❌ Evaluation failed: {str(e)}")
        return None


def analyze_task_definition():
    """Demonstrate task definition structure"""
    print("\n📋 Task Definition Example")
    print("=" * 30)
    
    # Get the first task definition
    task = TASK_DEFINITIONS["P11"]
    
    print(f"Task ID: {task.task_id}")
    print(f"Name: {task.name}")
    print(f"Category: {task.category.value}")
    print(f"Description: {task.description}")
    
    print(f"\nGoals ({len(task.goals)}):")
    for goal in task.goals:
        print(f"  - {goal.goal_id}: {goal.description} (weight: {goal.weight})")
    
    print(f"\nConstraints ({len(task.constraints)}):")
    for constraint in task.constraints:
        print(f"  - {constraint.constraint_id}: {constraint.description}")
    
    print(f"\nResources:")
    for key, value in task.resources.items():
        print(f"  - {key}: {value}")
    
    print(f"\nEvaluation Weights:")
    for metric, weight in task.evaluation_weights.items():
        print(f"  - {metric}: {weight}")


def demonstrate_metrics():
    """Demonstrate the evaluation metrics"""
    print("\n📊 Evaluation Metrics Overview")
    print("=" * 35)
    
    from evaluation.metrics import (
        PlanningQualityMetrics,
        PlanningOptimalityMetrics,
        CoordinationEffectivenessMetrics,
        ConstraintSatisfactionMetrics,
        ResourceUsageMetrics,
        AdaptationMetrics
    )
    
    # Create metric evaluators
    planning_quality = PlanningQualityMetrics()
    planning_optimality = PlanningOptimalityMetrics()
    coordination = CoordinationEffectivenessMetrics()
    constraints = ConstraintSatisfactionMetrics()
    resources = ResourceUsageMetrics()
    adaptation = AdaptationMetrics()
    
    # Example: Planning Quality
    expected_goals = ["minimize_makespan", "minimize_idle_time", "balance_workload"]
    achieved_goals = ["minimize_makespan", "minimize_idle_time"]
    
    goal_result = planning_quality.evaluate_goal_satisfaction(expected_goals, achieved_goals)
    print(f"Goal Satisfaction Rate: {goal_result.value:.2f}%")
    
    # Example: Planning Optimality
    schedule = [
        {"task_id": "task1", "start_time": 0, "end_time": 10},
        {"task_id": "task2", "start_time": 10, "end_time": 20},
        {"task_id": "task3", "start_time": 20, "end_time": 30}
    ]
    
    makespan_result = planning_optimality.evaluate_makespan(schedule)
    print(f"Makespan: {makespan_result.value} time units")
    
    # Example: Resource Usage
    memory_usage = [
        {"memory_mb": 100, "timestamp": time.time()},
        {"memory_mb": 120, "timestamp": time.time() + 1},
        {"memory_mb": 110, "timestamp": time.time() + 2}
    ]
    
    memory_result = resources.evaluate_memory_usage(memory_usage)
    print(f"Peak Memory Usage: {memory_result.value:.2f} MB")


def main():
    """Main example function"""
    print("REALM-Bench Evaluation Framework Example")
    print("=" * 50)
    
    # Demonstrate task definition structure
    analyze_task_definition()
    
    # Demonstrate metrics
    demonstrate_metrics()
    
    # Run simple evaluation
    print("\n" + "=" * 50)
    results = run_simple_evaluation()
    
    if results:
        print("\n🎉 Example completed successfully!")
        print("Check the 'example_results' directory for detailed outputs.")
    else:
        print("\n❌ Example failed. Check the error messages above.")


if __name__ == "__main__":
    main() 