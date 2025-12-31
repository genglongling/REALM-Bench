from typing import Annotated, Literal
from pydantic import BaseModel, Field

Operator = Literal["+", "-", "*", "/"]


class CalculatorInput(BaseModel):
    a: Annotated[int, Field(description="The first number.")]
    b: Annotated[int, Field(description="The second number.")]
    operator: Annotated[Operator, Field(description="The operator.")]


def calculator(input: Annotated[CalculatorInput, "Input to the calculator."]) -> int:
    if not isinstance(input, CalculatorInput):
        return "Invalid input: expected CalculatorInput model."

    if input.operator == "+":
        result = input.a + input.b
    elif input.operator == "-":
        result = input.a - input.b
    elif input.operator == "*":
        result = input.a * input.b
    elif input.operator == "/":
        result = int(input.a / input.b)
    else:
        raise ValueError("Invalid operator")

    return result
