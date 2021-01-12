import numpy as np
from mingus.midi import midi_file_out
from mingus.containers import note_container
from mingus.containers import track

from random import randrange

# NOTE:
    # global variable for the composition 

global t 

t = track.Track()

def seed(): 
    a = [ #blinker
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    b = [ #block
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]

    c = [ #tub
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    d = [ #bee_hive
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]

    e = [ #infinite
        [1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1],
    ]

    seeds = [a, b, c, d, e]

    number = (randrange(0, 100000))%5

    print(number)

    return np.array(seeds[number])


def updateUniverse(x, y, universe):
    # rules:
    # Any live cell with two or three live neighbours survives.
    # Any dead cell with three live neighbours becomes a live cell.
    # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    currentCell = universe[x, y]
    neighbours = np.sum(universe[x - 1 : x + 2, y - 1 : y + 2]) - currentCell

    shouldLive = False
    if (2 <= neighbours <= 3):
        shouldLive = True

    if universe[x, y] and (shouldLive == False): #delete cell 
        c_major = note_container.NoteContainer(["C", "E", "G"])
        t.add_notes(c_major) 
        return 0

    elif (neighbours == 3): #create cell
        a_minor = note_container.NoteContainer(["A", "C", "E"])
        t.add_notes(a_minor)
        return 1

    elif (currentCell == 1):
        # cell exists and survived iteration 
        f_major = note_container.NoteContainer(["F", "A", "C"])
        t.add_notes(f_major)

    return currentCell


def generation(universe):

    new_universe = np.copy(universe)

    for i in range(universe.shape[0]):
        for j in range(universe.shape[1]):
            new_universe[i, j] = updateUniverse(i, j, universe)
    return new_universe

def initializeUniverse(size = "100,100", position = "50,50", seed = seed()):
    universe = np.zeros((int(size.split(",")[0]), int(size.split(",")[1])), dtype=int)
    x = int(position.split(",")[0])
    y = int(position.split(",")[1])
    x2 = x + seed.shape[0]
    y2 = y + seed.shape[1]
    universe[x:x2, y:y2] = seed
    return universe    

def createTrack(iterations):
    # seed_array = seed()
    universe = initializeUniverse()

    for i in range(iterations):
        generation(universe)
    midi_file_out.write_Track("test.mid", t, 300)

createTrack(10)

# def visualize():



