# /Users/marcozingoni/Playgound/Python/diceRoller/tests/test_history.py
import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from dice_roller.history import RollHistory
from dice_roller.parser import DiceRoll
from dice_roller.roller import RollResult


class TestRollHistory:
    """Test cases for roll history management"""

    def setup_method(self):
        """Set up test fixtures with temporary file"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.history = RollHistory(self.temp_file.name)

    def teardown_method(self):
        """Clean up temporary file"""
        Path(self.temp_file.name).unlink(missing_ok=True)

    def create_test_result(self, command="1d20", count=1, sides=20, modifier=0, rolls=None, total=None):
        """Helper to create test roll results"""
        dice_roll = DiceRoll(count=count, sides=sides, modifier=modifier)
        individual_rolls = rolls or [15]  # Default roll
        calculated_total = total if total is not None else sum(individual_rolls) + modifier

        return RollResult(
            dice_roll=dice_roll,
            individual_rolls=individual_rolls,
            total=calculated_total,
            command=command
        )

    def test_add_single_roll(self):
        """Test adding a single roll to history"""
        result = self.create_test_result()
        self.history.add_roll(result)

        history = self.history.get_history()
        assert len(history) == 1

        entry = history[0]
        assert entry['command'] == '1d20'
        assert entry['count'] == 1
        assert entry['sides'] == 20
        assert entry['modifier'] == 0
        assert entry['individual_rolls'] == [15]
        assert entry['total'] == 15
        assert 'timestamp' in entry

    def test_add_multiple_rolls(self):
        """Test adding multiple rolls to history"""
        results = [
            self.create_test_result("1d20", rolls=[18]),
            self.create_test_result("3d6", count=3, sides=6, rolls=[4, 3, 5]),
            self.create_test_result("2d8+3", count=2, sides=8, modifier=3, rolls=[6, 4])
        ]

        for result in results:
            self.history.add_roll(result)

        history = self.history.get_history()
        assert len(history) == 3

        # Check order (should be chronological)
        assert history[0]['command'] == '1d20'
        assert history[1]['command'] == '3d6'
        assert history[2]['command'] == '2d8+3'

    def test_get_history_with_limit(self):
        """Test getting limited history"""
        # Add 5 rolls
        for i in range(5):
            result = self.create_test_result(f"{i+1}d6")
            self.history.add_roll(result)

        # Get last 3 rolls
        recent_history = self.history.get_history(limit=3)
        assert len(recent_history) == 3

        # Should be the last 3 rolls
        assert recent_history[0]['command'] == '3d6'
        assert recent_history[1]['command'] == '4d6'
        assert recent_history[2]['command'] == '5d6'

    def test_get_history_default_limit(self):
        """Test default limit of 20 rolls"""
        # Add 25 rolls
        for i in range(25):
            result = self.create_test_result(f"1d{i+1}")
            self.history.add_roll(result)

        # Get history with default limit (should be 20)
        history = self.history.get_history()
        assert len(history) == 20

        # Should be the last 20 rolls
        assert history[0]['command'] == '1d6'  # 6th roll (25-20+1)
        assert history[-1]['command'] == '1d25'  # 25th roll

    def test_get_all_history(self):
        """Test getting all history with limit=None"""
        # Add 25 rolls
        for i in range(25):
            result = self.create_test_result(f"1d{i+1}")
            self.history.add_roll(result)

        # Get all history
        all_history = self.history.get_history(limit=None)
        assert len(all_history) == 25

        # Should include all rolls
        assert all_history[0]['command'] == '1d1'  # First roll
        assert all_history[-1]['command'] == '1d25'  # Last roll

    def test_clear_history(self):
        """Test clearing all history"""
        # Add some rolls
        for i in range(3):
            result = self.create_test_result(f"{i+1}d6")
            self.history.add_roll(result)

        assert len(self.history.get_history()) == 3

        # Clear history
        self.history.clear_history()
        assert len(self.history.get_history()) == 0

    def test_empty_history(self):
        """Test behavior with empty history"""
        history = self.history.get_history()
        assert history == []

        limited_history = self.history.get_history(limit=5)
        assert limited_history == []

    def test_persistence_across_instances(self):
        """Test that history persists across different instances"""
        # Add roll with first instance
        result = self.create_test_result("1d20")
        self.history.add_roll(result)

        # Create new instance with same file
        new_history = RollHistory(self.temp_file.name)
        history = new_history.get_history()

        assert len(history) == 1
        assert history[0]['command'] == '1d20'

    def test_timestamp_format(self):
        """Test that timestamps are properly formatted"""
        result = self.create_test_result()
        self.history.add_roll(result)

        history = self.history.get_history()
        timestamp_str = history[0]['timestamp']

        # Should be able to parse the timestamp
        timestamp = datetime.fromisoformat(timestamp_str)
        assert isinstance(timestamp, datetime)

    def test_corrupted_history_file(self):
        """Test handling of corrupted history file"""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully and return empty history
        history = self.history.get_history()
        assert history == []

        # Should be able to add new rolls
        result = self.create_test_result()
        self.history.add_roll(result)

        history = self.history.get_history()
        assert len(history) == 1

    def test_nonexistent_history_file(self):
        """Test behavior when history file doesn't exist"""
        nonexistent_file = "/tmp/nonexistent_history.json"
        Path(nonexistent_file).unlink(missing_ok=True)

        history = RollHistory(nonexistent_file)

        # Should return empty history
        assert history.get_history() == []

        # Should be able to add rolls
        result = self.create_test_result()
        history.add_roll(result)

        assert len(history.get_history()) == 1

        # Clean up
        Path(nonexistent_file).unlink(missing_ok=True)
