import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import datetime
from VisualComponent import VisualComponent


class Strategies():
    def __init__(self,visual,debug=False):
        self.debug = debug
        self.visual = visual

    def getStrategy(self,position,cooldown=False):
        
        ### Taking new map 
        grid_cellular_map = self.visual.getGridFromMap()
        #grid_cellular_map_opposite = self.visual.getGridFromMap()
        #### Defining A-Star
        finder = AStarFinder(
                diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)

        if(position!=[]): actual_position = position
        
        ## Taking position for A*
        flag = np.where(self.visual.raw_map == self.visual.getFlag())
        flag_opposite = np.where(self.visual.raw_map == self.visual.getFlag().swapcase())
        
        

        ## Create nodes for A*
        start = grid_cellular_map.node(
                actual_position[0], actual_position[1])
        end_own = grid_cellular_map.node(flag[0][0],flag[1][0])
        end_opposite = grid_cellular_map_opposite.node(flag_opposite[0][0],flag_opposite[1][0]) ## Flag my team!
        start_opposite = grid_cellular_map_opposite.node(
                actual_position[0], actual_position[1])


        if(self.visual.getLoyality()==True): ##Impostore
            if(self.debug): print("I'm an impostor so i'm rushing to opposite team flag")
            
            grid_cellular_map.cleanup()
            path, _ = finder.find_path(start, end_opposite, grid_cellular_map) #Path per la bandiera da catturare
            return path ## Go to capture the flag
        else: ## PlayerNormale
            if(cooldown):
                grid_cellular_map.cleanup()
                path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare
                grid_cellular_map.cleanup()
                path_opposite, _ = finder.find_path(start_opposite, end_opposite, grid_cellular_map) #Path per la propria bandiera
                if(self.debug):
                    print("Distance from correct flag: "+str(len(path)))
                    print("Distance from opposite flag: "+str(len(path_opposite)))
                if(len(path)>len(path_opposite)): ### Stay in own base
                    if(self.debug): print("I'm going to my own base")
                    return path_opposite
                else: # Go to capture the flag
                    if(self.debug): print("I'm capturing the flag")
                    return path
            else:
               if(self.debug): print("I'm capturing the flag")
               path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare
               return path 
            


    