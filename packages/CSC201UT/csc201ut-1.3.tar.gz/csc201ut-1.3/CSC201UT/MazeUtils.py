"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the maze and labyrinth "debug".
Credit to Keith Schwarz (htiek@cs.stanford.edu).
See http://nifty.stanford.edu/2021/schwarz-linked-list-labyrinth/.
This is a Python port of his nifty assignment.
"""

from random import seed, shuffle, random, randint
from copy import deepcopy
from math import log
from CSC201UT.UnorderedList import UnorderedList

"""Defines a MazeCell (a cell within the maze/labyrinth)."""
class MazeCell:
    def __init__(self, item=None):
        self._item = item
        self._N = None
        self._S = None
        self._E = None
        self._W = None

"""Support classes and functions for creating mazes and labyrinths."""
class MazeUtils:
    # constants (for randomness)
    HASH_SEED = 5381
    HASH_MULTIPLIER = 33
    HASH_MASK = 0x7fffffff
    # constants (for the maze)
    NUM_ROWS = 4
    NUM_COLS = 4
    # constants (for the labyrinth)
    LABYRINTH_SIZE = 12

    # defines an edge between two MazeCells
    class EdgeBuilder:
        def __init__(self, frm, to, frmPort, toPort):
            self._frm = frm
            self._to = to
            self._frmPort = frmPort
            self._toPort = toPort

    # Given a location in a maze, returns whether the given sequence of
    # steps will let you escape the maze. The steps should be given as
    # a string made from N, S, E, and W for north/south/east/west without
    # spaces or other punctuation symbols, such as "WESNNNS".
    #
    # To escape the maze, you need to find the Potion, the Spellbook, and
    # the Wand. You can only take steps in the four cardinal directions,
    # and you can't move in directions that don't exist in the maze.
    #
    # It is assumed that the input MazeCell is not null.
    def isPathToFreedom(start, moves):
        cell = start
        items = []

        # pick up an item in the starting cell
        if (start._item):
            items.append(start._item)

        # make a move
        for path in moves:
            if (path == "N"):
                cell = cell._N
            elif (path == "S"):
                cell = cell._S
            elif (path == "E"):
                cell = cell._E
            elif (path == "W"):
                cell = cell._W
            else:
                return False

            # we've reached an invalid cell
            if (not cell):
                return False

            # can we pick up an item in this cell?
            if (cell._item and not cell._item in items):
                items.append(cell._item)

        # did we get all three items?
        return (len(items) == 3)

    # Simple rolling hash. Stolen shameless from StanfordCPPLib, maintained by a collection
    # of talented folks at Stanford University. We use this hash implementation to ensure
    # consistency from run to run and across systems.
    def hashCode(s, values=None):
        # if the input is just an integer, AND it with the mask
        if (type(s) is int):
            return s & MazeUtils.HASH_MASK
         
        # if input values exist, first get the hash of the input string
        if (values):
            h = MazeUtils.hashCode(s)
        # otherwise, the hash is the seed
        else:
            h = MazeUtils.HASH_SEED

        # if input values exist, update the hash to include them
        if (values):
            for v in values:
                h = h * MazeUtils.HASH_MULTIPLIER + v
        # otherwise, use the characters in the string
        else:
            for char in s:
                h = h * MazeUtils.HASH_MULTIPLIER + ord(char)

        return MazeUtils.hashCode(h)

    # Returns a maze specifically tailored to the given name.
    #
    # We've implemented this function for you. You don't need to write it
    # yourself.
    #
    # Please don't make any changes to this function - we'll be using our
    # reference version when testing your code, and it would be a shame if
    # the maze you solved wasn't the maze we wanted you to solve!
    def mazeFor(name):
        seed(MazeUtils.hashCode(name, [ MazeUtils.NUM_ROWS, MazeUtils.NUM_COLS ]))
        maze = MazeUtils.makeMaze(MazeUtils.NUM_ROWS, MazeUtils.NUM_COLS)
        
        linearMaze = []
        for row in maze:
            for col in row:
                linearMaze.append(col)

        # find the distances between all pairs of nodes
        distances = MazeUtils.allPairsShortestPaths(linearMaze)
        # select a combination of four nodes maximizing the minimum
        # distances between points and use that as our item/start locations
        locations = MazeUtils.remoteLocationsIn(distances)

        # place the items there
        linearMaze[locations[1]]._item = "Spellbook"
        linearMaze[locations[2]]._item = "Potion"
        linearMaze[locations[3]]._item = "Wand"

        # begin at position 0
        return linearMaze[locations[0]]

    # Returns a labyrinth specifically tailored to the given name.
    #
    # Please don't make any changes to this function - we'll be using our
    # reference version when testing your code, and it would be a shame if
    # the maze you solved wasn't the maze we wanted you to solve!
    def labyrinthFor(name):
        seed(MazeUtils.hashCode(name, [ MazeUtils.LABYRINTH_SIZE ]))
        maze = MazeUtils.makeLabyrinth(MazeUtils.LABYRINTH_SIZE)

        # find the distances between all pairs of nodes
        distances = MazeUtils.allPairsShortestPaths(maze)
        # select a 4-tuple maximizing the minimum distances between points
        # and use that as our item/start locations
        locations = MazeUtils.remoteLocationsIn(distances)

        # place the items there
        maze[locations[1]]._item = "Spellbook"
        maze[locations[2]]._item = "Potion"
        maze[locations[3]]._item = "Wand"

        # begin at position 0
        return maze[locations[0]]

    # returns if two nodes are adjacent
    def areAdjacent(first, second):
        return (first._N == second or first._S == second or first._E == second or first._W == second)

    # Uses the Floyd-Warshall algorithm to compute the shortest paths between all
    # pairs of nodes in the maze. The result is a table where table[i][j] is the
    # shortest path distance between maze[i] and maze[j].
    def allPairsShortestPaths(maze):
        # fill the table with "infinity" values
        result = [ [ len(maze) + 1 for _ in range(len(maze)) ] for _ in range(len(maze)) ]

        # the distance from a node to itself is 0
        for i in range(len(maze)):
            result[i][i] = 0

        # neighbors have a distance of 1
        for i in range(len(maze)):
            for j in range(len(maze)):
                if (MazeUtils.areAdjacent(maze[i], maze[j])):
                    result[i][j] = 1

        # Dynamic programming step. Keep expanding paths by allowing for paths
        # between nodes.
        for i in range(len(maze)):
            nxt = [ [ 0 for _ in range(len(maze)) ] for _ in range(len(maze)) ]
            for j in range(len(maze)):
                for k in range(len(maze)):
                    nxt[j][k] = min(result[j][k], result[j][i] + result[i][k])
            result = deepcopy(nxt)

        return result

    # Given a list of distinct nodes, returns the "score" for their distances,
    # which is a sequence of numbers representing pairwise distances in sorted
    # order.
    def scoreOf(nodes, distances):
        result = []

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                result.append(distances[nodes[i]][nodes[j]])

        result.sort()

        return result

    # Lexicographical comparison of two lists; they're assumed to have the same length.
    def lexicographicallyFollows(lhs, rhs):
        for i in range(len(lhs)):
            if (lhs[i] != rhs[i]):
                return lhs[i] > rhs[i]

        return False

    # Given a grid, returns a combination of four nodes whose overall score
    # (sorted list of pairwise distances) is as large as possible in a
    # lexicographical sense.
    def remoteLocationsIn(distances):
        result = [ 0, 1, 2, 3 ]

        # We could do this recursively, but since it's "only" four loops
        # we'll just do that instead. :-)
        for i in range(len(distances)):
            for j in range(i + 1, len(distances)):
                for k in range(j + 1, len(distances)):
                    for l in range(k + 1, len(distances)):
                        curr = [ i, j, k, l ]
                        if (MazeUtils.lexicographicallyFollows(MazeUtils.scoreOf(curr, distances), MazeUtils.scoreOf(result, distances))):
                            result = deepcopy(curr)
        
        return result

    # Clears all the links between the given group of nodes.
    def clearGraph(nodes):
        for node in nodes:
            node._item = None
            node._N = node._S = node._E = node._W = None

    # Returns a random unassigned link from the given node, or None if
    # they are all assigned.
    def randomFreePortOf(cell):
        ports = []

        if (not cell._N):
            ports.append("N")
        if (not cell._S):
            ports.append("S")
        if (not cell._E):
            ports.append("E")
        if (not cell._W):
            ports.append("W")
        if (len(ports) == 0):
            return None

        return ports[randint(0, len(ports) - 1)]

    # Links one MazeCell to the next using the specified port.
    def link(frm, to, link):
        if (link == "N"):
            frm._N = to
        elif (link == "S"):
            frm._S = to
        elif (link == "E"):
            frm._E = to
        elif (link == "W"):
            frm._W = to
        else:
            raise RuntimeError("Unknown port!")

    # Use a variation of the Erdos-Renyi random graph model. We set the
    # probability of any pair of nodes being connected to be ln(n) / n,
    # then artificially constrain the graph so that no node has degree
    # four or more. We generate mazes this way until we find one that's
    # connected.
    def erdosRenyiLink(nodes):
        # high probability that everything is connected
        threshold = log(len(nodes)) / len(nodes)

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if (random() <= threshold):
                    iLink = MazeUtils.randomFreePortOf(nodes[i])
                    jLink = MazeUtils.randomFreePortOf(nodes[j])

                    # oops, no free links
                    if (not iLink or not jLink):
                        return False

                    MazeUtils.link(nodes[i], nodes[j], iLink)
                    MazeUtils.link(nodes[j], nodes[i], jLink)

        return True

    # Returns whether the given maze is connected. Uses a BFS.
    def isConnected(maze):
        visited = set()
        frontier = UnorderedList()

        frontier.add(maze[0])
        while (not frontier.is_empty()):
            curr = frontier.pop()

            if (not curr in visited):
                visited.add(curr)

                if (curr._N):
                    frontier.add(curr._N)
                if (curr._S):
                    frontier.add(curr._S)
                if (curr._E):
                    frontier.add(curr._E)
                if (curr._W):
                    frontier.add(curr._W)

        return len(visited) == len(maze)

    # Returns all possible edges that could appear in a grid maze.
    def allPossibleEdgesFor(maze):
        result = []

        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if (row + 1 < len(maze)):
                    result.append(MazeUtils.EdgeBuilder(maze[row][col], maze[row + 1][col], "S", "N"))
                if (col + 1 < len(maze[row])):
                    result.append(MazeUtils.EdgeBuilder(maze[row][col], maze[row][col + 1], "E", "W"))

        return result

    # Union-find FIND operation.
    def repFor(reps, cell):
        while (reps[cell] != cell):
            cell = reps[cell]

        return cell

    # Creates a random maze of the given size using a randomized Kruskal's
    # algorithm. Edges are shuffled and added back in one at a time, provided
    # that each insertion links two disconnected regions.
    def makeMaze(numRows, numCols):
        maze = [ [ MazeCell() for _ in range(numCols) ] for _ in range(numRows) ]
        edges = MazeUtils.allPossibleEdgesFor(maze)
        shuffle(edges)
        representatives = {}

        # union-find structure, done without path compression because N is small
        for row in range(numRows):
            for col in range(numCols):
                representatives[maze[row][col]] = maze[row][col]

        # run a randomized Kruskal's algorithm to build the maze.
        edgesLeft = numRows * numCols - 1
        i = 0
        while (i < len(edges) and edgesLeft > 0):
            edge = edges[i]

            # see if they're linked already
            rep1 = MazeUtils.repFor(representatives, edge._frm)
            rep2 = MazeUtils.repFor(representatives, edge._to)

            # if not, link them
            if (rep1 != rep2):
                representatives[rep1] = rep2
                MazeUtils.link(edge._frm, edge._to, edge._frmPort)
                MazeUtils.link(edge._to, edge._frm, edge._toPort)

                edgesLeft -= 1

            i += 1

        if (edgesLeft != 0):
            raise RuntimeError("Edges remain?!")

        return maze

    # Generates a random labyrinth. This works by repeatedly generating
    # random graphs until a connected one is found.
    def makeLabyrinth(numNodes):
        result = []

        for i in range(numNodes):
            result.append(MazeCell())

        # keep generating mazes until we get a connected one
        while (True):
            MazeUtils.clearGraph(result)

            if (MazeUtils.erdosRenyiLink(result) and MazeUtils.isConnected(result)):
                break

        return result

