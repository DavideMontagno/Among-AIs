import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import datetime
from VisualComponent import VisualComponent


class CellularAutomata():
    def __init__(self, player, manager_dict, debug=False, consecutive_moves_no_shot=1, mode="kamikaze"):
        ################MODE
        #KAMIKAZE
            #Trova il path minimo e va dritto alla bandiera, 
            #cambia il path solo se si trova bloccato
        #007
            #Trova il path minimo controllando anche la posizione degli avversari
            #preferisce cammini più sicuri per raggiungere la bandiera
            #cambia sempre il path a seconda degli avversari
            #TODO: gestire il caso di 007 come impostore
        ################
        self.finished = False
        self.debug = debug
        self.already_shoot = []
        self.last_shot = False
        self.grid_cellular_map = Grid()
        self.consecutive_moves_no_shot = 1
        self.path = []
        self.mode = mode

        self.manager_dict = manager_dict

        self.game_interface = player
        self.visual = VisualComponent(player)
        self.flag_symbol = self.visual.getFlag()
        self.loyality = self.visual.getLoyality()
        self.player_position = self.visual.getPlayerPosition()
        self.game_symbol = self.visual.getPlayerGameSymbol()
        self.enemies = self.visual.get_enemies()
        self.raw_map, _ = self.game_interface.process_map()

        self.flag = np.where(self.raw_map == self.flag_symbol)

        if(self.flag == []):
            res = self.game_interface.interact("leave", text="No Flag in Map")
            if(self.debug):
                print(res)
                print("Error Flag")

        self.flag = (self.flag[0][0], self.flag[1][0])

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


    def move(self):
       # Prima Mossa o errore precedente o mod 007
        if(self.path == []):
            start = self.grid_cellular_map.node(
                self.player_position[0], self.player_position[1])
            end = self.grid_cellular_map.node(self.flag[0], self.flag[1])

            self.grid_cellular_map.cleanup()
            finder = AStarFinder(
                diagonal_movement=DiagonalMovement.never, time_limit=10000, max_runs=100000)
            self.path, _ = finder.find_path(start, end, self.grid_cellular_map)

            self.n_moves = 1

            if(self.path == []):  # Path non trovato
                res = self.game_interface.interact(
                    "leave", text="No path found")
                if(self.debug):
                    print("No path")
                    print(res)
                return 2

        for i in range(0, self.consecutive_moves_no_shot):

            path_x, path_y = self.path[self.n_moves][0], self.path[self.n_moves][1]

            direction = ""
            if(self.player_position[0] < path_x):
                direction = "S"
            elif(self.player_position[0] > path_x):
                direction = "N"
            elif(self.player_position[1] > path_y):
                direction = "W"
            else:
                direction = "E"

            command_mov = self.game_interface.interact("move", direction)

            self.n_moves += 1
            if(self.debug):
                print(command_mov)

            if("blocked" not in command_mov):
                self.player_position = (path_x, path_y)
            else:
                if(self.debug):
                    print("I'm here with the player: " +
                          self.game_interface.player_name)

                result = self.game_interface.status("status")
                index_game_active = result.find(
                    "GA: name="+self.game_interface.game_name+" "+"state=")
                condition_game_active = result[index_game_active +
                                               9+len(str(self.game_interface.game_name))+7]

                check_player_active = [True for elem in result.splitlines() if(
                    self.game_interface.player_name in elem and "ACTIVE" in elem)]

                # Vittoria
                if(self.raw_map[path_x][path_y] == self.flag_symbol and condition_game_active.lower() != "a"):
                    return 1

                # Se il gioco è finito
                if(condition_game_active.lower() != "a"):
                    print("Game Finished, no win")
                    return 2
                else:
                    # Se è ancora vivo
                    if(check_player_active == [True]):
                        self.path = []
                    else:
                        pass

        if(self.mode == "007"):
            self.path = []
        return 0

    def attack(self):
        # print(self.game_interface.deduction_game(command="accuse",player="pl6"))
        # print(self.game_interface.deduction_game(command="judge",player="pl6",player_nature="AI"))

        dict_shoot_direction = {
            "N": np.flip(self.raw_map[:self.player_position[0], self.player_position[1]]),
            "W": np.flip(self.raw_map[self.player_position[0], :self.player_position[1]]),
            "S": [],
            "E": []
        }
        # Check bordi mappa
        if(self.player_position[0] == (len(self.raw_map[0])-1)):

            dict_shoot_direction["S"] = self.raw_map[self.player_position[0]                                                     :, self.player_position[1]]

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
                    break
                elif (self.is_enemy(elem)):

                    result = self.game_interface.interact(
                        "shoot", direction=key)
                    self.already_shoot.append(elem)
                    self.last_shot = True

                    if(self.debug):
                        self.game_interface.command_chat(
                            "post", text_chat="shooting")
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

                    break

        return self.last_shot

    def manage_end(self, result, start_match):
        print("--- %.2f seconds ---" % (time.time() - start_match))

        if(result == 1):
            print(
                "|||||||||||||||||||||||||||WIN|||||||||||||||||||||||||||||||||")
            if(self.mode == "007"):
                file_object = open('sample.txt', 'a')
                file_object.write(self.visual.player.player_name+"\n")
                print("007 WIN "+self.visual.player.player_name)

            stat = self.game_interface.status("status")
            leave = self.game_interface.interact("leave", text="Win Game")
            if(self.debug):
                print(stat)
                print(leave)
            self.game_interface.finished = True
            return True

        if(result == 2):

            print(
                "|||||||||||||||||||||||||||ERROR|||||||||||||||||||||||||||||||")
            leave = self.game_interface.command_chat("leave")
            if(self.debug):
                print(leave)
            return False

    def check_impostors(self, most_probable_impostor):
        if("impostors" in self.manager_dict):
            current_most_pobable_impostor = max(
                self.manager_dict["impostors"], key=self.manager_dict["impostors"].get)

            if(current_most_pobable_impostor != most_probable_impostor):
                self.game_interface.deduction_game(
                    "accuse", current_most_pobable_impostor)
                most_pobable_impostor = current_most_pobable_impostor
                if(self.debug):
                    print("Find Impostor: ", most_pobable_impostor)
        return most_probable_impostor

    def wait_lobby(self):
        while(True):
            result = self.game_interface.status("status")
            if(self.debug):
                print(result)
            index = result.find(
                "GA: name="+self.game_interface.game_name+" "+"state=")
            condition = result[index+9 +
                               len(str(self.game_interface.game_name))+7]

            if(condition.lower() == "a"):
                # Prende il nome degli alleati
                self.manager_dict["allies"] = self.visual.get_allies_name(
                    result)
                break

    def is_enemy(self, elem):
        if(elem in ['@', '.', '~', '$', '!']):
            return False
        if(self.enemies == "upper" and elem.isupper()):
            return True
        elif(self.enemies == "lower" and elem.islower()):
            return True
        return False

    def is_unshottable(self, elem):
        if(elem in ['#', '&', 'X', 'x'] or elem in self.already_shoot):
            return True
        return False

    def play(self):
        ##### LOBBY #######################################################################

        self.wait_lobby()

        ####MATCH############################################################################
        start_match = time.time()
        most_probable_impostor = ""
        while(True):

            self.update()

            # GESTIONE ACCUSE
            most_probable_impostor = self.check_impostors(
                most_probable_impostor)

            # GESTIONE COOLDOWN
            if((time.time() - start_match) < 45.0):
                print("waiting")
            while((time.time() - start_match) < 45.0):
                # TODO
                pass

            # ATTACK AND MOVE
            if(not(self.attack())):
                result = self.move()
                if(result == 1 or result == 2):
                    return self.manage_end(result, start_match)
