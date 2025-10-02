# /Users/marcozingoni/Playgound/Python/diceRoller/dice_roller/history.py
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from .roller import RollResult


class RollHistory:
    """Manages roll history storage and retrieval"""

    def __init__(self, history_file: str = None):
        if history_file is None:
            # Check environment variable first
            env_file = os.getenv('DICE_ROLLER_HISTORY')
            if env_file:
                self.history_file = Path(env_file)
            else:
                home = Path.home()
                self.history_file = home / '.dice_roller_history.json'
        else:
            self.history_file = Path(history_file)

    def add_roll(self, result: RollResult) -> None:
        """Add a roll result to history"""
        history = self._load_history()

        roll_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': result.command,
            'count': result.dice_roll.count,
            'sides': result.dice_roll.sides,
            'modifier': result.dice_roll.modifier,
            'individual_rolls': result.individual_rolls,
            'total': result.total
        }

        history.append(roll_entry)
        self._save_history(history)

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get roll history, limited to recent entries (default: last 20)"""
        history = self._load_history()

        if limit is None:
            return history
        return history[-limit:]

    def clear_history(self) -> None:
        """Clear all roll history"""
        self._save_history([])

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from file"""
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't write history
