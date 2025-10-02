# /Users/marcozingoni/Playgound/Python/diceRoller/dice_roller/roller.py
import random
from dataclasses import dataclass
from typing import List
from .parser import DiceRoll


@dataclass
class RollResult:
    """Represents the result of a dice roll"""
    dice_roll: DiceRoll
    individual_rolls: List[int]
    total: int
    command: str


class DiceRoller:
    """Handles dice rolling mechanics"""

    def __init__(self):
        self.random = random.Random()

    def roll(self, dice_roll: DiceRoll, command: str) -> RollResult:
        """Roll dice and return detailed results"""
        individual_rolls = []

        for _ in range(dice_roll.count):
            roll = self.random.randint(1, dice_roll.sides)
            individual_rolls.append(roll)

        dice_sum = sum(individual_rolls)
        total = dice_sum + dice_roll.modifier

        return RollResult(
            dice_roll=dice_roll,
            individual_rolls=individual_rolls,
            total=total,
            command=command
        )
