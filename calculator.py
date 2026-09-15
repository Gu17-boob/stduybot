import sympy as sp


def solve_expression(expression):
    """Solve a mathematical expression or equation."""

    try:
        expression = expression.strip()

        if not expression:
            return None, "Please enter a mathematical expression."

        if "=" in expression:
            left, right = expression.split("=", 1)

            x = sp.symbols("x")

            equation = sp.Eq(
                sp.sympify(left),
                sp.sympify(right)
            )

            solution = sp.solve(equation, x)

            return solution, None

        result = sp.sympify(expression)

        return result, None

    except Exception:
        return None, "Invalid mathematical expression."