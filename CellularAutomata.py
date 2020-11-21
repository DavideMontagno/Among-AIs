import random
import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import sys
import os

import datetime
import matplotlib.pyplot as plt



## Debug part
## Path faster


time_sleep=0.51
class CellularAutomata():
    def __init__(self, player):
        self.finished=False
        self.player = player

        if(self.player.game_symbol.islower()):
            self.flag_symbol = "X"
        else:
            self.flag_symbol = "x"
        self.raw_map = self.player.process_map()

        
        self.already_shoot=[]
        self.last_shot=False
        self.flag = np.where(self.raw_map == self.flag_symbol)

        if(self.flag == []):
            print(self.player.interact("leave", text="No Flag in Map"))
            print("Error Flag")

        self.flag = (self.flag[0][0], self.flag[1][0])

        self.player_position = np.where(
            self.raw_map == self.player.game_symbol)

        self.player_position = (self.player_position[0][0], self.player_position[1][0])

        self.grid_cellular_map = Grid()

    
    def update(self):
        self.raw_map = self.player.process_map()
        #self.plot_grid()

        self.grid_cellular_map = Grid(
            width=len(self.raw_map), height=len(self.raw_map[0]))

        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):

                current_cell = self.raw_map[row][column]
                walkable = True
                if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&" or current_cell == self.flag_symbol.swapcase()):
                    result = -1
                    walkable = False
                elif(current_cell == "$"):
                    # distance.cityblock(self.flag,[row,column]).astype(int) -1
                    result = 4
                    walkable = True
                elif(current_cell == self.flag):
                    result = 1
                    walkable = True
                else:
                    # distance.cityblock(self.flag,[row,column]).astype(int)
                    result = 5
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
            print(self.player.interact("leave", text="No path found"))
            return 2

        # print(self.player.status("look"))
        # print(path)
        #print("Next_symbol: ", self.raw_map[path[1][0]][path[1][1]])
        #number of movements/movement
        n_movement=3
        for i in range(1,n_movement):
            
            self.player.command_chat("post",text_chat="I'm moving")
            #print("Movement "+self.player.player_name+" "+str(i)+": ",path[i])
            path_x = path[i][0]
            path_y = path[i][1]

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
                print(self.player.interact("leave", text="Win Game"))
                print("Current player is in: ", path_x, path_y)
                self.player.finished=True
                return 1

            if("blocked" not in command_mov):
                self.player_position = (path_x, path_y)
            else:
                print("I'm here with the player: "+self.player.player_name)
                result = self.player.status("status")
                index=result.find("GA: name="+self.player.game_name+" "+"state=") 
                condition=result[index+9+len(str(self.player.game_name))+7]
                if(condition.lower()!="a"):
                      print(self.player.interact("leave", text="Game finished, no win!"))
                      return 2
                else:
                    if(self.player.is_impostor):
                        check="PL: symbol="+self.player.game_symbol+" name="+self.player.player_name+" team=0 x="+str(self.player_position[0])+" y="+str(self.player_position[1])+" state=ACTIVE"
                    else:
                        check="PL: symbol="+self.player.game_symbol+" name="+self.player.player_name+" team=1 x="+str(self.player_position[0])+" y="+str(self.player_position[1])+" state=ACTIVE"
                    print(check)
                    print(result)
                    ### se giocatore attivo####
                    if(check in result):
                    ###No path!
                        if(path == []):
                            print("No path")
                            print(self.player.interact("leave", text="No path found"))
                            return 2
                        else: #### Ricomincio!
                            self.update()
                            start = self.grid_cellular_map.node(
                            self.player_position[0], self.player_position[1])
                            path, _ = finder.find_path(start, end, self.grid_cellular_map)
                            i=1
                    ### se giocatore non attivo####
                    else:
                        print("Player killed")
                        print(self.player.interact("leave", text="Player killed, RIP!"))
                        return 2

                     
                    
                '''print(self.player.interact("leave", text="Movement fail"))
                print("Path Blocked")
                return 2'''

        return 0

    def attack(self):
        if(self.player_position[0] == (len(self.raw_map[0])-1)):
            if(self.player_position[1] != (len(self.raw_map[0])-1)):
                dict_shoot_direction={
                    "N": np.flip(self.raw_map[:self.player_position[0], self.player_position[1]]),
                    "S": self.raw_map[self.player_position[0]:, self.player_position[1]],
                    "E": self.raw_map[self.player_position[0], self.player_position[1]+1:],
                    "W": np.flip(self.raw_map[self.player_position[0], :self.player_position[1]])
                }
            else:
                dict_shoot_direction={
                    "N": np.flip(self.raw_map[:self.player_position[0], self.player_position[1]]),
                    "S": self.raw_map[self.player_position[0]:, self.player_position[1]],
                    "E": self.raw_map[self.player_position[0], self.player_position[1]:],
                    "W": np.flip(self.raw_map[self.player_position[0], :self.player_position[1]])
                }
        elif(self.player_position[1] == (len(self.raw_map[0])-1)):
            dict_shoot_direction={
                "N": np.flip(self.raw_map[:self.player_position[0], self.player_position[1]]),
                "S": self.raw_map[self.player_position[0]+1:, self.player_position[1]],
                "E": self.raw_map[self.player_position[0], self.player_position[1]:],
                "W": np.flip(self.raw_map[self.player_position[0], :self.player_position[1]])
            }
        else: 
            dict_shoot_direction={
                "N": np.flip(self.raw_map[:self.player_position[0], self.player_position[1]]),
                "S": self.raw_map[self.player_position[0]+1:, self.player_position[1]],
                "E": self.raw_map[self.player_position[0], self.player_position[1]+1:],
                "W": np.flip(self.raw_map[self.player_position[0], :self.player_position[1]])
            }
        for key in dict_shoot_direction:
            blocked=False# Testare l'utilizzo del break
            for elem in dict_shoot_direction[key]:
                if (self.is_unshottable(elem)):
                    blocked=True
                elif (self.is_enemy(elem) and blocked==False):
                    # Attualmente se ci sono 2 nemici sulla stessa linea spara 2 volte reinserendo il primo
                    #Quando verà implementata la kill sarà ok
                    print("***SHOOT***")
                    if(self.player.is_impostor):
                        print("IMPOSTOR-> ", self.player.game_symbol, " SHOOT ",elem)
                        
                    print("Elem: ",elem)
                    result = self.player.interact("shoot", direction=key)
                    print("RESULT: ", result)
                    if(result.lower().find("error")!=-1): 
                        print('Cannot Shoot')
                    else:
                        self.already_shoot.append(elem)
                        print("ARRAY SHOOTED")
                        print(self.already_shoot)
                    print("Vettore controlato: ")
                    print(key+": " + str(dict_shoot_direction[key]))
                    print("***ENDSHOOT***")

        if(not(self.last_shot)):
            return False
        else: 
            return True

    def is_enemy(self,elem):
        if(elem in ['@','.','~','$','!']):
            return False
        if(not self.player.is_impostor):
            if(self.player.game_symbol.islower() and elem.islower()):
                return False
            if(self.player.game_symbol.isupper() and elem.isupper()):
                return False
        else:
            if(self.player.game_symbol.islower() and elem.isupper()):
                return False
            if(self.player.game_symbol.isupper() and elem.islower()):
                return False
        return True
    
    def is_unshottable(self,elem):
        if(elem in ['#', '&','X','x'] or elem in self.already_shoot):
            return True
        return False

    def play(self):
        ##### WAITING MATCH BEING STARTED #########
        last_nop= time.clock()
        while(True):
            result = self.player.status("status")
            index=result.find("GA: name="+self.player.game_name+" "+"state=") 
            condition=result[index+9+len(str(self.player.game_name))+7]
            if(condition.lower()=="a"):
                break
            else:
                if(time.clock()-last_nop>10):
                    print(self.player.interact("nop"))
                    last_nop=time.clock()
                
                
        #### PLAYING MATCH #####
        while(True):
            self.update()
            #print(self.player.status("look"))
            
            if(not(self.attack())):
                result = self.move()

                if(result == 1):
                    print(
                        "|||||||||||||||||||||||||||WIN|||||||||||||||||||||||||||||||||")
                    
                    #print(self.player.command_chat("leave"))
                    return True
                if(result == 2):
                    print(
                        "|||||||||||||||||||||||||||ERROR|||||||||||||||||||||||||||||||")
                    #print(self.player.command_chat("leave"))
                    return False
           


    ##############################################UTILITY
    def plot_grid(self):
        try:
            os.makedirs(str(self.player.game_name))
        except OSError as e:
            pass
        try:
            cellcolours = np.empty_like(self.raw_map, dtype='object')
        except Exception as e:
            print(e)
        if(self.last_shot):
            player_color='k'
        else:
            player_color='w'

        for row in range(len(self.raw_map)):
            for column in range(len(self.raw_map[0])):
                current_cell = self.raw_map[row][column]
                if(current_cell == "#"):
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
                    cellcolours[row][column] = player_color
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
            plt.tight_layout()
            ax.axis('off')
            the_table = ax.table(cellColours=cellcolours, loc='center')
            plt.savefig("./"+str(self.player.game_name)+"/fig_"+datetime.datetime.now(
            ).strftime("%Y%m%d_%H%M%S")+"_"+str(self.player.player_name)+".png")
            plt.close(fig)

        except Exception as e:
            print(e)
        
        self.last_shot=False

   
        
            
