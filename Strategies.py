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
                position[1], position[0])

        end_own = grid_cellular_map.node(flag[1][0],flag[0][0])
        end_opposite = grid_cellular_map.node(flag_opposite[1][0],flag_opposite[0][0])

        if(self.visual.getLoyality()==True): ##Impostore
            if(cooldown):
                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path, _ = finder.find_path(start, end_opposite, grid_cellular_map) #Path per la bandiera da catturare
                path=[(elem[1],elem[0])for elem in path]
            else:
                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path, _ = finder.find_path(start, end_own, grid_cellular_map) #Path per la bandiera da catturare
                path=[(elem[1],elem[0])for elem in path]
            return path, raw_map ## Go to capture the flag
        else: ## PlayerNormale
            if(cooldown):

                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path_opposite, _ = finder.find_path(start, end_opposite, grid_cellular_map) #Path per la propria bandiera
                
                grid_cellular_map.cleanup()
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
                path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare
                
                path=[(elem[1],elem[0])for elem in path]
                path_opposite=[(elem[1],elem[0])for elem in path_opposite]
                if(self.debug):
                    print("Distance from correct flag: "+str(len(path)))
                    print("Distance from opposite flag: "+str(len(path_opposite)))
                if(len(path)>len(path_opposite)): ### Stay in own base
                    if(self.debug): print(self.visual.getPlayerGameSymbol()+": I'm going to my own base")
                    return path_opposite, raw_map
                else: # Go to capture the flag
                    if(self.debug): print(self.visual.getPlayerGameSymbol()+": I'm going to capture the flag")
                   
                    return path, raw_map
            else:
               if(self.debug): print(self.visual.getPlayerGameSymbol()+": I'm going to capture the flag")

               grid_cellular_map.cleanup()
               finder = AStarFinder(diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
               path, _ = finder.find_path(start, end_own, grid_cellular_map) ## Path per la bandiera da catturare
               path=[(elem[1],elem[0])for elem in path]
               return path, raw_map
            


    
