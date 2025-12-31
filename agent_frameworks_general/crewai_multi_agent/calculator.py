from typing import Literal, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

Operator = Literal["+", "-", "*", "/"]


class CalculatorInput(BaseModel):
    """Input for CalculatorTool."""

    a: int = Field(description="The first number.")
    b: int = Field(description="The second number.")
    operator: Operator = Field(description="The operator.")


class CalculatorTool(BaseTool):
    name: str = "Calculator Tool"
    description: str = "A tool that can be used to perform basic arithmetic operations (+, -, *, /) on two integers."
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, a: int, b: int, operator: Operator) -> int:
        if operator == "+":
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator == "*":
            result = a * b
        elif operator == "/":
            if b == 0:
                return "Error: Division by zero."
            result = a / b
        else:
            raise ValueError("Invalid operator.")
        return result
