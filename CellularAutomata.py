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
import matplotlib.pyplot as plt

import datetime


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
            print(self.player.interact("leave",text="No Flag in Map"))
            print("Error Flag")
            return False
        self.flag = (self.flag[0][0], self.flag[1][0])

        self.player_position = np.where(
            self.raw_map == self.player.game_symbol)
        self.player_position = (
            self.player_position[0][0], self.player_position[1][0])

        self.grid_cellular_map = Grid()




    def plot_grid(self):
        try:
            os.makedirs(str(self.player.game_name))
        except OSError as e:
            pass
        try:    
            cellcolours = np.empty_like(self.raw_map, dtype='object')
        except Exception as e: print(e)

        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):
                current_cell = self.raw_map[row][column]
                if(current_cell == "#"  ):
                    cellcolours[row][column] = 'k'
                elif(current_cell == "."):
                    cellcolours[row][column] = 'g'
                elif(current_cell == "@"):
                    cellcolours[row][column] = 'b'
                elif(current_cell == self.flag_symbol.swapcase()):
                    cellcolours[row][column] = 'r'
                elif(current_cell == self.flag_symbol):
                    cellcolours[row][column] = 'r'
                elif(current_cell == self.player.game_symbol):
                    cellcolours[row][column] = 'w'
                elif(current_cell == "~"):
                   cellcolours[row][column] = 'c'
                elif(current_cell == "$"):
                   cellcolours[row][column] = 'y'
                elif(current_cell == "!"):
                   cellcolours[row][column] = '0.75'
                elif(current_cell == "&"):
                   cellcolours[row][column] = '0.50'
                else:
                    cellcolours[row][column] = 'm'
        try: 
            fig, ax = plt.subplots(
            )
            ax.axis('off')
            the_table = ax.table(cellColours=cellcolours,loc='center')
            plt.savefig("./"+str(self.player.game_name)+"/fig_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"_"+str(self.player.player_name)+".png")
            plt.close(fig)
    
        except Exception as e: print(e)

    def update(self):
        self.raw_map=self.player.process_map()
        self.plot_grid()

        self.grid_cellular_map = Grid(width=len(self.raw_map), height=len(self.raw_map[0]))

        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):

                current_cell = self.raw_map[row][column]
                walkable = True
                if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&" or current_cell == self.flag_symbol.swapcase()):
                    result = -1
                    walkable = False
                elif(current_cell == "$"):
                    result = 4#distance.cityblock(self.flag,[row,column]).astype(int) -1
                    walkable = True
                elif(current_cell == self.flag):
                    result = 1
                    walkable = True
                else:
                    result = 5#distance.cityblock(self.flag,[row,column]).astype(int)
                    walkable = True


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
            print(self.player.interact("leave",text="No path found"))
            return 2
        
        
        #print(self.player.status("look"))
        #print(path)
        #print("Next_symbol: ", self.raw_map[path[1][0]][path[1][1]])

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
        #print(command_mov)
        # Victory
        if(self.raw_map[path_x][path_y] == self.flag_symbol):
            print(self.player.status("status"))
            print(self.player.interact("leave",text="Win Game"))
            print("Current player is in: ", path_x, path_y)
            return 1

        if("blocked" not in command_mov):
            self.player_position = (path_x, path_y)
        else:
            print(self.player.interact("leave",text="Movement fail"))
            print("Path Blocked")
            return 2

        return 0

    def play(self):
        while(True):
            result = self.update()
            result = self.move()
            if(result == 1):
                print(
                    "|||||||||||||||||||||||||||WIN|||||||||||||||||||||||||||||||||")
                return True
            if(result == 2):
                print(
                    "|||||||||||||||||||||||||||ERROR|||||||||||||||||||||||||||||||")
                return False

