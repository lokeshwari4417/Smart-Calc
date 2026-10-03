"""
main.py - Entry point and Graphical User Interface for SmartCalc.

Built with Tkinter and pure Python standard library.
Features a modern dark theme, animated-feeling hover states, interactive history,
and comprehensive keyboard shortcuts.
"""

import sys
import tkinter as tk
from tkinter import font as tkfont
from typing import Dict, Any, Optional

from calculator import CalculatorEngine
from history import HistoryManager


class SmartCalcApp:
    """
    Main GUI Application controller for SmartCalc.
    """

    # Color Palette Tokens
    BG_COLOR = "#111827"           # Tailwind Gray 900 (Main Window)
    DISPLAY_BG = "#1F2937"         # Tailwind Gray 800 (Display Screen)
    CARD_BG = "#1E293B"            # Slate 800 (Card Containers)
    BORDER_COLOR = "#374151"       # Slate 700 (Subtle borders)

    # Button Colors
    BTN_NUM_BG = "#374151"         # Slate 700
    BTN_NUM_HOVER = "#4B5563"      # Slate 600
    BTN_NUM_ACTIVE = "#1F2937"

    BTN_OP_BG = "#2563EB"          # Blue 600
    BTN_OP_HOVER = "#3B82F6"       # Blue 500
    BTN_OP_ACTIVE = "#1D4ED8"      # Blue 700

    BTN_EQ_BG = "#14B8A6"          # Teal 500
    BTN_EQ_HOVER = "#2DD4BF"       # Teal 400
    BTN_EQ_ACTIVE = "#0F766E"      # Teal 700

    BTN_CLR_BG = "#EF4444"         # Red 500
    BTN_CLR_HOVER = "#F87171"      # Red 400
    BTN_CLR_ACTIVE = "#DC2626"     # Red 600

    BTN_UTIL_BG = "#4B5563"        # Gray 600
    BTN_UTIL_HOVER = "#6B7280"     # Gray 500
    BTN_UTIL_ACTIVE = "#374151"

    # Text Colors
    TEXT_MAIN = "#FFFFFF"          # Pure White
    TEXT_MUTED = "#9CA3AF"         # Gray 400
    TEXT_ACCENT = "#38BDF8"        # Sky 400
    TEXT_ERROR = "#F87171"         # Red 400

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SmartCalc – Python Calculator")
        self.root.configure(bg=self.BG_COLOR)

        # Base Dimensions
        self.base_width = 380
        self.history_width = 280
        self.height = 620
        self.history_visible = False

        # Core Engines
        self.engine = CalculatorEngine()
        self.history = HistoryManager()

        # Button lookup for keyboard flash animations
        self.button_widgets: Dict[str, tk.Button] = {}

        # Set Fonts & Window Geometry
        self._setup_fonts()
        self._center_window(self.base_width, self.height)
        self.root.minsize(360, 580)

        # Build UI Components
        self._create_main_layout()
        self._create_header()
        self._create_display()
        self._create_keypad()
        self._create_history_panel()
        self._create_footer()

        # Bind Keyboard Events
        self._bind_keyboard_events()

        # Initial Display Sync
        self._update_display()

    def _setup_fonts(self):
        """Initializes modern, clean system fonts with fallbacks."""
        primary_font = "Segoe UI"
        if sys.platform == "darwin":
            primary_font = ".AppleSystemUIFont"
        elif not sys.platform.startswith("win"):
            primary_font = "DejaVu Sans"

        self.font_title = tkfont.Font(family=primary_font, size=14, weight="bold")
        self.font_subtitle = tkfont.Font(family=primary_font, size=8, weight="normal")
        self.font_expr = tkfont.Font(family=primary_font, size=11, weight="normal")
        self.font_result = tkfont.Font(family=primary_font, size=24, weight="bold")
        self.font_result_small = tkfont.Font(family=primary_font, size=17, weight="bold")
        self.font_btn = tkfont.Font(family=primary_font, size=13, weight="bold")
        self.font_btn_op = tkfont.Font(family=primary_font, size=14, weight="bold")
        self.font_history = tkfont.Font(family=primary_font, size=9, weight="normal")
        self.font_history_bold = tkfont.Font(family=primary_font, size=10, weight="bold")
        self.font_footer = tkfont.Font(family=primary_font, size=8, weight="normal")

    def _center_window(self, width: int, height: int):
        """Centers the application window on screen."""
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_main_layout(self):
        """Creates the container frames for the calculator and optional history drawer."""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=1)

        # Calculator Main Frame (Left)
        self.calc_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=16, pady=12)
        self.calc_frame.grid(row=0, column=0, sticky="nsew")

        self.calc_frame.grid_columnconfigure(0, weight=1)
        self.calc_frame.grid_rowconfigure(0, weight=0)  # Header
        self.calc_frame.grid_rowconfigure(1, weight=0)  # Display
        self.calc_frame.grid_rowconfigure(2, weight=1)  # Keypad
        self.calc_frame.grid_rowconfigure(3, weight=0)  # Footer

        # History Frame (Right, expandable)
        self.history_frame = tk.Frame(self.root, bg=self.DISPLAY_BG, padx=12, pady=12, highlightthickness=1, highlightbackground=self.BORDER_COLOR)

    def _create_header(self):
        """Creates the top branding header with title, subtitle, and history toggle."""
        header_frame = tk.Frame(self.calc_frame, bg=self.BG_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        # Title & Subtitle container
        title_box = tk.Frame(header_frame, bg=self.BG_COLOR)
        title_box.grid(row=0, column=0, sticky="w")

        lbl_title = tk.Label(
            title_box,
            text="⚡ SmartCalc",
            font=self.font_title,
            fg=self.TEXT_MAIN,
            bg=self.BG_COLOR,
            anchor="w"
        )
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(
            title_box,
            text="Simple • Fast • Reliable",
            font=self.font_subtitle,
            fg=self.TEXT_ACCENT,
            bg=self.BG_COLOR,
            anchor="w"
        )
        lbl_sub.pack(anchor="w")

        # History Toggle Button
        self.btn_history_toggle = tk.Button(
            header_frame,
            text="📜 History",
            font=self.font_subtitle,
            fg=self.TEXT_MAIN,
            bg=self.BTN_UTIL_BG,
            activebackground=self.BTN_UTIL_ACTIVE,
            activeforeground=self.TEXT_MAIN,
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.toggle_history
        )
        self.btn_history_toggle.grid(row=0, column=1, sticky="e")
        self._add_hover_effect(self.btn_history_toggle, self.BTN_UTIL_BG, self.BTN_UTIL_HOVER)

    def _create_display(self):
        """Creates the sleek calculator screen showing live formula and result."""
        self.display_container = tk.Frame(
            self.calc_frame,
            bg=self.DISPLAY_BG,
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=self.BORDER_COLOR
        )
        self.display_container.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.display_container.grid_columnconfigure(0, weight=1)

        # Expression label (top, smaller font, muted color)
        self.lbl_expression = tk.Label(
            self.display_container,
            text="",
            font=self.font_expr,
            fg=self.TEXT_MUTED,
            bg=self.DISPLAY_BG,
            anchor="e",
            height=1
        )
        self.lbl_expression.grid(row=0, column=0, sticky="ew")

        # Result / Active Entry label (bottom, large bold font)
        self.lbl_result = tk.Label(
            self.display_container,
            text="0",
            font=self.font_result,
            fg=self.TEXT_MAIN,
            bg=self.DISPLAY_BG,
            anchor="e",
            height=1
        )
        self.lbl_result.grid(row=1, column=0, sticky="ew", pady=(4, 0))

    def _create_keypad(self):
        """Creates the 5x4 button grid layout according to specifications."""
        keypad_frame = tk.Frame(self.calc_frame, bg=self.BG_COLOR)
        keypad_frame.grid(row=2, column=0, sticky="nsew")

        for c in range(4):
            keypad_frame.grid_columnconfigure(c, weight=1, uniform="key_col")
        for r in range(5):
            keypad_frame.grid_rowconfigure(r, weight=1, uniform="key_row")

        buttons = [
            ("C", 0, 0, "clear", self._on_clear_click),
            ("⌫", 0, 1, "util", self._on_backspace_click),
            ("%", 0, 2, "util", self._on_percent_click),
            ("÷", 0, 3, "op", lambda: self._on_operator_click("÷")),

            ("7", 1, 0, "num", lambda: self._on_digit_click("7")),
            ("8", 1, 1, "num", lambda: self._on_digit_click("8")),
            ("9", 1, 2, "num", lambda: self._on_digit_click("9")),
            ("×", 1, 3, "op", lambda: self._on_operator_click("×")),

            ("4", 2, 0, "num", lambda: self._on_digit_click("4")),
            ("5", 2, 1, "num", lambda: self._on_digit_click("5")),
            ("6", 2, 2, "num", lambda: self._on_digit_click("6")),
            ("−", 2, 3, "op", lambda: self._on_operator_click("−")),

            ("1", 3, 0, "num", lambda: self._on_digit_click("1")),
            ("2", 3, 1, "num", lambda: self._on_digit_click("2")),
            ("3", 3, 2, "num", lambda: self._on_digit_click("3")),
            ("+", 3, 3, "op", lambda: self._on_operator_click("+")),

            ("+/-", 4, 0, "num", self._on_sign_click),
            ("0", 4, 1, "num", lambda: self._on_digit_click("0")),
            (".", 4, 2, "num", self._on_decimal_click),
            ("=", 4, 3, "eq", self._on_equal_click),
        ]

        for text, row, col, btn_type, action in buttons:
            btn = self._build_button(keypad_frame, text, btn_type, action)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.button_widgets[text] = btn

    def _build_button(self, parent: tk.Widget, text: str, btn_type: str, command: Any) -> tk.Button:
        """Constructs a beautifully styled Tkinter button with specific type colors."""
        if btn_type == "clear":
            bg = self.BTN_CLR_BG
            hover_bg = self.BTN_CLR_HOVER
            active_bg = self.BTN_CLR_ACTIVE
            fg = self.TEXT_MAIN
            font = self.font_btn
        elif btn_type == "op":
            bg = self.BTN_OP_BG
            hover_bg = self.BTN_OP_HOVER
            active_bg = self.BTN_OP_ACTIVE
            fg = self.TEXT_MAIN
            font = self.font_btn_op
        elif btn_type == "eq":
            bg = self.BTN_EQ_BG
            hover_bg = self.BTN_EQ_HOVER
            active_bg = self.BTN_EQ_ACTIVE
            fg = self.TEXT_MAIN
            font = self.font_btn_op
        elif btn_type == "util":
            bg = self.BTN_UTIL_BG
            hover_bg = self.BTN_UTIL_HOVER
            active_bg = self.BTN_UTIL_ACTIVE
            fg = self.TEXT_MAIN
            font = self.font_btn
        else:
            bg = self.BTN_NUM_BG
            hover_bg = self.BTN_NUM_HOVER
            active_bg = self.BTN_NUM_ACTIVE
            fg = self.TEXT_MAIN
            font = self.font_btn

        btn = tk.Button(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=self.TEXT_MAIN,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command
        )

        self._add_hover_effect(btn, bg, hover_bg)
        return btn

    def _add_hover_effect(self, widget: tk.Widget, default_bg: str, hover_bg: str):
        """Adds smooth mouse hover highlight to buttons."""
        def on_enter(e):
            if widget["state"] != "disabled":
                widget.configure(bg=hover_bg)

        def on_leave(e):
            if widget["state"] != "disabled":
                widget.configure(bg=default_bg)

        widget.bind("<Enter>", on_enter, add="+")
        widget.bind("<Leave>", on_leave, add="+")

    def _create_history_panel(self):
        """Constructs the slide-out history panel with calculation list and controls."""
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(1, weight=1)

        hist_header = tk.Frame(self.history_frame, bg=self.DISPLAY_BG)
        hist_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        hist_header.grid_columnconfigure(0, weight=1)

        lbl_hist_title = tk.Label(
            hist_header,
            text="Calculation History",
            font=self.font_history_bold,
            fg=self.TEXT_MAIN,
            bg=self.DISPLAY_BG
        )
        lbl_hist_title.grid(row=0, column=0, sticky="w")

        btn_close = tk.Button(
            hist_header,
            text="✕",
            font=self.font_subtitle,
            fg=self.TEXT_MUTED,
            bg=self.DISPLAY_BG,
            activebackground=self.BTN_CLR_BG,
            activeforeground=self.TEXT_MAIN,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.toggle_history
        )
        btn_close.grid(row=0, column=1, sticky="e")

        list_container = tk.Frame(self.history_frame, bg=self.CARD_BG, highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        list_container.grid(row=1, column=0, sticky="nsew")
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(0, weight=1)

        self.history_listbox = tk.Listbox(
            list_container,
            bg=self.CARD_BG,
            fg=self.TEXT_MAIN,
            selectbackground=self.BTN_OP_BG,
            selectforeground=self.TEXT_MAIN,
            font=self.font_history,
            relief="flat",
            bd=0,
            activestyle="none",
            highlightthickness=0
        )
        self.history_listbox.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        self.history_listbox.bind("<Double-Button-1>", self._on_history_item_selected)

        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.history_listbox.yview, bg=self.DISPLAY_BG)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        lbl_hint = tk.Label(
            self.history_frame,
            text="💡 Tip: Double-click an item to reuse",
            font=self.font_footer,
            fg=self.TEXT_MUTED,
            bg=self.DISPLAY_BG
        )
        lbl_hint.grid(row=2, column=0, sticky="w", pady=(6, 4))

        self.btn_clear_history = tk.Button(
            self.history_frame,
            text="🗑 Clear History",
            font=self.font_history_bold,
            bg=self.BTN_CLR_BG,
            fg=self.TEXT_MAIN,
            activebackground=self.BTN_CLR_ACTIVE,
            activeforeground=self.TEXT_MAIN,
            relief="flat",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self._on_clear_history_click
        )
        self.btn_clear_history.grid(row=3, column=0, sticky="ew", pady=(4, 0))
        self._add_hover_effect(self.btn_clear_history, self.BTN_CLR_BG, self.BTN_CLR_HOVER)

    def _create_footer(self):
        """Creates subtle bottom bar indicating keyboard readiness."""
        footer_frame = tk.Frame(self.calc_frame, bg=self.BG_COLOR)
        footer_frame.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        footer_frame.grid_columnconfigure(0, weight=1)

        lbl_footer = tk.Label(
            footer_frame,
            text="⌨ Keyboard Enabled • Esc=Clear • Enter=Equals",
            font=self.font_footer,
            fg=self.TEXT_MUTED,
            bg=self.BG_COLOR
        )
        lbl_footer.grid(row=0, column=0)

    def _update_display(self):
        """Synchronizes GUI labels with the calculator engine's internal state."""
        self.lbl_expression.config(text=self.engine.expression)

        if self.engine.error_message:
            self.lbl_result.config(
                text=self.engine.error_message,
                fg=self.TEXT_ERROR,
                font=self.font_result_small
            )
        else:
            display_text = self.engine.current_entry
            if len(display_text) > 12:
                self.lbl_result.config(text=display_text, fg=self.TEXT_MAIN, font=self.font_result_small)
            else:
                self.lbl_result.config(text=display_text, fg=self.TEXT_MAIN, font=self.font_result)

        hist_count = self.history.count()
        if hist_count > 0:
            self.btn_history_toggle.config(text=f"📜 History ({hist_count})")
        else:
            self.btn_history_toggle.config(text="📜 History")

    def _refresh_history_listbox(self):
        """Re-populates the history listbox widget."""
        self.history_listbox.delete(0, tk.END)
        items = self.history.get_all(reverse=True)
        if not items:
            self.history_listbox.insert(tk.END, "  (No calculations yet)")
        else:
            for item in items:
                self.history_listbox.insert(tk.END, f"  {item.expression} = {item.result}")

    def toggle_history(self):
        """Toggles the visibility of the side history drawer."""
        self.history_visible = not self.history_visible

        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()

        if self.history_visible:
            self.history_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)
            self._refresh_history_listbox()
            new_width = self.base_width + self.history_width
            self.root.geometry(f"{new_width}x{self.height}+{current_x}+{current_y}")
        else:
            self.history_frame.grid_forget()
            self.root.geometry(f"{self.base_width}x{self.height}+{current_x}+{current_y}")

    def _on_digit_click(self, digit: str):
        self._flash_button(digit)
        self.engine.input_digit(digit)
        self._update_display()

    def _on_decimal_click(self):
        self._flash_button(".")
        self.engine.input_decimal()
        self._update_display()

    def _on_operator_click(self, op: str):
        self._flash_button(op)
        self.engine.input_operator(op)
        self._update_display()

    def _on_sign_click(self):
        self._flash_button("+/-")
        self.engine.toggle_sign()
        self._update_display()

    def _on_percent_click(self):
        self._flash_button("%")
        self.engine.apply_percentage()
        self._update_display()

    def _on_backspace_click(self):
        self._flash_button("⌫")
        self.engine.backspace()
        self._update_display()

    def _on_clear_click(self):
        self._flash_button("C")
        self.engine.clear_all()
        self._update_display()

    def _on_equal_click(self):
        self._flash_button("=")
        raw_expr, result, error = self.engine.calculate()

        if result is not None and raw_expr is not None:
            self.history.add_entry(raw_expr, result)
            if self.history_visible:
                self._refresh_history_listbox()

        self._update_display()

    def _on_clear_history_click(self):
        self.history.clear()
        self._refresh_history_listbox()
        self._update_display()

    def _on_history_item_selected(self, event):
        """Loads a selected history calculation back into the calculator."""
        selection = self.history_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        items = self.history.get_all(reverse=True)
        if 0 <= index < len(items):
            item = items[index]
            self.engine.clear_all()
            self.engine.current_entry = item.result
            self.engine.is_new_calculation = True
            self.engine.expression = f"Ans: {item.expression} ="
            self._update_display()

    def _flash_button(self, symbol: str):
        """Provides brief visual feedback when a button or key is activated."""
        btn = self.button_widgets.get(symbol)
        if btn:
            orig_bg = btn.cget("bg")
            btn.config(bg="#FCD34D")
            self.root.after(80, lambda: btn.config(bg=orig_bg))

    def _bind_keyboard_events(self):
        """Binds all standard keyboard events for mouse-free calculation."""
        self.root.bind("<Key>", self._handle_key_press)

    def _handle_key_press(self, event: tk.Event):
        """Dispatches keyboard events to appropriate calculator actions."""
        key = event.char
        keysym = event.keysym

        if key in "0123456789":
            self._on_digit_click(key)
            return "break"

        if key == "+":
            self._on_operator_click("+")
            return "break"
        elif key == "-":
            self._on_operator_click("−")
            return "break"
        elif key in ("*", "x", "X"):
            self._on_operator_click("×")
            return "break"
        elif key == "/":
            self._on_operator_click("÷")
            return "break"
        elif key == "%":
            self._on_percent_click()
            return "break"
        elif key in (".", ","):
            self._on_decimal_click()
            return "break"

        elif keysym in ("Return", "KP_Enter", "equal") or key == "=":
            self._on_equal_click()
            return "break"

        elif keysym in ("BackSpace", "Delete"):
            self._on_backspace_click()
            return "break"

        elif keysym == "Escape" or key.lower() == "c":
            self._on_clear_click()
            return "break"

        elif key.lower() == "h":
            self.toggle_history()
            return "break"


def main():
    root = tk.Tk()
    app = SmartCalcApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
