import telnetlib
import time
import numpy as np

time_sleep = 0.51


class Player:
    def __init__(self,  game_name, player_name, player_nature="AI", player_descr="", host="margot.di.unipi.it", port=8421):
        self.host = host
        self.port = port
        self.game_name = game_name
        self.player_nature = player_nature
        self.player_name = player_name
        self.player_descr = player_descr
        self.connection = telnetlib.Telnet(self.host, self.port)

    def interact(self, command, direction=""):

        switcher = {"move": self.game_name+" MOVE "+direction+"\n",
                    "shoot": self.game_name+" SHOOT "+direction+"\n",
                    "join": self.game_name+" JOIN "+self.player_name+" "+self.player_nature+" - "+self.player_descr+"\n"}

        actual = switcher.get(command, "Invalid Command")

        time.sleep(time_sleep)
        self.connection.write(bytes(actual, "utf-8"))
        result = str(self.connection.read_until(
            b"\n", time_sleep).decode("utf-8"))

        return actual+" "+result

    def status(self, command):
        switcher = {"look": self.game_name+" LOOK\n",
                    "status": self.game_name+" STATUS\n"}

        actual = switcher.get(command, "Invalid Command")
        time.sleep(time_sleep)
        self.connection.write(bytes(actual, "utf-8"))
        result = str(self.connection.read_until(
            b"\xc2\xbb\n", time_sleep).decode("utf-8"))

        return result

    def manage_game(self, command):

        switcher = {"new": "NEW "+self.game_name+"\n",
                    "start": self.game_name+" START\n"}

        actual = switcher.get(command, "Invalid Command")
        time.sleep(time_sleep)
        self.connection.write(bytes(actual, "utf-8"))
        result = str(self.connection.read_until(
            b"\n", time_sleep).decode("utf-8"))
        return result

    def process_map(self):
        map_matrix = []
        raw_map = self.status("look")
        # map_processed = '................................\n...............................@\n................................\n.............&..................\n...............&................\n................................\n...................#...........!\n........&....&......#..x........\n.............&....#...#.#.......\n.....#...............#.#...$....\n...##.#..........#.....#........\n....##..........###....#........\n....###................#........\n...#.###.......&.##.............\n......##..............#.!.......\n.......#.........#..............\n......#...............#.........\n..........$$......##.#..........\n.........$$....###..............\n.........$$....#...#............\n....$$.....#######...#..........\n....$.......#######......$...$..\n...........#####...####..$......\n............#.####.##.#.........\n............####..###.#...~~~...\n...............#...###......~~..\n..X.....&.....#.#...##.......~~.\n........&............#......~~..\n..............#!.....####...~.@@\n.@@................####a#~~~..@@\n@@@................#.####~....@@\n.@@...................###~....@.\n'
        map_processed = raw_map.split('\n', 1)[-1]
        map_processed = map_processed.rsplit('\n', 2)[0]
        map_processed = map_processed.splitlines()
        for elem in map_processed:
            map_matrix.append(list(elem))

        map_matrix = np.array(map_matrix)

        return map_matrix
