import random
import sys
import os
import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder


class CellularAutomata():
    def __init__(self, player):

        self.player = player

        if(self.player.game_symbol.islower()):
            self.flag_symbol = "X"
        else:
            self.flag_symbol = "x"

        self.raw_map = self.player.process_map()

        self.flag = np.where(self.raw_map == self.flag_symbol)
        if(self.flag==[]):
            print("Error Flag")
            exit()
        self.flag = (self.flag[0][0], self.flag[1][0])

        self.player_position = np.where(
            self.raw_map == self.player.game_symbol)
        self.player_position = (
            self.player_position[0][0], self.player_position[1][0])

        self.grid_cellular_map = Grid()

    def update(self):
        self.raw_map=self.player.process_map()

        self.grid_cellular_map = Grid(
            width=len(self.raw_map), height=len(self.raw_map[0]))

        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):

                current_cell = self.raw_map[row][column]
                walkable = True
                if(current_cell == "#" or current_cell == "@" or current_cell == "&" or current_cell == self.flag_symbol.swapcase()):
                    result = -1
                    walkable = False
                else:
                    result = 1

                self.grid_cellular_map.nodes[column][row] = Node(
                    x=row, y=column, walkable=walkable, weight=result)

    def move(self):

        start = self.grid_cellular_map.node(
            self.player_position[0], self.player_position[1])
        end = self.grid_cellular_map.node(self.flag[0], self.flag[1])

        self.grid_cellular_map.cleanup()
        finder = AStarFinder(
            diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
        path, _ = finder.find_path(start, end, self.grid_cellular_map)

        if(path == []):
            print("No path")
            return 2
        
        
        print(self.player.status("look"))
        print(path)
        print("Next_symbol: ", self.raw_map[path[1][0]][path[1][1]])

        path_x = path[1][0]
        path_y = path[1][1]

        direction = ""
        if(self.player_position[0] < path_x):
            direction = "S"
        elif(self.player_position[0] > path_x):
            direction = "N"
        elif(self.player_position[1] > path_y):
            direction = "W"
        else:
            direction = "E"

        command_mov = self.player.interact("move", direction)
        print(command_mov)
        # Victory
        if(self.raw_map[path_x][path_y] == self.flag_symbol):
            print(self.player.status("status"))
            print("Current player is in: ", path_x, path_y)
            return 1

        if("blocked" not in command_mov):
            self.player_position = (path_x, path_y)
        else:
            print("Path Blocked")
            return 2

        return 0

    def play(self):
        while(True):
            self.update()
            result = self.move()
            if(result == 1):
                print(
                    "|||||||||||||||||||||||||||WIN|||||||||||||||||||||||||||||||||")
                break
            if(result == 2):
                print(
                    "|||||||||||||||||||||||||||ERROR|||||||||||||||||||||||||||||||")
                break
