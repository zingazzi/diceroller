# /Users/marcozingoni/Playgound/Python/diceRoller/tests/test_cli.py
import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner
from dice_roller.cli import main, DiceRollerCLI
from dice_roller.history import RollHistory


class TestDiceRollerCLI:
    """Test cases for CLI functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.runner = CliRunner()
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        # Set environment variable to use test history file
        self.env = {'DICE_ROLLER_HISTORY': self.temp_file.name}

    def teardown_method(self):
        """Clean up temporary file"""
        Path(self.temp_file.name).unlink(missing_ok=True)

    def test_help_command(self):
        """Test help command output"""
        result = self.runner.invoke(main, ['--help'], env=self.env)
        assert result.exit_code == 0
        assert 'D&D Dice Roller CLI' in result.output
        assert 'Roll dice using standard D&D notation' in result.output

    def test_simple_dice_roll(self):
        """Test simple dice roll command"""
        result = self.runner.invoke(main, ['1d20'], env=self.env)
        assert result.exit_code == 0
        assert '🎲 1d20 →' in result.output

    def test_multiple_dice_roll(self):
        """Test multiple dice roll"""
        result = self.runner.invoke(main, ['3d6'], env=self.env)
        assert result.exit_code == 0
        assert '🎲 3d6 →' in result.output
        assert 'Rolls:' in result.output

    def test_dice_with_modifier(self):
        """Test dice roll with modifier"""
        result = self.runner.invoke(main, ['2d8+3'], env=self.env)
        assert result.exit_code == 0
        assert '🎲 2d8+3 →' in result.output
        assert 'Rolls:' in result.output

    def test_invalid_dice_notation(self):
        """Test invalid dice notation handling"""
        result = self.runner.invoke(main, ['invalid'], env=self.env)
        assert result.exit_code == 0
        assert '❌ Invalid dice notation' in result.output
        assert 'Valid formats:' in result.output

    def test_history_empty(self):
        """Test history command with no rolls"""
        result = self.runner.invoke(main, ['history'], env=self.env)
        assert result.exit_code == 0
        assert '📜 No roll history found' in result.output

    def test_history_with_rolls(self):
        """Test history command after making rolls"""
        # Make some rolls first
        self.runner.invoke(main, ['1d20'], env=self.env)
        self.runner.invoke(main, ['3d6'], env=self.env)

        # Check history
        result = self.runner.invoke(main, ['history'], env=self.env)
        assert result.exit_code == 0
        assert '📜 Roll History:' in result.output
        assert '🎲 1d20 →' in result.output
        assert '🎲 3d6 →' in result.output

    def test_history_with_limit(self):
        """Test history command with limit"""
        # Make multiple rolls
        for i in range(5):
            self.runner.invoke(main, [f'{i+1}d6'], env=self.env)

        # Check limited history
        result = self.runner.invoke(main, ['history', '--limit', '2'], env=self.env)
        assert result.exit_code == 0

        # Should only show last 2 rolls
        lines = result.output.split('\n')
        roll_lines = [line for line in lines if '🎲' in line]
        assert len(roll_lines) == 2

    def test_history_default_limit(self):
        """Test history command with default limit of 20"""
        # Make 25 rolls
        for i in range(25):
            self.runner.invoke(main, [f'1d{i+1}'], env=self.env)

        # Check default history (should show last 20)
        result = self.runner.invoke(main, ['history'], env=self.env)
        assert result.exit_code == 0

        lines = result.output.split('\n')
        roll_lines = [line for line in lines if '🎲' in line]
        assert len(roll_lines) == 20

    def test_history_show_all(self):
        """Test history command with --all flag"""
        # Make 25 rolls
        for i in range(25):
            self.runner.invoke(main, [f'1d{i+1}'], env=self.env)

        # Check all history
        result = self.runner.invoke(main, ['history', '--all'], env=self.env)
        assert result.exit_code == 0

        lines = result.output.split('\n')
        roll_lines = [line for line in lines if '🎲' in line]
        assert len(roll_lines) == 25

    def test_clear_history_with_confirmation(self):
        """Test clear history command with confirmation"""
        # Make a roll first
        self.runner.invoke(main, ['1d20'], env=self.env)

        # Clear with confirmation
        result = self.runner.invoke(main, ['clear'], input='y\n', env=self.env)
        assert result.exit_code == 0
        assert '🗑️  Roll history cleared' in result.output

        # Verify history is empty
        result = self.runner.invoke(main, ['history'], env=self.env)
        assert '📜 No roll history found' in result.output

    def test_clear_history_abort(self):
        """Test aborting clear history command"""
        # Make a roll first
        self.runner.invoke(main, ['1d20'], env=self.env)

        # Abort clear
        result = self.runner.invoke(main, ['clear'], input='n\n', env=self.env)
        assert result.exit_code == 1  # Aborted

        # Verify history still exists
        result = self.runner.invoke(main, ['history'], env=self.env)
        assert '🎲 1d20 →' in result.output


class TestDiceRollerCLIClass:
    """Test the DiceRollerCLI class directly"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()

        # Create CLI instance with custom history file
        self.cli = DiceRollerCLI()
        self.cli.history = RollHistory(self.temp_file.name)

    def teardown_method(self):
        """Clean up temporary file"""
        Path(self.temp_file.name).unlink(missing_ok=True)

    def test_roll_dice_valid(self):
        """Test roll_dice method with valid input"""
        # This should not raise an exception
        self.cli.roll_dice("1d20")

        # Check that history was updated
        history = self.cli.history.get_history()
        assert len(history) >= 1
        assert history[-1]['command'] == '1d20'

    def test_roll_dice_invalid(self):
        """Test roll_dice method with invalid input"""
        # This should handle the error gracefully
        self.cli.roll_dice("invalid")

        # History should remain empty
        history = self.cli.history.get_history()
        assert len(history) == 0

    def test_show_history_empty(self):
        """Test show_history with no rolls"""
        # Should not raise an exception
        self.cli.show_history()

    def test_show_history_with_data(self):
        """Test show_history with existing rolls"""
        # Add some rolls
        self.cli.roll_dice("1d20")
        self.cli.roll_dice("3d6")

        # Should not raise an exception
        self.cli.show_history()

        # Test with specific limit
        self.cli.show_history(limit=1)

        # Test with no limit (all history)
        self.cli.show_history(limit=None)

    def test_clear_history(self):
        """Test clear_history method"""
        # Add a roll
        self.cli.roll_dice("1d20")
        assert len(self.cli.history.get_history()) >= 1

        # Clear history
        self.cli.clear_history()
        assert len(self.cli.history.get_history()) == 0
