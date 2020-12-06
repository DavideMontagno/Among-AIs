from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomataSUPER import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing

count=0
png_gif_dir = "./gif/"
tot=1
debug = False


def start_game(cellular_a):
    cellular_a.play()

def start_chat(cellular_chat):
    cellular_chat.read_chat()

if __name__ == "__main__":

    
    n_players=5
    flags="TQ1B"
    
    #CREATION
    NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(NAME_GAME)
    png_dir = str(NAME_GAME)

    pl0=GameInterface(NAME_GAME,NAME_GAME,"ai9_pl0",player_descr="v0.1",flags=flags)
    print(pl0.manage_game("new"))

    #JOIN GAME
    print(pl0.interact("join"))
    pl0.command_chat("name")
    pl0.command_chat("join")

    #OTHER_PLAYER___________________________________________________________________
    other_pl_list=[]
    for i in range(n_players):
        pl=GameInterface(NAME_GAME,NAME_GAME,"ai9_pl"+str(i+1),player_descr="v0.1",flags=flags)
        print(pl.interact("join"))
        pl.command_chat("name")
        pl.command_chat("join")
        other_pl_list.append(pl)
    #_______________________________________________________________________________


    manager = multiprocessing.Manager()

    manager_dict = manager.dict()
    ca0 = CellularAutomata(pl0, manager_dict,debug=False,mode="007") # to Debug
    ca_chat0 = CellularAutomata_chat(pl0, manager_dict,debug=False)

    t0 = multiprocessing.Process(target=start_game, args=(ca0,))
    c0 = multiprocessing.Process(target=start_chat, args=(ca_chat0,))

    threads=[t0,c0]

    #OTHER_PLAYER___________________________________________________________________
    ca_list=[]
    ca_chat_list=[]
    for i, pl in enumerate(other_pl_list):

        manager_dict = manager.dict()

        if(i%2==1):
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="007") # to Debug
        else:
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="kamikaze") # to Debug
        
        ca_chat = CellularAutomata_chat(pl, manager_dict,debug=False)

        ca_list.append(ca)
        ca_chat_list.append(ca_chat)


    for i in range(n_players):
        t = multiprocessing.Process(target=start_game, args=(ca_list[i],))
        c = multiprocessing.Process(target=start_chat, args=(ca_chat_list[i],))
        threads.append(c)
        threads.append(t)
    #_______________________________________________________________________________

    for n in range(len(threads)):
        threads[n].start()

    if(pl0.manage_game("start").lower().find("error")!=-1):
        print("ERRORE CREAZIONE")
        exit()
    else: print("Started")

    for n in range(len(threads)):
        threads[n].join()
