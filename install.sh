#!/bin/bash

# Function to print in color
print_color() {
    color=$1
    message=$2
    echo -e "\033[1;${color}m${message}\033[0m"
}

# Function to get the directory of the script
get_script_location() {
    script_location="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    echo "$script_location"
}

# Function to check and install Python
check_and_install_python() {
    print_color 32 "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        print_color 32 "Python3 is already installed."
    else
        print_color 31 "Python3 not found. Installing python-is-python3..."
        sudo apt-get update
        sudo apt-get install -y python-is-python3
    fi
}

# Function to check and install pip
check_and_install_pip() {
    print_color 32 "Checking pip installation..."
    if command -v pip &> /dev/null; then
        print_color 32 "pip is already installed."
    else
        print_color 31 "pip not found. Installing pip..."
        sudo apt-get update
        sudo apt-get install -y python3-pip
    fi
}

# Function to check and install FFmpeg
check_and_install_ffmpeg() {
    print_color 32 "Checking FFmpeg installation..."
    if command -v ffmpeg &> /dev/null; then
        print_color 32 "FFmpeg is already installed."
    else
        print_color 31 "FFmpeg not found. Installing FFmpeg..."

        # Directory to install FFmpeg
        install_dir="$HOME/ffmpeg"

        # Create installation directory
        mkdir -p "$install_dir"

        # Detect architecture
        arch=$(uname -m)
        if [ "$arch" == "x86_64" ]; then
            ffmpeg_url="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        elif [ "$arch" == "aarch64" ]; then
            ffmpeg_url="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz"
        else
            print_color 31 "Unsupported architecture: $arch"
            exit 1
        fi

        # Download and extract FFmpeg
        wget "$ffmpeg_url" -O "$install_dir/ffmpeg.tar.xz"
        tar xf "$install_dir/ffmpeg.tar.xz" -C "$install_dir" --strip-components=1

        # Add FFmpeg to the user's PATH
        echo 'export PATH=$PATH:'"$install_dir" >> "$HOME/.bashrc"
        source "$HOME/.bashrc"

        print_color 32 "FFmpeg installation completed."
    fi
}

# Function to install Python packages
install_python_packages() {
    print_color 32 "Installing Python packages..."
    python3 -m pip install requests argparse urllib3 colorama tqdm ffpb
}

# Function to set PWDL environment variable
set_pwdl_environment_variable() {
    script_location=$(get_script_location)
    pwdl_env_var="python $script_location/pwdl.py"

    # Check if PWDL variable is already set in the environment
    if [[ -z "${PWDL}" || "${PWDL}" != *"$script_location"* ]]; then
        # Add PWDL variable to the environment
        export PWDL="$pwdl_env_var"

        # Add PWDL to the user's ~/.bashrc if not already present
        if ! grep -qF "export PWDL" "$HOME/.bashrc"; then
            echo "export PWDL=\"$pwdl_env_var\"" >> "$HOME/.bashrc"
        fi

        print_color 32 "PWDL environment variable set."
    else
        print_color 32 "PWDL environment variable is already set."
    fi
}

# Check and install Python
check_and_install_python

# Check and install pip
check_and_install_pip

# Check and install FFmpeg
check_and_install_ffmpeg

# Install Python packages
install_python_packages

# Set PWDL environment variable
set_pwdl_environment_variable

# Display end message
print_color 36 "pwdl is set to go"

