from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
import numpy as np

class VisualComponent():
    def __init__(self, player):
        self.player = player
        self.raw_map = self.player.process_map()
        self.is_impostor = False
        self.set_information()

    def set_information(self):
        # Get game symbol
        result = self.player.status("status")
        index = result.find("ME: symbol=")
        self.game_symbol = result[index+11]
        # Get impostor
        index = result.find("loyalty=")
        if(result[index+8] == "0"):
            self.is_impostor = True

        # Get position
        index = result.find("PL: symbol="+self.game_symbol +
                            " name="+self.player.player_name+" team=")
        x1 = result[index+23+len(self.game_symbol)+len(self.player.player_name)+4]
        x2 = result[index+23+len(self.game_symbol)+len(self.player.player_name)+5]
        if(x2 == " "):
            y1 = result[index+23+len(self.game_symbol)+len(self.player.player_name)+8]
            y2 = result[index+23+len(self.game_symbol)+len(self.player.player_name)+9]
        else:
            y1 = result[index+23+len(self.game_symbol)+len(self.player.player_name)+9]
            y2 = result[index+23+len(self.game_symbol) +
                        len(self.player.player_name)+10]

        #Define Enemies
        if(self.is_impostor==False):
            if(self.game_symbol.islower()):
                self.player_enemies="upper"
            else:
                self.player_enemies="lower"
        else:
            if(self.game_symbol.islower()):
                self.player_enemies="lower"
            else:
                self.player_enemies="upper"

        self.player_position = (int(y1+y2), int(x1+x2))
    
    def get_allies_name(self, status_result=[]):
        if(status_result==[]):
            status_result = self.game_interface.status("status")

        list_allies=[]
        splitted = status_result.split()
        my_team=splitted[9]
        
        for i in range(15,len(splitted),7):
            name=splitted[i][5:]
            team=splitted[i+1]
            if(team==my_team):
                list_allies.append(name)
        
        return list_allies
        
    def findStrategy(self):
        pass

    def getFlag(self):
        if(self.game_symbol.islower()):
            return "X"
        else:
            return "x"

    def getLoyality(self):
        return self.is_impostor

    def getPlayerPosition(self):
        return self.player_position

    def getPlayerGameSymbol(self):
        return self.game_symbol

    def get_enemies(self):
        return self.player_enemies

    def getGridFromMap(self):
        self.raw_map,response = self.player.process_map()
        grid_cellular_map = Grid()
        '''if(self.debug):
            print(response)'''

        grid_cellular_map = Grid(
            width=len(self.raw_map), height=len(self.raw_map[0])) # perché qui si controlla la prima posizionie nella HEIGHT(e mi trovo), ma non nella width???

        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):

                current_cell = self.raw_map[row][column]
                walkable = True
                if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&"):
                    result = -1
                    walkable = False
                elif(current_cell == "$"):
                    # distance.cityblock(self.flag,[row,column]).astype(int) -1
                    result = 4
                    walkable = True
                elif(current_cell == self.getFlag() or current_cell == self.getFlag().swapcase()):
                    result = 1
                    walkable = True
                else:
                    # distance.cityblock(self.flag,[row,column]).astype(int)
                    result = 5
                    walkable = True

                grid_cellular_map.nodes[column][row] = Node(
                    x=row, y=column, walkable=walkable, weight=result)
        return grid_cellular_map