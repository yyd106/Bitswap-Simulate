
import math

DEGREE = 100

class Network:
    """ THe whole network """

    def __init__(self, n_vertices):
        self._n_vertices = n_vertices
        self._adj = [[] for _ in range(n_vertices)]


    def add_edge(self, s, t):
        self._adj[s].append(t)
        self._adj[t].append(s)