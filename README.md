# ⚡ SmartCalc – Python Calculator

> **Simple • Fast • Reliable**  
> A modern, secure, and beginner-friendly desktop calculator application built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)

---

## 📖 About The Project

**SmartCalc** is an intuitive, modern desktop calculator application built using Python 3 and Tkinter. It was designed from the ground up to combine a clean, sleek dark-themed user interface with robust mathematical evaluation and calculation history.

Unlike basic beginner calculator tutorials that use insecure `eval()` calls, **SmartCalc** implements an **Abstract Syntax Tree (AST)** safe evaluation engine, preventing code injection while providing mathematical precedence, percentage operations, sign toggling, interactive history, and keyboard shortcuts.

This project is structured for university/college mini-projects, lab presentations, viva evaluations, and portfolio showcases.

---

## ✨ Features

- 🎨 **Modern Dark UI**: Carefully crafted color scheme (`#111827`, `#1F2937`, `#2563EB`, `#14B8A6`, `#EF4444`) with interactive hover states and keypress feedback.
- ➗ **Standard Arithmetic Operations**:
  - Addition (`+`)
  - Subtraction (`−`)
  - Multiplication (`×`)
  - Division (`÷`)
  - Percentage (`%`)
  - Decimal support (`.`)
  - Positive/Negative sign toggle (`+/-`)
- 📜 **Session Calculation History**:
  - Expandable history drawer
  - Real-time history badge counter
  - Double-click any past calculation to instantly reuse the result
  - One-click **Clear History**
- ⌨ **Complete Keyboard Support**:
  - Full keypad input (`0-9`, `+`, `-`, `*`, `/`, `%`, `.`)
  - `Enter` or `=` to calculate
  - `Backspace` to delete the last digit
  - `Escape` or `C` to clear
  - `H` to toggle calculation history
- 🛡 **Secure AST Evaluation Engine**:
  - Evaluates formulas using Python's standard `ast` module.
  - Zero vulnerability to arbitrary code execution (no dangerous `eval()`).
- ⚠️ **Graceful Error Handling**:
  - Division by zero protection (`Cannot divide by zero`)
  - Overflow and syntax validation without application crashes.
- 📦 **Zero External Dependencies**:
  - Runs natively on any standard Python 3.8+ installation.

---

## 🛠 Technologies Used

- **Language:** Python 3.8+
- **GUI Toolkit:** Tkinter (Python Standard Library)
- **Parser & Math Engine:** `ast` & `operator` (Python Standard Library)
- **Data & History:** Python Standard Data Structures & `datetime`
- **Testing Framework:** `unittest` (Python Standard Library)

---

## 📂 Project Structure

```text
SmartCalc/
│
├── main.py              # Application entry point & Tkinter GUI Controller
├── calculator.py        # Safe AST mathematical evaluation engine & state machine
├── history.py           # Session history storage, retrieval, and management
├── test_smartcalc.py    # Unit tests for calculation engine, security, and history
├── test_gui.py          # Automated GUI test suite for Tkinter components
├── requirements.txt     # Dependency information (pure standard library)
└── README.md            # Comprehensive project documentation
```

### Module Responsibilities:

| File | Purpose |
| :--- | :--- |
| **`main.py`** | Builds the desktop GUI window, manages widget layouts, handles hover effects, binds keyboard events, and connects user actions to the calculator engine. |
| **`calculator.py`** | Contains `SafeEvaluator` (AST arithmetic parser) and `CalculatorEngine` (manages active digits, chaining operations, and output formatting). |
| **`history.py`** | Implements `HistoryManager` and `HistoryItem` to record calculations, maintain session memory, and support result reloading. |
| **`test_smartcalc.py`** | Comprehensive automated test suite validating math accuracy, operator precedence, percentage, and sandbox security. |
| **`test_gui.py`** | Headless automated test verifying Tkinter widget creation, button events, display updates, and history drawer toggling. |

---

## 🚀 Installation & Running

### Prerequisites
Make sure you have Python 3.8 or higher installed on your computer.

### Step 1: Clone or Download the Project
```bash
git clone https://github.com/your-username/SmartCalc.git
cd SmartCalc
```

### Step 2: Run the Calculator
No external package installation is required! Simply run:

```bash
python main.py
```

---

## 🎯 How to Use

