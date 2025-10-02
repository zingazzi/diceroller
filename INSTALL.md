# Installation Guide

## Quick Setup for Command Line Access

To use `dice-roller` from anywhere on your command line, follow these steps:

### Option 1: Add to PATH (Recommended)

1. **Add the bin directory to your PATH:**

   ```bash
   # For bash/zsh users, add this line to your ~/.bashrc or ~/.zshrc
   export PATH="$PATH:/Users/marcozingoni/Playgound/Python/diceRoller/bin"

   # Then reload your shell configuration
   source ~/.bashrc  # or source ~/.zshrc
   ```

2. **Test the installation:**
   ```bash
   dice-roller 1d20
   dice-roller history
   ```

### Option 2: Create a Symlink

1. **Create a symlink in a directory that's already in your PATH:**
   ```bash
   # Create symlink in /usr/local/bin (requires sudo)
   sudo ln -s /Users/marcozingoni/Playgound/Python/diceRoller/bin/dice-roller /usr/local/bin/dice-roller

   # Or create symlink in ~/bin (if it exists and is in PATH)
   ln -s /Users/marcozingoni/Playgound/Python/diceRoller/bin/dice-roller ~/bin/dice-roller
   ```

2. **Test the installation:**
   ```bash
   dice-roller 3d6+2
   ```

### Option 3: Use Directly from Project Directory

If you don't want to modify your PATH, you can run the script directly:

```bash
cd /Users/marcozingoni/Playgound/Python/diceRoller
./bin/dice-roller 1d20
```

## Package Installation (Alternative)

You can also install the package and use the entry point:

```bash
cd /Users/marcozingoni/Playgound/Python/diceRoller
pip install -e .
dice-roller 1d20  # This will work from anywhere
```

## Usage Examples

Once installed, you can use these commands from anywhere:

```bash
# Basic dice rolls
dice-roller 1d20
dice-roller 3d6
dice-roller 4d8+3
dice-roller 2d10-1

# History management
dice-roller history                    # Show last 20 rolls (default)
dice-roller history --limit 5         # Show last 5 rolls
dice-roller history --all             # Show all rolls
dice-roller clear                      # Clear history (with confirmation)

# Help
dice-roller --help
dice-roller history --help
```

## Troubleshooting

- **"Command not found"**: Make sure the bin directory is in your PATH or use the full path to the script
- **"Import error"**: Make sure you're running from the project directory or have installed the package with `pip install -e .`
- **"Permission denied"**: Make sure the script is executable with `chmod +x bin/dice-roller`
