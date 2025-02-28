import telnetlib
import time
import numpy as np
import re

default_time_sleep=0.50
command_time_sleep=0.30

class GameInterface:
    def __init__(self,  game_name, chat_name, player_name, player_nature="AI", player_descr="", flags="Q1",host="margot.di.unipi.it", port=8421, chat_port=8422):
        self.host = host
        self.port = port
        self.chat_port = chat_port
        self.game_name = game_name
        self.chat_name = chat_name
        self.chat_name_log=chat_name+"-L"
        self.player_nature = player_nature
        self.is_impostor = False
        self.player_name = player_name
        self.game_symbol = self.player_name
        self.player_descr = player_descr
        self.player_position = (0, 0)
        self.connection = telnetlib.Telnet(self.host, self.port)
        self.chat = telnetlib.Telnet(self.host, self.chat_port)
        self.chat_log=None

        self.timestamp_last_command = time.clock()

        self.command_time_sleep=command_time_sleep
        self.default_time_sleep=default_time_sleep

        self.flags=flags

        if("T" in self.flags):
            self.command_time_sleep=0.005

        


    def wait_last_command(self, time_mode="default"):
        if(time_mode=="default"):
            while(time.clock()-self.timestamp_last_command <= self.default_time_sleep):
                pass
        else:
            while(time.clock()-self.timestamp_last_command <= self.command_time_sleep):
                pass

    def interact(self, command, direction="", text=""):

        switcher = {"move": self.game_name+" MOVE "+direction+"\n",
                    "shoot": self.game_name+" SHOOT "+direction+"\n",
                    "join": self.game_name+" JOIN "+self.player_name+" "+self.player_nature+" - "+self.player_descr+"\n",
                    "leave": self.game_name+" LEAVE "+self.player_name+" "+text,
                    "nop": self.game_name+" NOP\n"

                    }

        actual = switcher.get(command, "Invalid Command")

        if(command=="join"):
            self.wait_last_command(time_mode="default")
        else:
            self.wait_last_command(time_mode="game")
        
        self.connection.write(bytes(actual, "utf-8"))
        result=""
        if(command!="leave"):
            result = str(self.connection.read_until(
            b"\n").decode("utf-8"))

        self.timestamp_last_command = time.clock()
        return actual+" "+result

    def status(self, command):
        switcher = {"look": self.game_name+" LOOK\n",
                    "status": self.game_name+" STATUS\n"}

        actual = switcher.get(command, "Invalid Command")

        self.wait_last_command(time_mode="game")#CHANGED
    
        self.connection.write(bytes(actual, "utf-8"))
        result = str(self.connection.read_until(
            b"\xc2\xbb\n").decode("utf-8"))

        self.timestamp_last_command = time.clock()
        
        return result

    def manage_game(self, command):

        switcher = {"new": "NEW "+self.game_name+" "+self.flags+"\n",
                    "start": self.game_name+" START\n"}

        actual = switcher.get(command, "Invalid Command")

        self.wait_last_command(time_mode="default")

        self.connection.write(bytes(actual, "utf-8"))

        result = str(self.connection.read_until(
            b"\n").decode("utf-8"))
        print(result)

        self.timestamp_last_command = time.clock()

        return result

    def process_map(self):
        map_matrix = []
        raw_map = self.status("look")
        response=raw_map
        # map_processed = '................................\n...............................@\n................................\n.............&..................\n...............&................\n................................\n...................#...........!\n........&....&......#..x........\n.............&....#...#.#.......\n.....#...............#.#...$....\n...##.#..........#.....#........\n....##..........###....#........\n....###................#........\n...#.###.......&.##.............\n......##..............#.!.......\n.......#.........#..............\n......#...............#.........\n..........$$......##.#..........\n.........$$....###..............\n.........$$....#...#............\n....$$.....#######...#..........\n....$.......#######......$...$..\n...........#####...####..$......\n............#.####.##.#.........\n............####..###.#...~~~...\n...............#...###......~~..\n..X.....&.....#.#...##.......~~.\n........&............#......~~..\n..............#!.....####...~.@@\n.@@................####a#~~~..@@\n@@@................#.####~....@@\n.@@...................###~....@.\n'
        map_processed = raw_map.split('\n', 1)[-1]
        map_processed = map_processed.rsplit('\n', 2)[0]
        map_processed = map_processed.splitlines()
        for elem in map_processed:
            map_matrix.append(list(elem))

        map_matrix = np.array(map_matrix)

        return map_matrix,response

    def command_chat(self, command, text_chat=""):
        switcher = {"name": "NAME "+self.player_name+"\n",
                    "join": "JOIN "+self.chat_name+"\n",
                    "join_log": "JOIN "+self.chat_name_log+"\n",
                    "leave": "LEAVE "+self.chat_name+"\n",
                    "post": "POST "+self.chat_name+" "+text_chat+"\n"
                    }
        actual = switcher.get(command, "Invalid Command")

        if(command=="join_log"):
            if("l" in self.flags):
                print(self.chat_name_log)
                self.chat_log = telnetlib.Telnet(self.host, self.chat_port)
                self.chat_log.write(bytes(switcher["name"], "utf-8"))
                self.chat_log.write(bytes(actual, "utf-8"))
        else:
            self.chat.write(bytes(actual, "utf-8"))

        if(command == "leave"):
            print("left chat correctly!")

    def deduction_game(self,command,player,player_nature=""):
        switcher = {"accuse": self.game_name+" ACCUSE "+player+"\n",
                    "judge": self.game_name+" JUDGE "+player+" "+player_nature+"\n"
                    }
        actual = switcher.get(command, "Invalid Command")

        self.wait_last_command(time_mode="default")
        self.connection.write(bytes(actual, "utf-8"))
        
        result = str(self.connection.read_until(
            b"\n").decode("utf-8"))

        self.timestamp_last_command = time.clock()
        return result
