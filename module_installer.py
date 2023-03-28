import subprocess
subprocess.run("pip install -r requirements.txt", shell=True)

# Set the command to append the export statement to the .zshrc file
command = 'echo "export IMAGEIO_FFMPEG_EXE=./ffmpeg" >> ~/.zshrc'

# Run the command using subprocess
subprocess.run(command, shell=True)
