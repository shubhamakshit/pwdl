#!/bin/bash

# Directory to install FFmpeg
install_dir="$HOME/ffmpeg"

# Function to install FFmpeg
install_ffmpeg() {
    echo "Installing FFmpeg..."

    # Create installation directory
    mkdir -p "$install_dir"

    # Detect architecture
    arch=$(uname -m)
    if [ "$arch" == "x86_64" ]; then
        ffmpeg_url="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    elif [ "$arch" == "aarch64" ]; then
        ffmpeg_url="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz"
    else
        echo "Unsupported architecture: $arch"
        exit 1
    fi

    # Download and extract FFmpeg
    wget "$ffmpeg_url" -O "$install_dir/ffmpeg.tar.xz"
    tar xf "$install_dir/ffmpeg.tar.xz" -C "$install_dir" --strip-components=1

    # Add FFmpeg to the user's PATH
    echo 'export PATH=$PATH:'"$install_dir" >> "$HOME/.bashrc"
    source "$HOME/.bashrc"

    echo "FFmpeg installation completed."
}

# Install FFmpeg
install_ffmpeg

