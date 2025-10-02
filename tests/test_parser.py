# /Users/marcozingoni/Playgound/Python/diceRoller/tests/test_parser.py
import pytest
from dice_roller.parser import DiceParser, DiceRoll


class TestDiceParser:
    """Test cases for dice notation parser"""

    def test_simple_dice_notation(self):
        """Test basic dice notation parsing"""
        result = DiceParser.parse("1d20")
        assert result is not None
        assert result.count == 1
        assert result.sides == 20
        assert result.modifier == 0

    def test_multiple_dice(self):
        """Test multiple dice parsing"""
        result = DiceParser.parse("3d6")
        assert result is not None
        assert result.count == 3
        assert result.sides == 6
        assert result.modifier == 0

    def test_positive_modifier(self):
        """Test dice with positive modifier"""
        result = DiceParser.parse("4d8+3")
        assert result is not None
        assert result.count == 4
        assert result.sides == 8
        assert result.modifier == 3

    def test_negative_modifier(self):
        """Test dice with negative modifier"""
        result = DiceParser.parse("2d10-1")
        assert result is not None
        assert result.count == 2
        assert result.sides == 10
        assert result.modifier == -1

    def test_case_insensitive(self):
        """Test case insensitive parsing"""
        result = DiceParser.parse("1D20")
        assert result is not None
        assert result.count == 1
        assert result.sides == 20

    def test_whitespace_handling(self):
        """Test parsing with whitespace"""
        result = DiceParser.parse(" 3d6 + 2 ")
        assert result is not None
        assert result.count == 3
        assert result.sides == 6
        assert result.modifier == 2

    def test_large_numbers(self):
        """Test parsing with large numbers"""
        result = DiceParser.parse("10d100+50")
        assert result is not None
        assert result.count == 10
        assert result.sides == 100
        assert result.modifier == 50

    def test_invalid_formats(self):
        """Test invalid dice notation formats"""
        invalid_inputs = [
            "",
            "d20",
            "1d",
            "abc",
            "1d20+",
            "1d20++3",
            "0d20",
            "1d0",
            "-1d20",
            "1d-20",
            "1.5d20",
            "1d20.5",
            "1d20+3.5"
        ]

        for invalid_input in invalid_inputs:
            result = DiceParser.parse(invalid_input)
            assert result is None, f"Expected None for input: {invalid_input}"

    def test_edge_cases(self):
        """Test edge cases"""
        # Minimum valid values
        result = DiceParser.parse("1d1")
        assert result is not None
        assert result.count == 1
        assert result.sides == 1

        # Zero modifier
        result = DiceParser.parse("1d20+0")
        assert result is not None
        assert result.modifier == 0
