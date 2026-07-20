"""
REALM-Bench Evaluation Framework.

The package root uses lazy imports so lightweight modules such as
evaluation.tier6.schemas and evaluation.tier6.scorer can be imported without
loading optional/heavy dependencies from the legacy evaluator stack.
"""

from importlib import import_module


_LAZY_ATTRS = {
    "PlanningQualityMetrics": "evaluation.metrics",
    "PlanningOptimalityMetrics": "evaluation.metrics",
    "CoordinationEffectivenessMetrics": "evaluation.metrics",
    "ConstraintSatisfactionMetrics": "evaluation.metrics",
    "ResourceUsageMetrics": "evaluation.metrics",
    "AdaptationMetrics": "evaluation.metrics",
    "TaskEvaluator": "evaluation.evaluator",
    "FrameworkEvaluator": "evaluation.evaluator",
    "BenchmarkEvaluator": "evaluation.evaluator",
    "TASK_DEFINITIONS": "evaluation.task_definitions",
    "TaskDefinition": "evaluation.task_definitions",
    "TaskResult": "evaluation.task_definitions",
}


__all__ = sorted(_LAZY_ATTRS)


def __getattr__(name):
    if name not in _LAZY_ATTRS:
        raise AttributeError(f"module 'evaluation' has no attribute {name!r}")

    module = import_module(_LAZY_ATTRS[name])
    value = getattr(module, name)
    globals()[name] = value
    return value
