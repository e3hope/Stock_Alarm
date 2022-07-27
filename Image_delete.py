import os
import inc

if os.path.exists(inc.environment[inc.branch] + 'Image/'):
    for file in os.scandir(inc.environment[inc.branch] + 'Image/'):
        os.remove(file.path)