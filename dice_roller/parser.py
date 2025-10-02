# /Users/marcozingoni/Playgound/Python/diceRoller/dice_roller/parser.py
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class DiceRoll:
    """Represents a parsed dice roll command"""
    count: int
    sides: int
    modifier: int = 0


class DiceParser:
    """Parses D&D dice notation like 1d20, 3d6, 4d8+3"""

    DICE_PATTERN = re.compile(r'^(\d+)d(\d+)([+-]\d+)?$', re.IGNORECASE)

    @classmethod
    def parse(cls, dice_string: str) -> Optional[DiceRoll]:
        """Parse dice notation string into DiceRoll object"""
        dice_string = dice_string.strip().replace(' ', '')

        match = cls.DICE_PATTERN.match(dice_string)
        if not match:
            return None

        count = int(match.group(1))
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        # Validate dice parameters
        if count <= 0 or sides <= 0:
            return None

        return DiceRoll(count=count, sides=sides, modifier=modifier)
