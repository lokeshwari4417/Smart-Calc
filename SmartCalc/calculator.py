"""
calculator.py - Core mathematical evaluation engine for SmartCalc.

Provides secure AST-based expression evaluation, input validation,
number formatting, and stateful calculation operations.
"""

import ast
import operator
import re
from typing import Tuple, Union, Optional


class SafeEvaluator:
    """
    Evaluates mathematical expressions safely using Python's Abstract Syntax Tree (AST).
    Prevents execution of arbitrary code by strictly allowing only basic arithmetic AST nodes.
    """

    # Supported binary operators
    _BINARY_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.FloorDiv: operator.floordiv,
    }

    # Supported unary operators
    _UNARY_OPS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    @classmethod
    def evaluate(cls, expression: str) -> Tuple[Optional[Union[int, float]], Optional[str]]:
        """
        Safely evaluates a sanitized mathematical expression string.

        Returns:
            (result, None) on success
            (None, error_message) on failure
        """
        if not expression or not expression.strip():
            return None, "Empty expression"

        # Normalize UI symbols to Python operators
        sanitized = cls._sanitize_expression(expression)
        if not sanitized:
            return None, "Invalid expression"

        try:
            # Parse into AST in 'eval' mode
            tree = ast.parse(sanitized, mode="eval")
            result = cls._eval_node(tree.body)

            # Check if result is a valid finite number
            if isinstance(result, (int, float)):
                # Handle special float values
                if result != result:  # NaN check
                    return None, "Math Error"
                if abs(result) == float("inf"):
                    return None, "Number too large"
                return result, None

            return None, "Invalid result"

        except ZeroDivisionError:
            return None, "Cannot divide by zero"
        except OverflowError:
            return None, "Number too large"
        except (SyntaxError, ValueError, TypeError):
            return None, "Invalid expression"
        except Exception as e:
            return None, f"Error: {str(e)}"

    @classmethod
    def _sanitize_expression(cls, expr: str) -> str:
        """
        Replaces user-facing display symbols with standard Python math operators.
        """
        expr = expr.strip()
        expr = expr.replace("×", "*").replace("✕", "*").replace("x", "*").replace("X", "*")
        expr = expr.replace("÷", "/").replace("∕", "/")
        expr = expr.replace("−", "-").replace("–", "-").replace("—", "-")
        expr = expr.replace(",", "")  # Remove thousands separators

        return expr

    @classmethod
    def _eval_node(cls, node: ast.AST) -> Union[int, float]:
        """
        Recursively evaluates an AST node strictly within allowed arithmetic boundaries.
        """
        # Python 3.8+ uses ast.Constant for literals
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        # Python < 3.8 compatibility for ast.Num
        if hasattr(ast, "Num") and isinstance(node, ast.Num):
            return node.n

        # Binary operations: left <op> right (e.g., 5 + 3, 10 * 2)
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in cls._BINARY_OPS:
                raise ValueError(f"Unsupported operator: {op_type}")

            left_val = cls._eval_node(node.left)
            right_val = cls._eval_node(node.right)

            # Prevent excessive exponentiation denial-of-service
            if op_type == ast.Pow:
                if abs(right_val) > 1000 or (abs(left_val) > 1 and right_val > 1000):
                    raise OverflowError("Exponent too large")

            # Check division by zero before operator call to produce clean message
            if op_type in (ast.Div, ast.Mod, ast.FloorDiv) and right_val == 0:
                raise ZeroDivisionError("Cannot divide by zero")

            return cls._BINARY_OPS[op_type](left_val, right_val)

        # Unary operations: <op> operand (e.g., -5, +3)
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in cls._UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {op_type}")

            operand_val = cls._eval_node(node.operand)
            return cls._UNARY_OPS[op_type](operand_val)

        # Disallow everything else (function calls, variables, attributes, imports, etc.)
        raise ValueError(f"Unsupported syntax construct: {type(node).__name__}")


