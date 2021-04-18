# Read in the file
import os
import sys

init_path = os.path.join('tsteno', '__init__.py')

with open(init_path, 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('prebuild', sys.argv[1])

# Write the file out again
with open(init_path, 'w') as file:
    file.write(filedata)
