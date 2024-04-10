#!/bin/bash

# Name of the virtual environment directory
VENV_DIR="venv"
ERROR_LOG="error_log.txt"
REQUIREMENTS="requirements.txt"

# Function to log errors
log_error() {
    echo "[$(date)] - $1" >> "$ERROR_LOG"
}

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one now..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Check if requirements are installed
if [ -f "$REQUIREMENTS" ]; then
    # Check if requirements are already satisfied
    python3 -m pip freeze > installed.txt

    if diff -q "$REQUIREMENTS" installed.txt > /dev/null; then
      python3 -m pip install --upgrade pip  # Ensure pip is up-to-date
      echo "Installing required Python packages..."
      python3 -m pip install -r "$REQUIREMENTS"
    fi
    rm installed.txt
else
    echo "No requirements.txt file found."
fi

# This will assign the first command-line argument to FILE_PATH
FILE_PATH="$1"

# Check if the file path was provided
if [ -z "$FILE_PATH" ]; then
    echo "No file path provided. Usage: ./get_coyote_data.sh ./path/to/file"
    exit 1
fi

# Check if the file path is valid
if [ -f "$FILE_PATH" ]; then
      python3 main.py "$FILE_PATH" 2>> "$ERROR_LOG" || log_error "main.py script execution failed."
      python3 arc_gis_online.py 2>> "$ERROR_LOG" || log_error "arc_gis_online.py script execution failed."
else
    echo "File does not exist or is not a regular file."
    exit 1
fi

deactivate