class CalculatorEngine:
    """
    Manages the active state, input sequencing, and calculation flow for SmartCalc.
    """

    MAX_DISPLAY_LENGTH = 16

    def __init__(self):
        self.expression: str = ""       # Current full formula (e.g., "125 × 8")
        self.current_entry: str = "0"   # Current active number entry (e.g., "8")
        self.result: Optional[str] = None
        self.error_message: Optional[str] = None
        self.is_new_calculation: bool = False

    def input_digit(self, digit: str) -> None:
        """Appends a numerical digit (0-9) to the current active number."""
        self.error_message = None

        if self.is_new_calculation:
            self.expression = ""
            self.current_entry = digit
            self.is_new_calculation = False
            return

        if self.current_entry == "0":
            self.current_entry = digit
        else:
            if len(self.current_entry.replace(",", "").replace(".", "").replace("-", "")) < self.MAX_DISPLAY_LENGTH:
                self.current_entry += digit

    def input_decimal(self) -> None:
        """Appends a decimal point '.' to the current active number."""
        self.error_message = None

        if self.is_new_calculation:
            self.expression = ""
            self.current_entry = "0."
            self.is_new_calculation = False
            return

        if "." not in self.current_entry:
            self.current_entry += "."

    def input_operator(self, op: str) -> None:
        """
        Applies a binary operator (+, −, ×, ÷, %).
        Chains previous calculations if needed.
        """
        self.error_message = None

        # Standardize operator symbol
        op_map = {"*": "×", "/": "÷", "-": "−", "+": "+", "%": "%"}
        display_op = op_map.get(op, op)

        if self.is_new_calculation:
            # Continue calculating from previous result
            self.expression = f"{self.current_entry} {display_op} "
            self.is_new_calculation = False
            self.current_entry = "0"
            return

        if self.expression and self.expression.endswith((" + ", " − ", " × ", " ÷ ", " % ")):
            if self.current_entry == "0":
                # User changed their mind about the operator
                self.expression = self.expression[:-3] + f" {display_op} "
                return

        # Append current entry and operator to expression
        clean_num = self._clean_number_str(self.current_entry)
        self.expression += f"{clean_num} {display_op} "
        self.current_entry = "0"

    def toggle_sign(self) -> None:
        """Toggles the positive/negative sign of the current entry."""
        self.error_message = None

        if self.current_entry == "0":
            return

        if self.current_entry.startswith("-"):
            self.current_entry = self.current_entry[1:]
        else:
            self.current_entry = "-" + self.current_entry

    def apply_percentage(self) -> None:
        """
        Converts the current entry to its percentage value (entry / 100).
        """
        self.error_message = None
        try:
            val = float(self._clean_number_str(self.current_entry))
            percent_val = val / 100.0
            self.current_entry = self.format_number(percent_val)
        except (ValueError, TypeError):
            self.error_message = "Invalid percentage"

    def backspace(self) -> None:
        """Deletes the last character from the current entry."""
        self.error_message = None

        if self.is_new_calculation:
            self.clear_all()
            return

        if len(self.current_entry) > 1:
            if self.current_entry.startswith("-") and len(self.current_entry) == 2:
                self.current_entry = "0"
            else:
                self.current_entry = self.current_entry[:-1]
        else:
            self.current_entry = "0"

    def clear_entry(self) -> None:
        """Resets only the current active entry."""
        self.current_entry = "0"
        self.error_message = None

    def clear_all(self) -> None:
        """Resets the entire calculator state."""
        self.expression = ""
        self.current_entry = "0"
        self.result = None
        self.error_message = None
        self.is_new_calculation = False

    def calculate(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Evaluates the full current formula.

        Returns:
            (formula_str, formatted_result_str, error_message)
        """
        self.error_message = None

        # Build full expression string
        clean_entry = self._clean_number_str(self.current_entry)
        full_expression = f"{self.expression}{clean_entry}".strip()

        if not full_expression:
            return None, None, "Empty expression"

        # Check if user pressed '=' with a trailing operator like "12 +"
        if full_expression.endswith((" +", " −", " ×", " ÷", " %")):
            full_expression = full_expression.rsplit(" ", 1)[0].strip()

        raw_result, error = SafeEvaluator.evaluate(full_expression)

        if error is not None:
            self.error_message = error
            return full_expression, None, error

        formatted_result = self.format_number(raw_result)
        formula_display = f"{full_expression} ="

        # Update engine state for next operation
        self.expression = formula_display
        self.current_entry = formatted_result
        self.result = formatted_result
        self.is_new_calculation = True

        return full_expression, formatted_result, None

    @staticmethod
    def format_number(val: Union[int, float]) -> str:
        """
        Formats a number cleanly:
        - Integers displayed without decimal point (e.g., 5, 1000)
        - Eliminates floating-point precision artifacts (e.g. 0.30000000000000004 -> 0.3)
        - Very large / very small numbers in scientific notation if necessary
        """
        if isinstance(val, int):
            return f"{val:,}"

        if isinstance(val, float):
            # Check if float is practically an integer (e.g. 10.0 -> 10)
            if val.is_integer() and abs(val) < 1e15:
                return f"{int(val):,}"

            # Check for extreme magnitudes
            if abs(val) >= 1e15 or (0 < abs(val) < 1e-6):
                return f"{val:.6e}"

            # Round to 10 decimal places to eliminate precision artifacts, then strip trailing zeros
            rounded = round(val, 10)
            formatted = f"{rounded:f}".rstrip("0").rstrip(".")

            # Add comma separators to integer part if reasonable
            if "." in formatted:
                int_part, dec_part = formatted.split(".", 1)
                try:
                    int_formatted = f"{int(int_part):,}"
                    return f"{int_formatted}.{dec_part}"
                except ValueError:
                    return formatted
            else:
                try:
                    return f"{int(formatted):,}"
                except ValueError:
                    return formatted

        return str(val)

    @staticmethod
    def _clean_number_str(num_str: str) -> str:
        """Removes display formatting like comma separators."""
        return num_str.replace(",", "").strip()
