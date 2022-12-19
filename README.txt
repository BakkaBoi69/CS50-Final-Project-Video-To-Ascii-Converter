it'll take a bit of effort to set this up
the most difficult part should be the python installation
and pip installation which is not that difficult i think


FOR WINDOWS:
go to this website to get the latest version of python 
on your system and  and get pip (python's package manager):
https://www.geeksforgeeks.org/how-to-install-pip-on-windows/


FOR MAC:
go to this website to get the latest version of python 
https://www.python.org/downloads/macos/
on your system and  and get pip (python's package manager):
https://www.geeksforgeeks.org/how-to-install-pip-in-macos/


This next bit is more preferrably done in vsc or any text editor rather 
than in the terminal/command prompt but it can be done them too


INSTALLING NECESSARY MODULES:
Run "python module_installer.py" (should work maybe)


OR IF THAT DOESN'T WORK THEN FOLLOW STEPS BELOW


Run "pip install module_name" for each module which is required 
You'll find the list of module names in requirements.txt
After that, you should be able to run the program


GIVING THE FILEPATH TO THE VIDEO WHEN RUNNING THE PROGRAM:
While running the program, when asked for a video file path, remember that it is the 
RELATIVE FILEPATH, i.e, it is relative to the current working directory (the folder where this program is stored)

for example, the current directory for "usr/something/thing/project" is "project"

if the video you want to convert is in "usr/something/media/videos",
the relative path will be "../../media/videos/my_video.mp4"

here, the ".." means to go one directory up, while "." means the current directory