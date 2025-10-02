# /Users/marcozingoni/Playgound/Python/diceRoller/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY dice_roller/ ./dice_roller/

# Create entrypoint script
RUN echo '#!/bin/bash\npython -m dice_roller.cli "$@"' > /usr/local/bin/dice-roller && \
    chmod +x /usr/local/bin/dice-roller

# Set up volume for history persistence
VOLUME ["/root"]

ENTRYPOINT ["dice-roller"]
