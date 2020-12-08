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

    def getStrategy(self, position, cooldown=False):
        
        ### Taking new map 
        grid_cellular_map, raw_map = self.visual.getGridFromMap()

        
        ## Taking position for A*
        flag = np.where(raw_map == self.visual.getFlag())
        flag_opposite = np.where(raw_map == self.visual.getFlag().swapcase())

        ## Create nodes for A*
        start = grid_cellular_map.node(
                position[0], position[1])

        end_own = grid_cellular_map.node(flag[0][0],flag[1][0]) ##Bandiera da catturare
        end_opposite = grid_cellular_map.node(flag_opposite[0][0],flag_opposite[1][0]) #Propria bandiera

        if(self.visual.getLoyality()==True): ##Impostore
            if(self.debug): print("I'm an impostor so i'm rushing to opposite team flag")

            if(cooldown):
                if(self.debug): print("I'm an impostor.. i'm rushing to my own team flag")
                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path_opposite, _ = finder.find_path(start, end_opposite, grid_cellular_map) #Path per la propria bandierareturn path_opposite, raw_map
                return path_opposite, raw_map
            else:
               if(self.debug): print("I'm capturing the flag")
               grid_cellular_map.cleanup()
               finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
               path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare
               return path, raw_map

        else: ## PlayerNormale
            if(cooldown):

                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path_opposite, _ = finder.find_path(start, end_opposite, grid_cellular_map) #Path per la propria bandiera
                
                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare

                if(self.debug):
                    print("Distance from correct flag: "+str(len(path)))
                    print("Distance from opposite flag: "+str(len(path_opposite)))
                if(len(path)>len(path_opposite)): ### Stay in own base
                    if(self.debug): print("I'm going to my own base")
                    return path_opposite, raw_map
                else: # Go to capture the flag
                    if(self.debug): print("I'm capturing the flag")
                    return path, raw_map
            else:
               if(self.debug): print("I'm capturing the flag")

               grid_cellular_map.cleanup()
               finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
               path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare
               return path, raw_map
            


    
