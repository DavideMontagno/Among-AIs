import random
import sys
import os
import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class CellularAutomata():
    def __init__(self, player):
        self.player = player
        self.raw_map = player.process_map()

        if(player.game_symbol.islower()):
            self.flag_symbol = "X"
        else:
            self.flag_symbol = "x"

        self.flag = np.where(self.raw_map == self.flag_symbol)
        self.flag = (self.flag[0][0], self.flag[1][0])
        self.cellular_map = np.zeros([len(self.raw_map[0]), len(self.raw_map)])

    def update(self):
        self.raw_map = self.player.process_map()

        for row in range(len(self.cellular_map[0])):
            for column in range(len(self.cellular_map)):
                current_cell = self.raw_map[row][column]
                if(current_cell == "#" or current_cell == "@"):
                    result = 256
                elif(current_cell == "&"):
                    result = distance.cityblock(self.flag, [row, column]) -10
                elif(current_cell == self.flag_symbol):
                    result = 0
                else:
                    result = distance.cityblock(self.flag, [row, column])
                self.cellular_map[row][ column] = result
        #print(self.cellular_map.astype(int))
    def move(self):

        grid = Grid(matrix=self.cellular_map.astype(int))
        player_position = np.where(self.raw_map == self.player.game_symbol)
        start = grid.node(player_position[0][0], player_position[1][0])
        end = grid.node(self.flag[0], self.flag[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, _ = finder.find_path(start, end, grid)
        print(path)
        player_position_x = player_position[0][0]
        player_position_y = player_position[1][0]
        path_x = path[1][0]
        path_y = path[1][1]
        direction = ""
        if(player_position_x < path_x ):
            direction = "S"
        elif(player_position_x > path_x ):
            direction = "N"
        elif(player_position_y > path_y):
            direction = "W"
        else:
            direction = "E"
        command_mov= self.player.interact("move",direction)
        if((command_mov.lower().find("ok blocked")!=-1) and (not(self.raw_map[path[1][0]][path[1][1]] == self.flag_symbol))):
            print("SONO QUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            print(self.player.interact("leave"))
            return 2

        if(self.raw_map[path[1][0]][path[1][1]] == self.flag_symbol):
            print(
            self.player.status("status"))
            print("Current player is in: ",np.where(self.raw_map == self.player.game_symbol))
            return 1

        return 0

    def play(self):
        while(True):
            self.update()
            if(self.move()==1):
                print(
                    "|||||||||||||||||||||||||||WIN!!!!!!!!!!!!!!|||||||||||||||||||||||||||||||||")
                break
            if(self.move()==2):
                print(
                    "|||||||||||||||||||||||||||TROUBLES!!!!!!!!!!!!!!|||||||||||||||||||||||||||||||||")
                break


