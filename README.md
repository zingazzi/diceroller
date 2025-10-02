# D&D Dice Roller CLI

A command-line dice roller for Dungeons & Dragons that supports standard dice notation with modifiers and roll history.

## Features

- 🎲 Roll dice using standard D&D notation (1d20, 3d6, 4d8+3)
- 📜 Track and view roll history (default: last 20 rolls)
- 🔧 Standalone executable script for easy command-line access
- 🐳 Docker support for easy deployment
- ✨ Beautiful CLI output with emojis

## Installation

### Quick Start (Standalone Script)

```bash
# Clone or download the project
cd diceRoller

# Install dependencies
pip install -r requirements.txt

# Use directly
./bin/dice-roller 1d20

# Or add to PATH for global access (see INSTALL.md for details)
export PATH="$PATH:$(pwd)/bin"
dice-roller 1d20
```

### Package Installation

```bash
# Install as a Python package
pip install -e .
dice-roller 1d20
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

### Docker Installation

```bash
# Build the Docker image
docker-compose build

# Or build manually
docker build -t dice-roller .
```

## Usage

### Basic Rolling

```bash
# Roll a single d20
dice-roller 1d20

# Roll three d6 and sum them
dice-roller 3d6

# Roll four d8, sum them, and add 3
dice-roller 4d8+3

# Roll with negative modifier
dice-roller 2d10-1
```

### History Commands

```bash
# Show roll history (default: last 20 rolls)
dice-roller history

# Show specific number of recent rolls
dice-roller history --limit 5

# Show all roll history
dice-roller history --all

# Clear all history
dice-roller clear
```

### Docker Usage

```bash
# Roll dice using Docker
docker-compose run dice-roller 1d20

# View history
docker-compose run dice-roller history

# Interactive mode
docker-compose run dice-roller
```

## Examples

```bash
$ dice-roller 1d20
🎲 1d20 → 15

$ dice-roller 3d6
🎲 3d6 → 12
   Rolls: [4 + 3 + 5] = 12

$ dice-roller 4d8+3
🎲 4d8+3 → 19
   Rolls: [2 + 6 + 4 + 4] = 16 +3 = 19

$ dice-roller history --limit 3
📜 Roll History:
==================================================
🕐 2024-10-02 14:30:15
🎲 1d20 → 15

🕐 2024-10-02 14:30:22
🎲 3d6 → 12
   Rolls: [4 + 3 + 5]

🕐 2024-10-02 14:30:28
🎲 4d8+3 → 19
   Rolls: [2 + 6 + 4 + 4] +3
```

## Supported Dice Notation

- `XdY` - Roll X dice with Y sides (e.g., `1d20`, `3d6`)
- `XdY+Z` - Roll X dice with Y sides and add Z (e.g., `4d8+3`)
- `XdY-Z` - Roll X dice with Y sides and subtract Z (e.g., `2d10-1`)

## History Storage

Roll history is stored in `~/.dice_roller_history.json` and persists between sessions. When using Docker, history is stored in a named volume for persistence.

## Development

```bash
# Run tests (if you add them)
python -m pytest

# Format code
black dice_roller/

# Type checking
mypy dice_roller/
```

## License

MIT License - feel free to use and modify as needed for your D&D sessions!
