import numpy as np
from queue import PriorityQueue


def my_position(player, player_game, mappa):
    player.status("status")
    for i in range(mappa.shape[0]):
        for j in range(mappa.shape[1]):
            if mappa[i][j] == player_game:
                return (i, j)


def flag_position(player, player_game, mappa):
    mappa = player.process_map()
    if player_game.islower():
        flag = 'X'
    else:
        flag = 'x'

    for i in range(mappa.shape[0]):
        for j in range(mappa.shape[1]):
            if mappa[i][j] == flag:
                return (i, j)


# Path Finding
class PathFinder():

    def __init__(self, mappa, start, goal):
        self.mappa = mappa
        self.start = start
        self.goal = goal
        self.frontier = PriorityQueue()
        self.frontier.put(start, 0)
        self.came_from = dict()
        self.cost_so_far = dict()
        self.came_from[self.start] = None
        self.cost_so_far[self.start] = 0
        self.neighbords = []


    def map_cost(self, mappa, current):
        x_current = current[0]
        y_current = current[1]

        if mappa[x_current][y_current] == '#':
            return 100
        elif mappa[x_current][y_current] == '@':
            return 100
        elif mappa[x_current][y_current] == '!':
            return 100
        elif mappa[x_current][y_current] == '&':
            return 100
        elif mappa[x_current][y_current] == '~':
            return 20
        elif mappa[x_current][y_current] == '$':
            return 1
        elif mappa[x_current][y_current] == '.':
            return 1

        return 0


    def heuristic(self, a, b):
        # Manhattan Distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self):
        while not self.frontier.empty():
            self.current = self.frontier.get()
            self.neighbords = [(self.current[0] - 1, self.current[1]), (self.current[0], self.current[1]+1),
                               (self.current[0]+1, self.current[1]), (self.current[0], self.current[1]-1)]

#            if self.current == self.goal:
#                break

            for next in self.neighbords:
                if next[0] < 0 or next[1] < 0:
                    continue
                if next[0] > len(self.mappa) - 1 or next[1] > len(self.mappa) - 1:
                    continue

                new_cost = self.cost_so_far[self.current] + self.map_cost(self.mappa, self.current)
                if next not in self.cost_so_far or new_cost < self.cost_so_far[next]:
                    self.cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(self.goal, next)
                    self.frontier.put(next, priority)
                    self.came_from[next] = self.current

    def get_path(self):
        current = self.goal
        path = []
        while current != self.start:
            path.append(current)
            current = self.came_from[current]
        path.append(self.start)
        path.reverse()
        return path