1. **Enter Numbers**: Click the numeric buttons (`0-9`) or type them on your keyboard.
2. **Select an Operation**: Click `+`, `−`, `×`, or `÷` (or press `+`, `-`, `*`, `/` on your keyboard).
3. **Chain Calculations**: Enter the next operand and press another operator to continue chaining calculations.
4. **Calculate Result**: Click `=` or press `Enter` to see the calculated result in the main display.
5. **Toggle Positive/Negative**: Click `+/-` to switch the sign of the active number.
6. **Calculate Percentages**: Enter a number (e.g. `100`) and click `%` to instantly get its percentage (`1`).
7. **View History**: Click the **📜 History** button (or press `H`) in the top header to slide out your session history.
8. **Reuse Past Results**: In the history panel, **double-click** any calculation record to paste that result directly back into your active calculator!
9. **Clear History**: Click **🗑 Clear History** to reset session records.
10. **Clear / Reset**: Click `C` or press `Escape` to reset the calculator.

---

## ⌨ Keyboard Shortcuts Reference

| Keyboard Key | Calculator Action | Description |
| :--- | :--- | :--- |
| `0` – `9` | Digit Entry | Appends digit to the active entry |
| `+` | Addition | Adds active operand |
| `-` | Subtraction | Subtracts active operand |
| `*` or `x` | Multiplication | Multiplies active operand |
| `/` | Division | Divides active operand |
| `%` | Percentage | Converts active number to percentage (`x / 100`) |
| `.` or `,` | Decimal Point | Appends decimal place |
| `Enter` / `Return` / `=` | Equals | Evaluates the active formula |
| `Backspace` / `Delete` | Backspace (`⌫`) | Deletes the last entered character |
| `Escape` / `c` / `C` | Clear (`C`) | Resets active display and engine state |
| `h` / `H` | Toggle History | Opens or closes the calculation history drawer |

---

## 🧪 Testing & Verification

SmartCalc includes a full automated test suite covering unit calculations, AST security, edge cases, and GUI operations.

### Run All Unit & Security Tests:
```bash
python test_smartcalc.py
```

### Run GUI Verification Tests:
```bash
python test_gui.py
```

### Verified Test Cases:
- ✅ **Addition:** `10 + 20 = 30`
- ✅ **Subtraction:** `50 - 15 = 35`
- ✅ **Multiplication:** `8 × 7 = 56`
- ✅ **Division:** `100 ÷ 4 = 25`
- ✅ **Decimal Math:** `10.5 + 2.5 = 13`
- ✅ **Precedence (PEMDAS):** `50 + 25 × 2 = 100`
- ✅ **Percentage:** `100 % = 1`, `50 % = 0.5`
- ✅ **Division by Zero:** `10 ÷ 0` displays `"Cannot divide by zero"` without crashing
- ✅ **AST Security:** Injection strings such as `__import__('os')` or `eval()` are rejected
- ✅ **History Management:** Add, retrieve, formatted display, and clear operations

---

## 🔒 Security Architecture

Many simple Python calculators use `eval(user_input)`, which introduces severe Remote Code Execution (RCE) vulnerabilities.

**SmartCalc** implements an AST (Abstract Syntax Tree) validator in `calculator.py`:

```python
# Safe AST evaluation restricts syntax to allowed mathematical operations only:
_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}
```

Any AST node that represents function calls (`ast.Call`), variable lookups (`ast.Name`), or module imports is rejected at the parser level before execution.

---

## 🔮 Future Improvements

Here are ideas and features that can be added in future versions:

1. **Scientific Calculator Mode**: Support for trigonometric functions ($\sin, \cos, \tan$), logarithms ($\log, \ln$), powers ($x^y$), and square roots ($\sqrt{x}$).
2. **Light / Dark Theme Toggle**: An interactive theme switch for users who prefer a bright aesthetic.
3. **Persistent History Storage**: Save calculation history to a local SQLite database or JSON file between sessions.
4. **Currency & Unit Converter**: Integrated real-time conversion for currencies, weights, lengths, and temperatures.
5. **Calculation Export**: Export history logs directly to `.csv` or `.txt` files.
6. **Mobile / Cross-Platform Port**: Packaging for Android/iOS using Kivy or BeeWare.

---

## 👤 Author & Acknowledgments

- **Project:** SmartCalc – Python Calculator
- **Built for:** Python Desktop Application / College Mini-Project / Portfolio
- **License:** Open-source under the [MIT License](LICENSE)
