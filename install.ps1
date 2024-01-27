# Function to print in color
function Print-Color {
  param(
    [Parameter(Mandatory = $true)]
    [int]$Color,
    [Parameter(Mandatory = $true)]
    [string]$Message
  )

  Write-Host $Message -ForegroundColor $Color
}

# Function to get the directory of the script
function Get-ScriptDirectory {
  $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
  return $scriptPath
}

# Function to check and install Python
function Check-And-Install-Python {
  Print-Color 32 "Checking Python installation..."
  if (Get-Command python -ErrorAction SilentlyContinue) {
    Print-Color 32 "Python is already installed."
  } else {
    Print-Color 31 "Python not found. Installing Python..."
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe"  # Download the latest Python installer
    Start-BitsTransfer -Source $pythonInstallerUrl -Destination "$env:TEMP\python-installer.exe"
    Start-Process "$env:TEMP\python-installer.exe" -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    Remove-Item "$env:TEMP\python-installer.exe"
  }
}

# Function to check and install pip
function Check-And-Install-Pip {
  Print-Color 32 "Checking pip installation..."
  if (Get-Command pip -ErrorAction SilentlyContinue) {
    Print-Color 32 "pip is already installed."
  } else {
    Print-Color 31 "pip not found. Installing pip..."
    python -m ensurepip
  }
}

# Function to check and install FFmpeg
function Check-And-Install-FFmpeg {
  Print-Color 32 "Checking FFmpeg installation..."
  if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    Print-Color 32 "FFmpeg is already installed."
  } else {
    Print-Color 31 "FFmpeg not found. Installing FFmpeg..."
    $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"  # Download a pre-built Windows version
    $downloadPath = "$env:USERPROFILE\Downloads\ffmpeg.7z"
    Start-BitsTransfer -Source $ffmpegUrl -Destination $downloadPath
    Expand-Archive $downloadPath -DestinationPath "$env:USERPROFILE\ffmpeg" -Force
    Remove-Item $downloadPath
    $env:Path += ";$env:USERPROFILE\ffmpeg\bin"
    [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
  }
}

# Function to install Python packages
function Install-PythonPackages {
  Print-Color 32 "Installing Python packages..."
  pip install requests argparse urllib3 colorama tqdm ffpb
}

# Function to set PWDL environment variable
function Set-PWDLEnvironmentVariable {
  $scriptDirectory = Get-ScriptDirectory
  $pwdlEnvVar = "python $scriptDirectory\pwdl.py"

  if (!(Test-Path env:PWDL) -or ($env:PWDL -notlike "*$scriptDirectory*")) {
    $env:PWDL = $pwdlEnvVar
    [Environment]::SetEnvironmentVariable("PWDL", $env:PWDL, [EnvironmentVariableTarget]::User)
    Print-Color 32 "PWDL environment variable set."
  } else {
    Print-Color 32 "PWDL environment variable is already set."
  }
}

# Check and install Python
Check-And-Install-Python

# Check and install pip
Check-And-Install-Pip

# Check and install FFmpeg
Check-And-Install-FFmpeg

# Install Python packages
Install-PythonPackages

# Set PWDL environment variable
Set-PWDLEnvironmentVariable

# Display end message
Print-Color 36 "pwdl is set to go"

