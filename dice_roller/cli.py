# /Users/marcozingoni/Playgound/Python/diceRoller/dice_roller/cli.py
import click
from datetime import datetime
from .parser import DiceParser
from .roller import DiceRoller
from .history import RollHistory


class DiceRollerCLI:
    """Main CLI application for dice rolling"""

    def __init__(self):
        self.parser = DiceParser()
        self.roller = DiceRoller()
        self.history = RollHistory()

    def roll_dice(self, dice_string: str) -> None:
        """Roll dice from string notation and display results"""
        dice_roll = self.parser.parse(dice_string)

        if dice_roll is None:
            click.echo(f"❌ Invalid dice notation: {dice_string}")
            click.echo("Valid formats: 1d20, 3d6, 4d8+3, 2d10-1")
            return

        result = self.roller.roll(dice_roll, dice_string)
        self.history.add_roll(result)

        # Display results
        self._display_roll_result(result)

    def show_history(self, limit: int = 20) -> None:
        """Display roll history (default: last 20 rolls)"""
        history = self.history.get_history(limit)

        if not history:
            click.echo("📜 No roll history found.")
            return

        click.echo("📜 Roll History:")
        click.echo("=" * 50)

        for entry in history:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            click.echo(f"🕐 {time_str}")
            click.echo(f"🎲 {entry['command']} → {entry['total']}")

            if len(entry['individual_rolls']) > 1:
                rolls_str = " + ".join(map(str, entry['individual_rolls']))
                if entry['modifier'] != 0:
                    modifier_str = f" {entry['modifier']:+d}" if entry['modifier'] != 0 else ""
                    click.echo(f"   Rolls: [{rolls_str}]{modifier_str}")
                else:
                    click.echo(f"   Rolls: [{rolls_str}]")

            click.echo()

    def clear_history(self) -> None:
        """Clear all roll history"""
        self.history.clear_history()
        click.echo("🗑️  Roll history cleared.")

    def _display_roll_result(self, result) -> None:
        """Display a single roll result with formatting"""
        dice_roll = result.dice_roll

        # Main result
        click.echo(f"🎲 {result.command} → {result.total}")

        # Show individual rolls if multiple dice
        if len(result.individual_rolls) > 1:
            rolls_str = " + ".join(map(str, result.individual_rolls))
            dice_sum = sum(result.individual_rolls)

            if dice_roll.modifier != 0:
                modifier_str = f" {dice_roll.modifier:+d}"
                click.echo(f"   Rolls: [{rolls_str}] = {dice_sum}{modifier_str} = {result.total}")
            else:
                click.echo(f"   Rolls: [{rolls_str}] = {result.total}")


# CLI Commands
@click.group(invoke_without_command=True, no_args_is_help=True)
@click.argument('args', nargs=-1)
@click.pass_context
def main(ctx, args):
    """D&D Dice Roller CLI

    Roll dice using standard D&D notation:
    - dice-roller 1d20 (roll one 20-sided die)
    - dice-roller 3d6 (roll three 6-sided dice and sum)
    - dice-roller 4d8+3 (roll four 8-sided dice, sum, and add 3)

    Or use subcommands for history management:
    - dice-roller history (show roll history)
    - dice-roller clear (clear roll history)
    """
    if ctx.invoked_subcommand is not None:
        return

    if not args:
        click.echo(ctx.get_help())
        return

    # Check if first argument is a known subcommand
    first_arg = args[0].lower()
    if first_arg in ['history', 'clear']:
        # Manually invoke the subcommand
        if first_arg == 'history':
            # Parse options if provided
            limit = 20  # default
            show_all = False

            i = 1
            while i < len(args):
                if args[i] in ['--limit', '-l'] and i + 1 < len(args):
                    try:
                        limit = int(args[i + 1])
                        i += 2
                    except (ValueError, IndexError):
                        i += 1
                elif args[i] in ['--all', '-a']:
                    show_all = True
                    i += 1
                else:
                    i += 1

            ctx.invoke(history, limit=limit, all=show_all)
        elif first_arg == 'clear':
            # For clear command, we need to handle confirmation manually
            if click.confirm('Are you sure you want to clear all history?'):
                cli = DiceRollerCLI()
                cli.clear_history()
            else:
                ctx.exit(1)
        return

    # Treat as dice notation
    dice_string = args[0]
    cli = DiceRollerCLI()
    cli.roll_dice(dice_string)


@main.command()
@click.option('--limit', '-l', type=int, default=20, help='Number of recent rolls to show (default: 20)')
@click.option('--all', '-a', is_flag=True, help='Show all roll history')
def history(limit, all):
    """Show roll history (default: last 20 rolls)"""
    cli = DiceRollerCLI()
    if all:
        cli.show_history(limit=None)
    else:
        cli.show_history(limit=limit)


@main.command()
@click.confirmation_option(prompt='Are you sure you want to clear all history?')
def clear():
    """Clear roll history"""
    cli = DiceRollerCLI()
    cli.clear_history()


if __name__ == '__main__':
    main()
