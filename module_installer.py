import pkg_resources
import subprocess
import platform
import sys


# We need to ensure user has ffmpeg library installed and can be found
# First, check if package manager and ffmpeg are installed respectively
# If not, then install it

installations_successful = True

def confirm_and_execute(cmd):
    global installations_successful
    confirm = input(f'About to run: {cmd}. Proceed? [y/n] ')
    if confirm.lower() == 'y':
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f'Failed to execute: {cmd}')
            installations_successful = False
    else:
        print('Skipping.')
        installations_successful = False


def check_and_install(check_cmd, install_cmd):
    # Check if the software is installed.
    result = subprocess.run(check_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f'{check_cmd.split()[0]} is already installed.')
    else:  # If the check command failed, then the software is not installed.
        print(f'{check_cmd.split()[0]} is not installed.')
        confirm_and_execute(install_cmd)


def check_and_install_library(library):
    try:
        dist = pkg_resources.get_distribution(library)
        print(f'{library} ({dist.version}) is already installed.')
    except pkg_resources.DistributionNotFound:
        print(f'{library} not found, will try installing after confirmation')
        confirm_and_execute(f'pip install {library}')


OS_system = platform.system()

if OS_system == 'Windows':
    # Check if Chocolatey is installed and then install ffmpeg.
    check_and_install('choco -v', '@"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\\chocolatey\\bin"')
    check_and_install('ffmpeg -version', 'choco install ffmpeg -y')
elif OS_system == 'Darwin':
    # Check if brew is installed and then install ffmpeg.
    check_and_install('brew -v', '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    check_and_install('ffmpeg -version', 'brew install ffmpeg')
else:  # Assume the system is a Linux distribution.
    # Check if apt-get is installed and then install ffmpeg. We assume apt-get exists in this case, might not be true for all Linux distributions.
    check_and_install('apt-get -v', 'sudo apt update && sudo apt upgrade -y')
    check_and_install('ffmpeg -version', 'sudo apt install ffmpeg -y')

with open('requirements.txt', 'r') as f:
    # Open text file and read required libraries into a list
    libraries = f.read().splitlines()

for library in libraries:
    # Iterate through list and see if the library is already installed or not
    check_and_install_library(library)
    
if installations_successful:
    print("All required software and libraries are installed. The Python project will now work properly.")
else:
    print("Some installations were skipped or failed. The Python project may not work properly.")