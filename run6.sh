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
python3 minmax3_6_players.py 1 &
python3 minmax3_6_players.py 2 &
python3 minmax3_6_players.py 3 &
python3 minmax3_6_players.py 4 &
python3 minmax3_6_players.py 5 &
python3 minmax3_6_players.py 6 &
python3 game_engine.py 6

# Wait for all child processes to finish
wait
