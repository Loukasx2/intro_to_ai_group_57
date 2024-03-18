#!/bin/bash

# Define the Python scripts to be executed
game="/home/pleon/DTU/IntroToAI/intro_to_ai_group_57/game_engine.py"
player="/home/pleon/DTU/IntroToAI/intro_to_ai_group_57/AI.py"

# Define the number of times to execute the Python scripts
num_executions=20

# Loop to execute the Python scripts multiple times
for (( i=1; i<=$num_executions; i++ ))
do

    while ps -a | grep -q '[p]ython3'; do
        pkill python3
        sleep 1
    done
    echo "Launching Python scripts for the $i-th time..."

    # Run game_engine.py and AI.py (player 1) in the background
    python3 "$game" 2 > /dev/null &   # Redirect output to /dev/null to suppress output
    sleep 1
    python3 "$player" 1 > /dev/null &

    # Run AI.py (player 2) in the foreground
    python3 "$player" 2 

    echo "Waiting for the Python scripts to finish..."


    # wait
done

echo "All executions completed."
