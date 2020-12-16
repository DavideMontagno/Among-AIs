import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import datetime
from VisualComponent import VisualComponent
from Strategies import Strategies
import random

class CellularAutomata():
    def __init__(self, game_interface, manager_dict, debug=False, consecutive_moves_no_shot=1, risk_007=0.1, mode="kamikaze"):
        ################MODE
        #KAMIKAZE
            #Trova il path minimo e va dritto alla bandiera, 
            #cambia il path solo se si trova bloccato
        #007
            #Trova il path minimo controllando anche la posizione degli avversari
            #preferisce cammini più sicuri per raggiungere la bandiera
            #cambia sempre il path a seconda degli avversari
            #Ha una percentuale di rischio impostabile
        ################
        self.debug = debug
        self.already_shoot = []
        self.last_shot = False
        self.grid_cellular_map = Grid()
        self.consecutive_moves_no_shot = consecutive_moves_no_shot
        self.path = []
        self.mode = mode
        self.risk_007=risk_007

        self.manager_dict=manager_dict

        self.game_interface = game_interface

        self.visual = VisualComponent(self,game_interface)
        self.strategy = Strategies(visual=self.visual,debug=self.debug)

        self.flag_symbol = self.visual.getFlag()
        self.loyality = self.visual.getLoyality()
        self.player_position = self.visual.getPlayerPosition()
        self.game_symbol = self.visual.getPlayerGameSymbol()
        self.enemies = self.visual.get_enemies()
        self.raw_map,_ = self.game_interface.process_map()

        self.flag = np.where(self.raw_map == self.flag_symbol)
        
        if(self.flag == []):
            res = self.game_interface.interact("leave", text="No Flag in Map")
            if(self.debug):
                print(res)
                print("Error Flag")

        self.flag = (self.flag[0][0], self.flag[1][0])

        

        '''
        def update(self):
            self.raw_map, response = self.game_interface.process_map()

            if(self.debug):
                print(response)

            self.grid_cellular_map = Grid(
                width=len(self.raw_map), height=len(self.raw_map[0]))

            list_enemies_position = []
            for row in range(len(self.raw_map)):
                for column in range(len(self.raw_map[0])):

                    current_cell = self.raw_map[row][column]
                    walkable = True
                    if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&" or current_cell == self.flag_symbol.swapcase()):
                        result = -1
                        walkable = False
                    elif(current_cell == "$"):
                        result = 2
                        walkable = True
                    elif(self.is_enemy(current_cell)):
                        result = 5
                        walkable = True
                        if(self.visual.game_symbol!=current_cell and self.visual!=self.flag_symbol):
                            list_enemies_position.append((row, column))
                    else:
                        result = 5
                        walkable = True

                    self.grid_cellular_map.nodes[column][row] = Node(
                        x=row, y=column, walkable=walkable, weight=result)

            if(self.mode == "007"):
                if(random.uniform(0, 1)>=self.risk_007):

                    next_move={}

                    if(self.player_position[0]+1<=len(self.raw_map)):
                        next_move["S"]=(self.player_position[0]+1,self.player_position[1])
                    if(self.player_position[0]-1>=0):
                        next_move["N"]=(self.player_position[0]-1,self.player_position[1])
                    if(self.player_position[1]-1<=0):
                        next_move["O"]=(self.player_position[0],self.player_position[1]-1)
                    if(self.player_position[1]+1<=len(self.raw_map)):
                        next_move["E"]=(self.player_position[0],self.player_position[1]+1)

                    for key in next_move:
                        old_node = self.grid_cellular_map.nodes[next_move[key][0]][next_move[key][1]]
                        for enemy_position in list_enemies_position:
                            if(enemy_position[1]==next_move[key][1]):# Se la colonna è la stessa
                                self.grid_cellular_map.nodes[next_move[key][1]][next_move[key][0]] = Node(
                                x=next_move[key][0], y=next_move[key][1], walkable=old_node.walkable, weight=11)

                            if(enemy_position[0]==next_move[key][0]):# Se la riga è la stessa
                                self.grid_cellular_map.nodes[next_move[key][1]][next_move[key][0]] = Node(
                                x=next_move[key][0], y=next_move[key][1], walkable=old_node.walkable, weight=11)
    '''

    def direction(self,path_x,path_y):
        direction = ""
        if(self.player_position[0] < path_x):
            direction = "S"
        elif(self.player_position[0] > path_x):
            direction = "N"
        elif(self.player_position[1] > path_y):
            direction = "W"
        else:
            direction = "E"
        return direction

    def send_move(self,path_x,path_y):
        
        direction = self.direction(path_x=path_x,path_y=path_y)
        command_mov = self.game_interface.interact("move", direction)

        if(self.debug):
            print(command_mov)

        if("blocked" not in command_mov):
            self.player_position = (path_x, path_y)
            return 0
        else:
            if(self.debug):
                print("I'm here with the player: "+self.game_interface.player_name)

            result = self.game_interface.status("status")
            index = result.find("GA: name="+self.game_interface.game_name+" "+"state=")
            
            condition_game_active = result[index+9+len(str(self.game_interface.game_name))+7]

            check_player_active = [True for elem in result.splitlines() if(
                    self.game_interface.player_name in elem and "ACTIVE" in elem)]

            if(self.cooldown==False):
                if(self.raw_map[path_x][path_y] == self.flag_symbol and condition_game_active.lower() != "a"):
                    return 1
            
            if(condition_game_active.lower() != "a"):# SE IL GIOCO È FINITO #
                print(self.game_interface.player_name+" Game Finished, no win")
                return 2
            else:
                if(check_player_active == [True]):
                    self.path = []
                    return 0
                else:
                    if(self.debug):
                        print(self.game_interface.player_name+" Player killed")
                    return 3# TODO gestire uscita/restare in gioco se kilato

    def move(self):
       
        if(self.loyality==True and len(self.path)==2): #Se è impostore e se è arrivato alla flag del proprio team non fare nulla
            if("finish" in self.manager_dict):
                return 2
            return 0
             
        if(self.debug): print(self.path)
        if(self.debug): print("Player: "+self.game_symbol+" in position: "+str(self.player_position))

        # Path non trovato
        if(self.path == []):
                res = self.game_interface.interact("leave", text="No path found")
                if(self.debug):
                    print("No path")
                    print(res)
                return 2

        for i in range(0, self.consecutive_moves_no_shot):

            #self.game_interface.command_chat("post", text_chat="I'm moving")
            
            path_x = self.path[i+1][0]
            path_y = self.path[i+1][1]

            if(self.debug):
                print("Prossima mossa: ",path_x,path_y)

            result = self.send_move(path_x=path_x,path_y=path_y)
            
            if(result!=0):
                return result
                    
        return 0

    def attack(self):
        dict_shoot_direction = {
            "N": np.flip(self.raw_map[:self.player_position[0], self.player_position[1]]),
            "W": np.flip(self.raw_map[self.player_position[0], :self.player_position[1]]),
            "S": [],
            "E": []
        }

        # Check bordi della mappa

        if(self.player_position[0] == (len(self.raw_map[0])-1)):

            dict_shoot_direction["S"] = self.raw_map[self.player_position[0]:, self.player_position[1]]

            if(self.player_position[1] != (len(self.raw_map[0])-1)):
                dict_shoot_direction["E"] = self.raw_map[self.player_position[0],
                                                         self.player_position[1]+1:]
            else:
                dict_shoot_direction["E"] = self.raw_map[self.player_position[0],
                                                         self.player_position[1]:]
        else:
            dict_shoot_direction["S"] = self.raw_map[self.player_position[0] +
                                                     1:, self.player_position[1]]

            if(self.player_position[1] == (len(self.raw_map[0])-1)):
                dict_shoot_direction["E"] = self.raw_map[self.player_position[0],
                                                         self.player_position[1]:]
            else:
                dict_shoot_direction["E"] = self.raw_map[self.player_position[0],
                                                         self.player_position[1]+1:]

        self.last_shot = False
        for key in dict_shoot_direction:
            for elem in dict_shoot_direction[key]:
                if (self.is_unshottable(elem)):
                    break   # Se trova un elemento che blocca lo sparo smette di controllare il vettore corrente
                elif (self.is_enemy(elem)):

                    result = self.game_interface.interact("shoot", direction=key)
                    self.last_shot = True

                    if(self.debug):
                        self.game_interface.command_chat("post", text_chat="shooting")
                        print("***SHOOT***")
                        if(self.loyality):
                            print("IMPOSTOR-> ", self.game_symbol,
                                  " SHOOT ", elem)
                        print("Elem: ", elem)

                        print("RESULT: ", result)
                        if(result.lower().find("error") != -1):
                            print('Cannot Shoot')
                        else:
                            print("ARRAY SHOOTED prima dello sparo")
                            print(self.already_shoot)
                            print("Vettore controllato: ")
                            print(key+": " + str(dict_shoot_direction[key]))
                            print("***ENDSHOOT***")

                    break   # Se spara in una direzione non controlla gli altri elementi in quella direzione

        return self.last_shot

    def is_enemy(self, elem):
        if(elem in ['@', '.', '~', '$', '!']):
            return False
        if(self.enemies=="upper" and elem.isupper()):
            return True
        elif(self.enemies=="lower" and elem.islower()):
            return True
        return False

    def is_unshottable(self, elem):
        if("already_shooted_name" in self.manager_dict):
            self.already_shoot=[self.visual.dict_mapping_symbol_player[elem] for elem in self.manager_dict["already_shooted_name"]]
        
        if(elem in ['#', '&', 'X', 'x'] or elem in self.already_shoot):
            return True
        return False

    def check_impostors(self, most_probable_impostor):
        if("impostors" in self.manager_dict):
            current_most_probable_impostor = max(
                self.manager_dict["impostors"], key=self.manager_dict["impostors"].get)

            if(current_most_probable_impostor != most_probable_impostor and current_most_probable_impostor!=self.game_interface.player_name):
                self.game_interface.deduction_game("accuse", current_most_probable_impostor)
                most_probable_impostor = current_most_probable_impostor
                if(self.debug):
                    print("Find Impostor: ", most_probable_impostor)
        return most_probable_impostor

    def manage_end(self, result, start_match):

        if(result == 1):
            print("--- %.2f seconds --- "%(time.time() - start_match)+
                "|||||||||||||||||||||||||||WIN "+self.game_interface.player_name+" "+self.mode+"|||||||||||||||||||||||||||||||||")
            
            return 1

        if(result == 2 or result == 3):
            error_information=""
            if(result==3):
                error_information="killed"
            else:
                error_information="game_finished"

            print(
                "|||||||||||||||||||||||||||ERROR"+self.game_interface.player_name+" "+self.mode+" "+error_information+"|||||||||||||||||||||||||||||||")

            return 0

    def wait_lobby(self):
        while(True):

            result = self.game_interface.status("status")
            if("start_match" in self.manager_dict):
                self.manager_dict["allies"] = self.visual.get_allies_name(result)
                self.visual.get_mapping_symbol_players(result)

                #####JUDGE###########
                self.ai_list = self.visual.get_all_names(result)
                for ai in self.ai_list:
                    self.game_interface.deduction_game("judge", ai,"AI")
                break

    def play(self, starting=False):

        print(self.game_interface.player_name+" is in!!!")
        ######CREATION#######################################################
        if(starting==True):
            print("CREATION, wait 30 seconds")
            time.sleep(30)
            if(self.game_interface.manage_game("start").lower().find("error")!=-1):
                print("ERRORE CREAZIONE")
                exit()
            else: print("Started")

        ##### LOBBY #######################################################################
        self.wait_lobby()
        
        ####MATCH############################################################################
        start_time = time.time()
        most_probable_impostor = ""
        
        #####TIME ESTIMATE ######################################
        self.cooldown=False
        self.path, self.raw_map = self.strategy.getStrategy(cooldown=self.cooldown,position=self.player_position)
        estimate_time=len(self.path)*(self.game_interface.command_time_sleep+self.game_interface.default_time_sleep)
        self.cooldown=True

        #####COOLDOWN##############################
        print("COOLDOWN")
        self.cooldown=True
        self.path, self.raw_map = self.strategy.getStrategy(cooldown=self.cooldown,position=self.player_position)
        if(self.debug):print(self.path)
        if(self.path==[]):
            res = self.game_interface.interact("leave", text="No path found")
            if(self.debug):
                print("No path")
                print(res)
            return 2

        while(start_time+30-estimate_time>=time.time()):
        #while("cooldown_catch_end" not in self.manager_dict):
            most_probable_impostor=self.check_impostors(most_probable_impostor)

            self.path, self.raw_map = self.strategy.getStrategy(cooldown=self.cooldown,position=self.player_position)
                
            if("cooldown_shot_end" in self.manager_dict):
                self.attack()
                pass

            if(len(self.path)>0):
                self.move()
        

        ####PLAYING_MATCH###################
        print("MATCH")
        self.cooldown=False
        while(True):
            
            self.path, self.raw_map = self.strategy.getStrategy(cooldown=self.cooldown,position=self.player_position)
        
            # GESTIONE ACCUSE
            most_probable_impostor = self.check_impostors(most_probable_impostor)

            if(not(self.attack())):
                result = self.move()
                if(result >= 1):
                    return self.manage_end(result, start_time)
                
