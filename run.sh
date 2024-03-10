#!/bin/bash

# Function to clean up and terminate child processes
cleanup() {
    echo "Stopping child processes..."
    # Terminate the child processes
    pkill -P $$
    exit 0
}

# Trap Ctrl+C and call cleanup function
trap cleanup INT

# Start the processes in the background
python3 minmax3.py 1 &
python3 minmax3.py 2 &
python3 game_engine.py 2

# Wait for all child processes to finish
wait
