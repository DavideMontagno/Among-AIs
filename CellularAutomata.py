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
class CellularAutomata():
    def __init__(self, player, manager_dict, debug=False):
        self.finished = False
        self.game_interface = player
        self.debug = debug
        self.visual = VisualComponent(player)
        self.flag_symbol = self.visual.getFlag()
        self.loyality = self.visual.getLoyality()
        self.player_position = self.visual.getPlayerPosition()
        self.game_symbol = self.visual.getPlayerGameSymbol()
        self.enemies = self.visual.get_enemies()
        self.raw_map,_ = self.game_interface.process_map()
        self.flag = np.where(self.raw_map == self.flag_symbol)
        self.already_shoot = []
        self.last_shot = False
        if(self.flag == []):
            res = self.game_interface.interact("leave", text="No Flag in Map")
            if(self.debug):
                print(res)
                print("Error Flag")

        self.flag = (self.flag[0][0], self.flag[1][0])
        self.grid_cellular_map = Grid()
        self.consecutive_moves = 5
        self.path = []
        self.strategy = strategy = Strategies(visual=self.visual,debug=self.debug)
        self.manager_dict=manager_dict
        self.ai_list = []

        

    def update(self):
        self.raw_map,response = self.game_interface.process_map()

        if(self.debug):
            print(response)

        self.grid_cellular_map = Grid(
            width=len(self.raw_map), height=len(self.raw_map[0])) # perché qui si controlla la prima posizionie nella HEIGHT(e mi trovo), ma non nella width???

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

    def send_move(self,path_x,path_y,cooldown):
        
        direction = self.direction(path_x=path_x,path_y=path_y)
        command_mov = self.game_interface.interact("move", direction)
        if(self.debug):
                print(command_mov)
        # Da controllare se va bene inserirlo solo sotto
        # if(self.raw_map[path_x][path_y] == self.flag_symbol):
            # return 1

        if("blocked" not in command_mov):
            self.player_position = (path_x, path_y)
            return 0
        else:
            if(self.debug):
                print("I'm here with the player: "+self.game_interface.player_name)

            result = self.game_interface.status("status")
            index = result.find("GA: name="+self.game_interface.game_name+" "+"state=")
            condition = result[index+9+len(str(self.game_interface.game_name))+7]

            if(cooldown==False):
                if(self.raw_map[path_x][path_y] == self.flag_symbol and condition.lower() != "a"):
                    
                    return 1
            
            if(condition.lower() != "a"):# SE IL GIOCO È FINITO #
                print("Game Finished, no win")
                return 2
            else:
                if(self.loyality):
                    check = "PL: symbol="+self.game_symbol+" name="+self.game_interface.player_name+" team=0 x=" + \
                        str(self.player_position[0])+" y="+str(
                             self.player_position[1])+" state=ACTIVE"
                else:
                     check = "PL: symbol="+self.game_symbol+" name="+self.game_interface.player_name+" team=1 x=" + \
                         str(self.player_position[0])+" y="+str(
                             self.player_position[1])+" state=ACTIVE"
                #if(self.debug):
            #         print(check)
            #         print(result)

                
                if(check not in result):### se giocatore attivo va ricalcolato il path####
                     #self.path=[]

                #else:### se giocatore non attivo####
                     if(self.debug):
                         print("Player killed")
                     return 2
    def move(self,cooldown=False,movement=1):
       # Prima Mossa o errore precedente
        if(cooldown==False):
            self.path = self.strategy.getStrategy(cooldown=cooldown,position=self.player_position)
            if(self.visual.getLoyality()==True and len(self.path)==2): ##Impostore
                return 0
            if(self.debug): print(self.path)
            if(self.debug): print(self.path)
            if(self.debug): print("Player: "+self.visual.getPlayerGameSymbol()+" in position: "+str(self.player_position))
            # Path non trovato
            if(self.path == []):
                    res = self.game_interface.interact("leave", text="No path found")
                    if(self.debug):
                        print("No path")
                        print(res)
                    return 2
            #self.n_moves=1
            for i in range(1, self.consecutive_moves):

                self.game_interface.command_chat("post", text_chat="I'm moving")
                #print("Position "+str(i)+" on: "+str(self.path))
                path_x = self.path[i][0]
                path_y = self.path[i][1]

                
                result = self.send_move(path_x=path_x,path_y=path_y,cooldown=cooldown)
                
                
                if(result==1): return 1
                elif(result==2): return 2
                
                
        else:
            path_x = self.path[movement][0]
            path_y = self.path[movement][1]
            result = self.send_move(path_x=path_x,path_y=path_y,cooldown=cooldown)
            
            
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
                    self.already_shoot.append(elem)
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
                            print("ARRAY SHOOTED")
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
        if(elem in ['#', '&', 'X', 'x'] or elem in self.already_shoot):
            return True
        return False

    def play(self):
        ##### WAITING MATCH BEING STARTED #########
        while(True):
            result = self.game_interface.status("status")
            if(self.debug):
                print(result)
            index = result.find("GA: name="+self.game_interface.game_name+" "+"state=")
            condition = result[index+9+len(str(self.game_interface.game_name))+7]

            self.ai_list = self.visual.get_all_names(result)
            for ai in self.ai_list:
                print(self.game_interface.deduction_game("judge", ai,"AI"))
            humans = self.visual.change_behaviour(self.ai_list)
            for p in humans:
                print(self.game_interface.deduction_game("judge", p, "H"))

            if(condition.lower() == "a"):
                ######################################################Prendere lista giocatori con il nome
                
                self.manager_dict["allies"]=self.visual.get_allies_name(result)
                break
        
        start_time = time.time()
        most_pobable_impostor=""
        #### PLAYING MATCH #####
        while(True):
            
            self.update()
            
            if("impostors" in self.manager_dict):
                current_most_pobable_impostor=max(self.manager_dict["impostors"], key=self.manager_dict["impostors"].get)

                if(current_most_pobable_impostor!=most_pobable_impostor):
                    self.game_interface.deduction_game("accuse", current_most_pobable_impostor)
                    most_pobable_impostor=current_most_pobable_impostor

                    if(self.debug):
                        print("Find Impostor: ", most_pobable_impostor)
            first_time=True
            movement=1
            while((time.time() - start_time) < 30.0):
                if((time.time() - start_time) > 6.9):
                    self.update()
                    self.attack()
                if(movement!=(len(self.path)-1)):
                            if(first_time):
                                self.path = self.strategy.getStrategy(cooldown=True,position=self.player_position)
                                #print(self.path)
                                if(self.path==[]):
                                    res = self.game_interface.interact("leave", text="No path found")
                                    if(self.debug):
                                        print("No path")
                                        print(res)
                                    return 2
                                if(len(self.path)>0):
                                    self.move(cooldown=True,movement=movement)
                                    movement = movement+1
                                    first_time=False
                            else:
                                if(len(self.path)>0):
                                    self.move(cooldown=True,movement=movement)
                                    movement = movement+1

                #print((45 - (time.time() - start_time)))
                
            if(not(self.attack())):
                result = self.move(cooldown=False,movement=movement)

                if(result == 1):
                    print("--- %.2f seconds ---" % (time.time() - start_time))
                    print(
                        "|||||||||||||||||||||||||||WIN|||||||||||||||||||||||||||||||||")
                    stat = self.game_interface.status("status")
                    leave = self.game_interface.interact("leave", text="Win Game")
                    if(self.debug):
                        print(stat)
                        print(leave)
                    self.game_interface.finished = True
                    return True
                if(result == 2):
                    print("--- %.2f seconds ---" % (time.time() - start_time))
                    print(
                        "|||||||||||||||||||||||||||ERROR|||||||||||||||||||||||||||||||")
                    leave = self.game_interface.command_chat("leave")
                    if(self.debug):
                        print(leave)
                    return False
