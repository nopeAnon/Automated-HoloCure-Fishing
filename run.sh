#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed on this system."
    exit 1
fi

# Check if Xwininfo is installed
if ! command -v xwininfo &> /dev/null; then
    echo "Error: Xwininfo is not installed on this system. Please install it using your distribution's package manager"
    exit 1
fi

# Check if x11 session
if [ "$XDG_SESSION_TYPE" != "x11" ]; then
    echo "Warning: Couldn't determine if running on X11. Wayland and other compositors are not suppported."
fi

python_version=$(python3 --version)

major_version=$(echo "$python_version" | cut -d ' ' -f 2 | cut -d '.' -f 1)
minor_version=$(echo "$python_version" | cut -d '.' -f 2 | cut -d '.' -f 2)

if [ "$major_version" -lt 3 ] || { [ "$major_version" -eq 3 ] && [ "$minor_version" -lt 11 ]; }; then
    echo "Warning: Python version is older than 3.11. This script was only tested with python 3.11."
fi

setup_env(){
    echo "Info: Existing environment not found, this is probably the first time you're running this script...."

    echo "Info: Creating new virtual environment in .venv/ folder."
    python3 -m venv .venv
    source .venv/bin/activate

    echo "Info: Installing dependencies."
    pip install -r requirements_linux.txt

   remove_xlib_bad_file
}

remove_xlib_bad_file(){
    echo "Info: Removing line in Xlib dependency that breaks certain Linux systems"
    python_lib_dir=".venv/lib/python$major_version.$minor_version"
    unix_connect_file="$python_lib_dir/site-packages/Xlib/support/unix_connect.py"
    if [ -f "$unix_connect_file" ]; then
        sed -i '31,35d' "$unix_connect_file"
    else
        echo "Error: failed, $unix_connect_file not found."
        echo "Error: Please report this bug on github."
        deactivate
        rm -rf .venv
        exit 1

    fi

    python -c "from Xlib.display import Display; Display()"
    return_code=$?

    if [ $return_code -eq 0 ]; then
        echo "Info: Line removal OK."
    else
        echo "Error: Removing the line didn't fix the issue"
        echo "Error: Please report this bug on github."
        deactivate
        rm -rf .venv
        exit 1
    fi
}

if [ ! -d ".venv" ]; then
    setup_env
else
    echo "Info: Using existing virtual environment .venv directory."

    source .venv/bin/activate
fi

echo "Info: Starting main program."
python holocure_fishing.py


