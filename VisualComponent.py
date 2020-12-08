from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
import numpy as np
import random

class VisualComponent():
    def __init__(self, cellular_automata,player):
        self.player = player
        self.cellular_automata=cellular_automata
        self.raw_map = self.player.process_map()
        self.is_impostor = False
        self.set_information()

    def change_behaviour(self, ai_list):
        #TODO define a strategy to remove the humans
        humans = []
        for player in ai_list:
            if(player == self.player.player_name):
                continue
            choise = random.randint(0,1)
            if(choise == 0):
                humans.append(player)
                # ai_list.remove(player)
            
        return humans

    def set_information(self):
        # Get game symbol
        result = self.player.status("status")
        index = result.find("ME: symbol=")
        self.game_symbol = result[index+11]

        # Get impostor
        index_l = result.find("loyalty=")
        index_t = result.find("team=")

        if(result[index_l+8] != result[index_t+5]):
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
            status_result = self.player.status("status")

        list_allies=[]
        splitted = status_result.split()
        my_team=splitted[10]

        for i in range(16,len(splitted),7):
            name=splitted[i][5:]
            team=splitted[i+1]
            if(team==my_team):
                list_allies.append(name)
 
        return list_allies
    def change_behaviour(self, ai_list):
         #TODO define a strategy to remove the humans
        humans = []
        for player in ai_list:
            if(player == self.player.player_name):
                continue
            choise = random.randint(0,1)
            if(choise == 0):
                humans.append(player)
                # ai_list.remove(player)

    def get_all_names(self, status_result=[]):
          if(status_result==[]):
              status_result = self.player.status("status")
 
          possible_ai = []
          splitted = status_result.split()
 
          for i in range(15, len(splitted), 7):
              ais = splitted[i+1][5:]
              possible_ai.append(ais)
 
          return possible_ai

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


        grid_cellular_map = Grid(
            width=len(self.raw_map[0]), height=len(self.raw_map))

        list_enemies_position=[]
        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):

                current_cell = self.raw_map[row][column]
                walkable = True
                if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&"):
                    result = -1
                    walkable = False
                elif(current_cell == "$"):
                    result = 2
                    walkable = True
                elif(current_cell == self.getFlag().swapcase()):
                    result = 5
                    walkable = True
                elif(self.cellular_automata.is_enemy(current_cell)):
                    result = 5
                    walkable = True
                    if(self.game_symbol!=current_cell and self.game_symbol!=self.getFlag()):
                        list_enemies_position.append((row, column))
                else:
                    result = 5
                    walkable = True

                grid_cellular_map.nodes[row][column] = Node(
                    x=column, y=row, walkable=walkable, weight=result)
        
        if(self.cellular_automata.mode == "007"):
            if(random.uniform(0, 1)>=self.cellular_automata.risk_007):

                next_move={}

                if(self.cellular_automata.player_position[0]+1<=len(self.raw_map[0])):
                    next_move["S"]=(self.cellular_automata.player_position[0]+1,self.cellular_automata.player_position[1])
                if(self.cellular_automata.player_position[0]-1>=0):
                    next_move["N"]=(self.cellular_automata.player_position[0]-1,self.cellular_automata.player_position[1])
                if(self.cellular_automata.player_position[1]-1<=0):
                    next_move["O"]=(self.cellular_automata.player_position[0],self.cellular_automata.player_position[1]-1)
                if(self.cellular_automata.player_position[1]+1<=len(self.raw_map)):
                    next_move["E"]=(self.cellular_automata.player_position[0],self.cellular_automata.player_position[1]+1)

                for key in next_move:
                    old_node = grid_cellular_map.nodes[next_move[key][0]][next_move[key][1]]
                    for enemy_position in list_enemies_position:
                        if(enemy_position[1]==next_move[key][1]):# Se la colonna è la stessa
                            grid_cellular_map.nodes[next_move[key][0]][next_move[key][1]] = Node(
                            x=next_move[key][1], y=next_move[key][0], walkable=old_node.walkable, weight=11)

                        if(enemy_position[0]==next_move[key][0]):# Se la riga è la stessa
                            grid_cellular_map.nodes[next_move[key][0]][next_move[key][1]] = Node(
                            x=next_move[key][1], y=next_move[key][0], walkable=old_node.walkable, weight=11)
        
        return grid_cellular_map, self.raw_map
