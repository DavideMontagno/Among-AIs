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
import random

def start_game(cellular_a,starting=False):
    res=cellular_a.play(starting)
    return res

def start_chat(cellular_chat):
    res=cellular_chat.read_chat()
    return res

def start_match(name_game,n_players, raw_mode):
     #PARAMETRI
    flags="W1B"
    list_mode=["007","kamikaze"]

    players_mode=[]
    if raw_mode=="R":
        players_mode=[list_mode[random.randint(0,1)] for elem in range(n_players)]
    else:
        players_mode=(["007"] * raw_mode[0])+(["kamikaze"] * raw_mode[1])
    

    #INIZIALIZZAZIONE THREAD COMMUNICATION
    manager = multiprocessing.Manager()

    #OTHER_PLAYER_GAME_INTERFACE___________________________________________________________________
    threads=[]
    for i in range(n_players):
        pl=GameInterface(name_game,name_game,"Garada"+str(i+1),player_descr="AI9-v1.1",flags=flags)

        print(pl.interact("join"))
        pl.command_chat("name")
        pl.command_chat("join")

        manager_dict = manager.dict()
        
        ca = CellularAutomata(pl, manager_dict,debug=False,mode=players_mode[i]) # to Debug


        ca_chat = CellularAutomata_chat(pl, manager_dict,debug=False)

        
        t = multiprocessing.Process(target=start_game, args=(ca,))
        c = multiprocessing.Process(target=start_chat, args=(ca_chat,))

        threads.append(c)
        threads.append(t)
    #_______________________________________________________________________________

    for n in range(0, len(threads)):
        threads[n].start()

    for n in range(len(threads)):
        threads[n].join()


if __name__ == "__main__":
    while(True):
        name_game=input("\nInserisci il nome della partita e premi invio...")
        n_players=0
        while(True):
            try:
                n_players=input("\nInserisci il numero di giocatori da inserire (max 40)...")
                n_players=int(n_players)
                if(n_players>40):
                    raise Exception()
                else:
                    break
            except:
                input("------->Errore numero massimo consentito 40. Premi invio per ritentare.")
        
        raw_mode=""
        while(True):
            try:
                raw_mode=input(("\nSpecifica la modalità per le {} AI."
                +"\nAttenzione la somma deve coincidere con il numero di AI."
                +"\nInserisci \"R\" per l'inserimento casuale oppure \"numero 007-numero kamikaze\" es. 4-5...").format(n_players))

                # Caso randomico
                if(raw_mode=="R"):
                    break

                #Caso Assegnazione
                raw_mode=raw_mode.split("-")
                check_sum=int(raw_mode[0])+int(raw_mode[1])
                if(check_sum==n_players):
                    raw_mode=[int(raw_mode[0]),int(raw_mode[1])]
                    break
                else:
                    raise Exception()
            except:
                input("------->Errore. Ripeti l'inserimento. Premi invio per ritentare.")
        
        check_ok=input("\nRiepilogo:\n\tNome match: {}\n\tNumero AI player: {}\n\tModalità: {}\nPremi Y per continuare N per cambiare i dati...".format(name_game,n_players,raw_mode))
        if(check_ok=="Y"):
            start_match(name_game,n_players,raw_mode=raw_mode)
