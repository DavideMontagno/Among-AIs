from pathfinding.core.diagonal_movement import DiagonalMovement
import time
from pathfinding.core.grid import Grid, Node
import numpy as np
import random
import pickle

class VisualComponent():
    def __init__(self, cellular_automata,player):
        self.player = player
        self.cellular_automata=cellular_automata
        self.raw_map,_ = self.player.process_map()
        self.is_impostor = False
        self.set_information()
        self.dict_mapping_symbol_player={}
        self.flag_0, self.flag_1 = self.flag_position()
        self.players_pos = {}
        self.map_history=[]

    # Judge Humans
    def judge_humans(self):
        for player in self.players_pos.items():
            if(player[1].get('count') > 2):
                print(player[0])
                self.player.deduction_game("judge", str(player[0]),"H")
                player[1].update({'count' : -100})
                # self.players_pos.pop(player[0])

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
        raw_map,response = self.player.process_map()
        position_temp=np.where(raw_map == self.game_symbol)
        
        #Map letters->player
        
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

        self.player_position =(position_temp[0][0],position_temp[1][0])

    def save_maps(self):
        
        with open('ml_raw_data/'+self.player.game_name+'.pickle', 'wb') as handle:
            pickle.dump((self.player_enemies,self.game_symbol,self.map_history), handle)


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

    def get_mapping_symbol_players(self, status_result=[]):
        if(status_result==[]):
            status_result = self.player.status("status")

        #dict_mapping_symbol_player
        splitted = status_result.split()

        for i in range(15,len(splitted),7):
            symbol=splitted[i][7:]
            name=splitted[i+1][5:]
            self.dict_mapping_symbol_player[name]=symbol

        return 

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
        
        self.map_history.append(self.raw_map)

        grid_cellular_map = Grid()


        grid_cellular_map = Grid(
            width=len(self.raw_map[0]), height=len(self.raw_map))

        list_enemies_position=[]

        start_time = time.time()
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

                self.update_pos(current_cell, row, column)
                # self.judge_humans()

                grid_cellular_map.nodes[row][column] = Node(
                    x=column, y=row, walkable=walkable, weight=result)
        # Find AI's
        self.findAI()
        # Judge Humans
        self.judge_humans()
        
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
        
        print("--- %s seconds ---" % (time.time() - start_time))
        return grid_cellular_map, self.raw_map

    # Update the pos and prev_pos of each player
    def update_pos(self, current_cell, row, column):
        for player in self.players_pos.items():
            if (player[1].get('symbol') == current_cell):
                prev_pos = player[1].get('pos')
                player[1]['prev_pos'] = prev_pos
                player[1]['pos'] = (column, row)

    # see if a player switch his position like a human nad not like and AI
    def findAI(self):
        for player in self.players_pos.items():
            if(player[1]['team'] == '0'):
                if(player[1]['prev_pos'][0] > player[1]['pos'][0]):
                    player[1]['count'] += 1
            else:
                if(player[1]['prev_pos'][0] < player[1]['pos'][0]):
                    player[1]['count'] += 1

    # Initialize the dictionary with all players
    def check_players_pos(self, status_result=[]):
        if(status_result==[]):
            status_result = self.player.status("status")

        splitted = status_result.split()

        for i in range(15,len(splitted),7):
            symbol = splitted[i][7:]
            name = splitted[i+1][5:]
            team = splitted[i+2][5:]
            x = int(splitted[i+3][2:])
            y = int(splitted[i+4][2:])
            pos = (x,y)
            prev_pos = pos
            self.players_pos[name] = {'symbol' : symbol,'team' : team, 'pos' : pos, 'prev_pos' : prev_pos, 'count' : 0}

        print(self.players_pos)

        return self.players_pos

    def flag_position(self):
        flag_0 = np.where(self.raw_map == 'x')
        flag_1 = np.where(self.raw_map == 'X')

        return flag_0, flag_1
