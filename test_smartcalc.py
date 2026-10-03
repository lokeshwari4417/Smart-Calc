"""
test_smartcalc.py - Automated test suite for SmartCalc calculation engine,
security evaluation, history management, and edge cases.
"""

import unittest
from calculator import SafeEvaluator, CalculatorEngine
from history import HistoryManager


class TestSafeEvaluator(unittest.TestCase):
    """Tests the AST-based SafeEvaluator for accuracy and security."""

    def test_basic_arithmetic(self):
        # Addition
        res, err = SafeEvaluator.evaluate("10 + 20")
        self.assertIsNone(err)
        self.assertEqual(res, 30)

        # Subtraction
        res, err = SafeEvaluator.evaluate("50 - 15")
        self.assertIsNone(err)
        self.assertEqual(res, 35)

        # Multiplication
        res, err = SafeEvaluator.evaluate("8 × 7")
        self.assertIsNone(err)
        self.assertEqual(res, 56)

        # Division
        res, err = SafeEvaluator.evaluate("100 ÷ 4")
        self.assertIsNone(err)
        self.assertEqual(res, 25)

        # Decimal Addition
        res, err = SafeEvaluator.evaluate("10.5 + 2.5")
        self.assertIsNone(err)
        self.assertEqual(res, 13)

    def test_operator_precedence(self):
        # Standard math order of operations (BODMAS / PEMDAS)
        res, err = SafeEvaluator.evaluate("50 + 25 × 2")
        self.assertIsNone(err)
        self.assertEqual(res, 100)

        res, err = SafeEvaluator.evaluate("10 + 5 × 2 - 8 ÷ 4")
        self.assertIsNone(err)
        self.assertEqual(res, 18)  # 10 + 10 - 2 = 18

    def test_division_by_zero(self):
        res, err = SafeEvaluator.evaluate("10 ÷ 0")
        self.assertIsNone(res)
        self.assertEqual(err, "Cannot divide by zero")

        res, err = SafeEvaluator.evaluate("5 / (2 - 2)")
        self.assertIsNone(res)
        self.assertEqual(err, "Cannot divide by zero")

    def test_security_and_sandbox(self):
        # Disallowed Python expressions should fail cleanly without executing
        malicious_inputs = [
            "__import__('os').system('dir')",
            "open('test.txt', 'w')",
            "eval('2+2')",
            "exec('x=1')",
            "lambda x: x",
            "[x for x in range(10)]",
            "import math",
        ]
        for malicious in malicious_inputs:
            res, err = SafeEvaluator.evaluate(malicious)
            self.assertIsNone(res, f"Should not evaluate: {malicious}")
            self.assertIsNotNone(err)

    def test_invalid_syntax(self):
        invalid_expressions = ["++", "10 +* 5", "---", "", "   ", "abc + 2"]
        for expr in invalid_expressions:
            res, err = SafeEvaluator.evaluate(expr)
            self.assertIsNone(res)
            self.assertIsNotNone(err)


class TestCalculatorEngine(unittest.TestCase):
    """Tests the state machine of CalculatorEngine."""

    def setUp(self):
        self.engine = CalculatorEngine()

    def test_digit_entry(self):
        self.engine.input_digit("1")
        self.engine.input_digit("2")
        self.engine.input_digit("5")
        self.assertEqual(self.engine.current_entry, "125")

    def test_decimal_entry(self):
        self.engine.input_digit("3")
        self.engine.input_decimal()
        self.engine.input_digit("1")
        self.engine.input_digit("4")
        self.assertEqual(self.engine.current_entry, "3.14")
        # Second decimal should be ignored
        self.engine.input_decimal()
        self.assertEqual(self.engine.current_entry, "3.14")

    def test_sign_toggle(self):
        self.engine.input_digit("4")
        self.engine.input_digit("2")
        self.engine.toggle_sign()
        self.assertEqual(self.engine.current_entry, "-42")
        self.engine.toggle_sign()
        self.assertEqual(self.engine.current_entry, "42")

    def test_percentage(self):
        self.engine.input_digit("1")
        self.engine.input_digit("0")
        self.engine.input_digit("0")
        self.engine.apply_percentage()
        self.assertEqual(self.engine.current_entry, "1")

        self.engine.clear_all()
        self.engine.input_digit("5")
        self.engine.input_digit("0")
        self.engine.apply_percentage()
        self.assertEqual(self.engine.current_entry, "0.5")

    def test_backspace(self):
        self.engine.input_digit("9")
        self.engine.input_digit("8")
        self.engine.input_digit("7")
        self.engine.backspace()
        self.assertEqual(self.engine.current_entry, "98")
        self.engine.backspace()
        self.assertEqual(self.engine.current_entry, "9")
        self.engine.backspace()
        self.assertEqual(self.engine.current_entry, "0")

    def test_full_calculation_flow(self):
        # 125 * 8 = 1000
        self.engine.input_digit("1")
        self.engine.input_digit("2")
        self.engine.input_digit("5")
        self.engine.input_operator("×")
        self.assertEqual(self.engine.expression, "125 × ")
        self.assertEqual(self.engine.current_entry, "0")

        self.engine.input_digit("8")
        expr, res, err = self.engine.calculate()
        self.assertIsNone(err)
        self.assertEqual(expr, "125 × 8")
        self.assertEqual(res, "1,000")
        self.assertEqual(self.engine.current_entry, "1,000")

    def test_chained_calculation(self):
        # 10 + 20 = 30, then * 2 = 60
        self.engine.input_digit("1")
        self.engine.input_digit("0")
        self.engine.input_operator("+")
        self.engine.input_digit("2")
        self.engine.input_digit("0")
        self.engine.calculate()
        self.assertEqual(self.engine.current_entry, "30")

        # Now press * directly to continue
        self.engine.input_operator("×")
        self.assertEqual(self.engine.expression, "30 × ")
        self.engine.input_digit("2")
        expr, res, err = self.engine.calculate()
        self.assertIsNone(err)
        self.assertEqual(res, "60")


class TestHistoryManager(unittest.TestCase):
    """Tests the session calculation history."""

    def setUp(self):
        self.history = HistoryManager(max_entries=5)

    def test_add_and_retrieve_history(self):
        self.assertTrue(self.history.is_empty())
        self.history.add_entry("25 + 25", "50")
        self.history.add_entry("100 ÷ 4", "25")
        self.history.add_entry("8 × 7", "56")

        self.assertEqual(self.history.count(), 3)
        items = self.history.get_all(reverse=True)
        # Newest first
        self.assertEqual(items[0].expression, "8 × 7")
        self.assertEqual(items[0].result, "56")
        self.assertEqual(items[2].expression, "25 + 25")

    def test_clear_history(self):
        self.history.add_entry("1 + 1", "2")
        self.assertEqual(self.history.count(), 1)
        self.history.clear()
        self.assertTrue(self.history.is_empty())
        self.assertEqual(self.history.count(), 0)

    def test_capacity_limit(self):
        for i in range(10):
            self.history.add_entry(f"{i} + 1", f"{i+1}")
        self.assertEqual(self.history.count(), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
