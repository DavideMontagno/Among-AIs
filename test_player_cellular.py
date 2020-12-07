from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing
from Tournament import Tournament

count=0
png_gif_dir = "./gif/"
tot=1


def start_game(cellular_a):
    cellular_a.play()
def start_chat(cellular_chat):
    cellular_chat.read_chat()
    pass

if __name__ == "__main__":
    n_player = 3
    flags="Q1B"
    participate_tournament = False
    debug=False
    creation_game=True
    NAME_GAME = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    tournament = "SmartCUP"
    manager_game = ""
    threads_player = []
    threads_chat = []
    
    png_dir = str(NAME_GAME)
    created=False

    if(participate_tournament):
        for i in range(0,n_player):
            Tournament(name="ai9_pl"+str(i+1), tournament=tournament)
        input('Completed registring all players in tournament: '+str(tournament))

    for i in range(0,n_player):
        temp = GameInterface(NAME_GAME,NAME_GAME,"ai9_pl"+str(i+1),player_descr="v0.1",flags=flags)

        if(creation_game):
            result = temp.manage_game("new").lower()
            print(result)

            if(result.find("error")!=-1):
                print("ERRORE CREAZIONE")
                exit()
            else: 
                creation_game=False
                created=True
                manager_game = temp

        print(temp.interact("join"))
        temp.command_chat("name")
        temp.command_chat("join")

        manager = multiprocessing.Manager()
        manager_dict = manager.dict()
        ca = CellularAutomata(temp, manager_dict,debug=debug) # to Debug
        ca_chat = CellularAutomata_chat(temp, manager_dict,debug=False)

        t_player = multiprocessing.Process(target=start_game, args=(ca,))
        chat_player = multiprocessing.Process(target=start_chat, args=(ca_chat,))

        threads_player.append(t_player)
        threads_chat.append(chat_player)

    input("Prest enter to start")
    
    for n in range(len(threads_chat)):
        threads_chat[n].start()

    for n in range(len(threads_player)):
        threads_player[n].start()

    

    if(created):
        manager_game.manage_game("start")
        print("Game started...")

    
    for n in range(len(threads_player)):
        threads_player[n].join()
    for n in range(len(threads_chat)):
        threads_chat[n].join()
    
