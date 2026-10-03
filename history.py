"""
history.py - Calculation history manager for SmartCalc.

Maintains an in-memory session history of calculations, allowing users
to view past operations, reload results, and clear history.
"""

from datetime import datetime
from typing import List, Dict, Optional


class HistoryItem:
    """Represents a single calculation entry in history."""

    def __init__(self, expression: str, result: str):
        self.expression: str = expression
        self.result: str = result
        self.timestamp: str = datetime.now().strftime("%H:%M:%S")

    @property
    def display_text(self) -> str:
        """Returns standard readable string e.g. '25 + 25 = 50'"""
        return f"{self.expression} = {self.result}"

    def to_dict(self) -> Dict[str, str]:
        """Converts entry to dictionary representation."""
        return {
            "expression": self.expression,
            "result": self.result,
            "timestamp": self.timestamp,
            "display": self.display_text,
        }


class HistoryManager:
    """
    Manages session-based calculation records.
    Provides methods to store, retrieve, format, and clear history.
    """

    def __init__(self, max_entries: int = 100):
        self.max_entries: int = max_entries
        self._history: List[HistoryItem] = []

    def add_entry(self, expression: str, result: str) -> HistoryItem:
        """
        Records a new calculation result to session history.

        Args:
            expression: The arithmetic formula (e.g. '125 × 8')
            result: The evaluated result (e.g. '1,000')

        Returns:
            The created HistoryItem object
        """
        # Clean expression if it has trailing '='
        clean_expr = expression.rstrip("=").strip()
        item = HistoryItem(clean_expr, str(result))

        self._history.append(item)

        # Enforce maximum capacity
        if len(self._history) > self.max_entries:
            self._history.pop(0)

        return item

    def get_all(self, reverse: bool = True) -> List[HistoryItem]:
        """
        Returns all stored history items.

        Args:
            reverse: If True, returns newest records first.
        """
        if reverse:
            return list(reversed(self._history))
        return list(self._history)

    def get_item(self, index: int) -> Optional[HistoryItem]:
        """Retrieves a history item at a specific index."""
        if 0 <= index < len(self._history):
            return self._history[index]
        return None

    def clear(self) -> None:
        """Clears all session history entries."""
        self._history.clear()

    def count(self) -> int:
        """Returns total number of calculations stored."""
        return len(self._history)

    def is_empty(self) -> bool:
        """Checks if history is currently empty."""
        return len(self._history) == 0

    def export_as_text(self) -> str:
        """Exports the entire calculation history as a formatted text block."""
        if self.is_empty():
            return "No calculations recorded yet."

        lines = ["=== SmartCalc History ==="]
        for item in self._history:
            lines.append(f"[{item.timestamp}] {item.expression} = {item.result}")
        return "\n".join(lines)
