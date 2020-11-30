from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import numpy as np

class VisualComponent():
    def __init__(self, player):
        self.player = player
        self.map = self.player.process_map()
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

    def getFlagPosition(self):
        return np.where(self.map == self.game_symbol)

    def get_enemies(self):
        return self.player_enemies

