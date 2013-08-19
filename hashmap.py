import math


def dict_setdefault(d, k, v):
    r = d.get(k, v)
    if k not in d:
        d[k] = v
    return r


class HashMap(object):
    """
    Spatial hashing that allows for a 3D or 2D domain space to be projected
    into a 1D hash table
    http://www.cs.ucf.edu/~jmesit/publications/scsc%202005.pdf
    """
    def __init__(self):
        self.blockSize = 50
        self.blocks = {}

    def key(self, position):
        """
        Hashing function for any point
        """
        blockSize = self.blockSize
        return (
            int((math.floor(position[0] / blockSize)) * blockSize),
            int((math.floor(position[1] / blockSize)) * blockSize)
        )

    def insert(self, position):
        """
        Inserts a point
        """
        dict_setdefault(self.blocks, self.key(position), []).append(position)

    def get(self, position):
        """
        Returns all of the objects in the cell as given by point
        """
        return dict_setdefault(self.blocks, self.key(position), [])

    def clear(self):
        """
        Clears all of the blocks from the hashmap
        """
        self.blocks = {}

