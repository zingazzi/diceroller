# /Users/marcozingoni/Playgound/Python/diceRoller/tests/test_roller.py
import pytest
from dice_roller.parser import DiceRoll
from dice_roller.roller import DiceRoller, RollResult


class TestDiceRoller:
    """Test cases for dice rolling logic"""

    def setup_method(self):
        """Set up test fixtures"""
        self.roller = DiceRoller()

    def test_single_die_roll(self):
        """Test rolling a single die"""
        dice_roll = DiceRoll(count=1, sides=20)
        result = self.roller.roll(dice_roll, "1d20")

        assert isinstance(result, RollResult)
        assert result.dice_roll == dice_roll
        assert len(result.individual_rolls) == 1
        assert 1 <= result.individual_rolls[0] <= 20
        assert result.total == result.individual_rolls[0]
        assert result.command == "1d20"

    def test_multiple_dice_roll(self):
        """Test rolling multiple dice"""
        dice_roll = DiceRoll(count=3, sides=6)
        result = self.roller.roll(dice_roll, "3d6")

        assert len(result.individual_rolls) == 3
        for roll in result.individual_rolls:
            assert 1 <= roll <= 6
        assert result.total == sum(result.individual_rolls)

    def test_roll_with_positive_modifier(self):
        """Test rolling with positive modifier"""
        dice_roll = DiceRoll(count=2, sides=8, modifier=3)
        result = self.roller.roll(dice_roll, "2d8+3")

        dice_sum = sum(result.individual_rolls)
        assert result.total == dice_sum + 3
        assert len(result.individual_rolls) == 2
        for roll in result.individual_rolls:
            assert 1 <= roll <= 8

    def test_roll_with_negative_modifier(self):
        """Test rolling with negative modifier"""
        dice_roll = DiceRoll(count=2, sides=10, modifier=-1)
        result = self.roller.roll(dice_roll, "2d10-1")

        dice_sum = sum(result.individual_rolls)
        assert result.total == dice_sum - 1
        for roll in result.individual_rolls:
            assert 1 <= roll <= 10

    def test_roll_distribution(self):
        """Test that rolls are within expected range over multiple attempts"""
        dice_roll = DiceRoll(count=1, sides=6)
        results = []

        # Roll 100 times to check distribution
        for _ in range(100):
            result = self.roller.roll(dice_roll, "1d6")
            results.append(result.individual_rolls[0])

        # Check all results are in valid range
        assert all(1 <= roll <= 6 for roll in results)

        # Check we get some variety (not all the same number)
        assert len(set(results)) > 1

    def test_large_dice_count(self):
        """Test rolling many dice at once"""
        dice_roll = DiceRoll(count=10, sides=6)
        result = self.roller.roll(dice_roll, "10d6")

        assert len(result.individual_rolls) == 10
        assert 10 <= result.total <= 60  # Min: 10*1, Max: 10*6
        for roll in result.individual_rolls:
            assert 1 <= roll <= 6

    def test_result_object_structure(self):
        """Test that RollResult contains all expected data"""
        dice_roll = DiceRoll(count=2, sides=4, modifier=1)
        result = self.roller.roll(dice_roll, "2d4+1")

        # Check all attributes exist and have correct types
        assert hasattr(result, 'dice_roll')
        assert hasattr(result, 'individual_rolls')
        assert hasattr(result, 'total')
        assert hasattr(result, 'command')

        assert isinstance(result.individual_rolls, list)
        assert isinstance(result.total, int)
        assert isinstance(result.command, str)
        assert result.dice_roll is dice_roll
