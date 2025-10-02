#!/bin/bash
# /Users/marcozingoni/Playgound/Python/diceRoller/setup.sh
# Setup script for D&D Dice Roller

set -e

echo "🎲 Setting up D&D Dice Roller..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x bin/dice-roller
chmod +x dice-roller

# Get the absolute path to the bin directory
BIN_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/bin"

echo "✅ Setup complete!"
echo ""
echo "🚀 You can now use the dice roller in several ways:"
echo ""
echo "1. Run directly from project directory:"
echo "   ./dice-roller 1d20"
echo "   ./bin/dice-roller 1d20"
echo ""
echo "2. Add to your PATH for global access:"
echo "   export PATH=\"\$PATH:$BIN_PATH\""
echo "   echo 'export PATH=\"\$PATH:$BIN_PATH\"' >> ~/.bashrc  # or ~/.zshrc"
echo "   source ~/.bashrc  # or source ~/.zshrc"
echo "   dice-roller 1d20"
echo ""
echo "3. Install as Python package:"
echo "   pip install -e ."
echo "   dice-roller 1d20"
echo ""
echo "📖 For detailed instructions, see INSTALL.md"
echo ""
echo "🎯 Quick test:"
./bin/dice-roller 1d20
