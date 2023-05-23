import numpy as np
from interface import Interface

file = open("file.txt", "r")
world = []
for index, line in enumerate(file.readlines()):
    world.append([int(s) for s in line.split() if s.isdigit()])

interface = Interface(np.matrix(world))
interface.showInterface()
