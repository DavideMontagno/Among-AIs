from player import Player
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing


def read_chat(cellular_a):
    cellular_a.read_chat()

if __name__ == "__main__":
    
    NAME = "ai9_test"#+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    pl1=Player(NAME,"ai9_pl17")
    pl1=Player(NAME,"ai9_pl1")
    pl1.command_chat("name")
    pl1.command_chat("join")
    
    ca=CellularAutomata_chat(pl1)
    t1 = multiprocessing.Process(target=read_chat, args=(ca,))
    t1.start()
    for i in range(0,10):
        pl1.command_chat("post",text_chat="prova"+str(i))
    
    '''ca=CellularAutomata(pl1)
    t1 = multiprocessing.Process(target=start_game, args=(ca,))
    

    threads = [t1]
    for n in range(len(threads)):
        threads[n].start()
    
    # Wait all threads to finish.
    for n in range(len(threads)):
        threads[n].join()
    print("finished")'''