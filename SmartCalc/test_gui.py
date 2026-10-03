"""
test_gui.py - Automated GUI tests for SmartCalcApp Tkinter interface.
"""

import unittest
import tkinter as tk
from main import SmartCalcApp


class TestSmartCalcGUI(unittest.TestCase):
    """Tests the Tkinter GUI functionality without blocking mainloop."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = SmartCalcApp(self.root)
        self.root.update()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_gui_initialization(self):
        self.assertEqual(self.app.lbl_result.cget("text"), "0")
        self.assertEqual(self.app.lbl_expression.cget("text"), "")
        self.assertFalse(self.app.history_visible)

    def test_button_clicks_and_display(self):
        self.app._on_digit_click("1")
        self.app._on_digit_click("2")
        self.app._on_digit_click("5")
        self.root.update()
        self.assertEqual(self.app.lbl_result.cget("text"), "125")

        self.app._on_operator_click("×")
        self.root.update()
        self.assertEqual(self.app.lbl_expression.cget("text"), "125 × ")

        self.app._on_digit_click("8")
        self.root.update()
        self.assertEqual(self.app.lbl_result.cget("text"), "8")

        self.app._on_equal_click()
        self.root.update()
        self.assertEqual(self.app.lbl_result.cget("text"), "1,000")
        self.assertEqual(self.app.lbl_expression.cget("text"), "125 × 8 =")

        self.assertEqual(self.app.history.count(), 1)
        self.assertEqual(self.app.btn_history_toggle.cget("text"), "📜 History (1)")

    def test_division_by_zero_gui(self):
        self.app._on_digit_click("1")
        self.app._on_digit_click("0")
        self.app._on_operator_click("÷")
        self.app._on_digit_click("0")
        self.app._on_equal_click()
        self.root.update()
        self.assertEqual(self.app.lbl_result.cget("text"), "Cannot divide by zero")

    def test_history_toggle_gui(self):
        self.assertFalse(self.app.history_visible)
        self.app.toggle_history()
        self.root.update()
        self.assertTrue(self.app.history_visible)
        self.app.toggle_history()
        self.root.update()
        self.assertFalse(self.app.history_visible)


if __name__ == "__main__":
    unittest.main(verbosity=2)
