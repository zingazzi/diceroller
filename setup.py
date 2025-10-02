# /Users/marcozingoni/Playgound/Python/diceRoller/setup.py
from setuptools import setup, find_packages

setup(
    name="dice-roller",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "dice-roller=dice_roller.cli:main",
        ],
    },
    author="Marco Zingoni",
    description="A D&D dice roller CLI application",
    python_requires=">=3.8",
)
