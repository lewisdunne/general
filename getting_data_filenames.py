'''GETTING DATA FILES FROM A DIRECTORY'''
import os # Use the os library to identify files.

#-Function -------------------------------------------------------------------#
def get_files(path, extension=None):
    '''Reads all files into a list if they have a given extension.
    If extension is undefined, just returns all files. '''
    if extension == None:
        files = os.listdir(path)
    else:
        files = [f for f in os.listdir(path) if f.split('.')[-1] == extension]
    
    return files
    
#-Example run ----------------------------------------------------------------#
# Define the path in which your datafiles exist.
path = 'C://Users//L//Documents//PsychoPy//MemANT//data'

files = read_files(path, extension='csv')

print(files)
