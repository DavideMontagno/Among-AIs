from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing

png_gif_dir = "./gif/"
tot=1
debug = False


def start_game(cellular_a,starting=False):
    res=cellular_a.play(starting)
    return res

def start_chat(cellular_chat):
    res=cellular_chat.read_chat()
    return res

if __name__ == "__main__":


    #PARAMETRI
    NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    n_players=5
    flags="Q1B"
    
    print(NAME_GAME)

    #INIZIALIZZAZIONE THREAD COMMUNICATION
    manager = multiprocessing.Manager()

    #OTHER_PLAYER_GAME_INTERFACE___________________________________________________________________
    threads=[]
    for i in range(n_players):
        pl=GameInterface(NAME_GAME,NAME_GAME,"ai9_pl"+str(i+1),player_descr="v0.1",flags=flags)

        if(i==0):#Creatore del gioco
            pl.manage_game("new")

        print(pl.interact("join"))
        pl.command_chat("name")
        pl.command_chat("join")

        manager_dict = manager.dict()

        if(i%2==1):
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="007") # to Debug
        else:
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="kamikaze") # to Debug
        
        ca_chat = CellularAutomata_chat(pl, manager_dict,debug=False)

        if(i==0):# Creatore del gioco
            ca_chat = CellularAutomata_chat(pl, manager_dict,debug=True)
            t = multiprocessing.Process(target=start_game, args=(ca,True))
        else:  
            t = multiprocessing.Process(target=start_game, args=(ca,))
        c = multiprocessing.Process(target=start_chat, args=(ca_chat,))
        threads.append(c)
        threads.append(t)
    #_______________________________________________________________________________

    for n in range(0, len(threads)):
        threads[n].start()

    for n in range(len(threads)):
        threads[n].join()
