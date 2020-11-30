import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import datetime
from FindStrategy import FindStrategy

class CellularAutomata():
    def __init__(self, player, debug=False):
        self.finished = False
        self.player = player
        self.debug = debug
        strategy = FindStrategy(player)
        self.flag_symbol = strategy.getFlag()
        self.loyality = strategy.getLoyality()
        self.player_position = strategy.getPlayerPosition()
        self.game_symbol = strategy.getPlayerGameSymbol()
        self.raw_map = self.player.process_map()

        self.already_shoot = []
        self.last_shot = False
        self.flag = np.where(self.raw_map == self.flag_symbol)
        if(self.flag == []):
            res = self.player.interact("leave", text="No Flag in Map")
            if(self.debug):
                print(res)
                print("Error Flag")

        self.flag = (self.flag[0][0], self.flag[1][0])

        self.grid_cellular_map = Grid()

    def idle(self):
        pass

    def update(self):
        self.raw_map = self.player.process_map()

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
            res = self.player.interact("leave", text="No path found")
            if(self.debug):
                print("No path")
                print(res)
            return 2

        # print(self.player.status("look"))
        # print(path)
        #print("Next_symbol: ", self.raw_map[path[1][0]][path[1][1]])
        # number of movements/movement
        n_movement = 2
        for i in range(1, n_movement):

            self.player.command_chat("post", text_chat="I'm moving")
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
            if(self.debug):
                print(command_mov)

            # Victory
            if(self.raw_map[path_x][path_y] == self.flag_symbol):
                stat = self.player.status("status")
                leave = self.player.interact("leave", text="Win Game")
                if(self.debug):
                    print(stat)
                    print(leave)
                    print("Current player is in: ", path_x, path_y)
                self.player.finished = True
                return 1

            if("blocked" not in command_mov):
                self.player_position = (path_x, path_y)
            else:
                if(self.debug):
                    print("I'm here with the player: "+self.player.player_name)
                result = self.player.status("status")
                index = result.find(
                    "GA: name="+self.player.game_name+" "+"state=")
                condition = result[index+9+len(str(self.player.game_name))+7]
                # SE IL GIOCO È FINITO =>
                if(condition.lower() != "a"):
                    leave = self.player.interact(
                        "leave", text="Game finished, no win!")
                    if(self.debug):
                        print(leave)
                    return 2
                else:
                    if(self.loyality):
                        check = "PL: symbol="+self.game_symbol+" name="+self.player.player_name+" team=0 x=" + \
                            str(self.player_position[0])+" y="+str(
                                self.player_position[1])+" state=ACTIVE"
                    else:
                        check = "PL: symbol="+self.game_symbol+" name="+self.player.player_name+" team=1 x=" + \
                            str(self.player_position[0])+" y="+str(
                                self.player_position[1])+" state=ACTIVE"
                    if(self.debug):
                        print(check)
                        print(result)
                    ### se giocatore attivo####
                    if(check in result):
                        # Se nessun path
                        if(path == []):
                            leave = self.player.interact(
                                "leave", text="No path found")
                            if(self.debug):
                                print(leave)
                                print("No path")
                            return 2
                        else:  # Ricomincio!
                            self.update()
                            start = self.grid_cellular_map.node(
                                self.player_position[0], self.player_position[1])
                            path, _ = finder.find_path(
                                start, end, self.grid_cellular_map)
                            i = 1
                    ### se giocatore non attivo####
                    else:
                        leave = self.player.interact(
                            "leave", text="Player killed, RIP!")
                        if(self.debug):
                            print(leave)
                            print("Player killed")
                        return 2

                '''print(self.player.interact("leave", text="Movement fail"))
                print("Path Blocked")
                return 2'''

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

                    result = self.player.interact("shoot", direction=key)
                    self.already_shoot.append(elem)
                    self.last_shot = True

                    if(self.debug):
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

        if(self.last_shot):
            return True
        else:
            return False

    def is_enemy(self, elem):
        if(elem in ['@', '.', '~', '$', '!']):
            return False
        if(not self.loyality):
            if(self.game_symbol.islower() and elem.islower()):
                return False
            if(self.game_symbol.isupper() and elem.isupper()):
                return False
        else:
            if(self.game_symbol.islower() and elem.isupper()):
                return False
            if(self.game_symbol.isupper() and elem.islower()):
                return False
        return True

    def is_unshottable(self, elem):
        if(elem in ['#', '&', 'X', 'x'] or elem in self.already_shoot):
            return True
        return False

    def play(self):
        ##### WAITING MATCH BEING STARTED #########
        while(True):
            result = self.player.status("status")
            if(self.debug):
                print(result)
            index = result.find("GA: name="+self.player.game_name+" "+"state=")
            condition = result[index+9+len(str(self.player.game_name))+7]

            if(condition.lower() == "a"):
                break

        #### PLAYING MATCH #####
        while(True):

            self.update()
            if(self.debug):
                print(self.player.status("look"))

            if(not(self.attack())):
                result = self.move()

                if(result == 1):
                    print(
                        "|||||||||||||||||||||||||||WIN|||||||||||||||||||||||||||||||||")

                    # print(self.player.command_chat("leave"))
                    return True
                if(result == 2):
                    print(
                        "|||||||||||||||||||||||||||ERROR|||||||||||||||||||||||||||||||")
                    # print(self.player.command_chat("leave"))
                    return False
