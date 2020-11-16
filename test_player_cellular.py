from player import Player
from CellularAutomata import CellularAutomata
import time
import datetime
import threading
import os
import imageio

count=0
for i in range(0,1):
    try:
        #CREATION
        NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        pl1=Player(NAME_GAME,"pl1")
        print(pl1.manage_game("new"))

        #JOIN GAME
        print(pl1.interact("join"))

        pl2=Player(NAME_GAME,"pl2")
        print(pl2.interact("join"))

        pl3=Player(NAME_GAME,"pl3")
        print(pl3.interact("join"))

        pl4=Player(NAME_GAME,"pl4")
        print(pl4.interact("join"))

        # START GAME
        if(pl1.manage_game("start")=="ERROR 501 Need two non-empty teams to start"):
            print("ERRORE CREAZIONE")
            exit()


        print(pl1.status("status"))

        #print(pl1.status("look"))


        ca=CellularAutomata(pl1)
        result = ca.play()
        '''t1 = threading.Thread(target=ca.play(), args=[])
        ca2=CellularAutomata(pl2)
        t2 = threading.Thread(target=ca2.play(), args=[])
        ca3=CellularAutomata(pl3)
        t3 = threading.Thread(target=ca3.play(), args=[])
        ca3=CellularAutomata(pl4)
        t4 = threading.Thread(target=ca4.play(), args=[])
        list_ca = [ca,ca2,ca3,ca4]
        threads = []
        for n in range(len(list_ca)):
           start_new_thread(list_ca[n].play(), [])

        # Wait all threads to finish.
        for t in threads:
            t.join()'''

        if(result==True):
            count = count+1
            png_dir = str(NAME_GAME)
            png_gif = "./gif/"
            images = []
            for file_name in os.listdir(png_dir):
                if file_name.endswith('.png'):
                    file_path = os.path.join(png_dir, file_name)
                    images.append(imageio.imread(file_path))
                    os.remove(file_path)
            imageio.mimsave(png_gif+NAME_GAME+"_"+str(count)+".gif", images)
            os.rmdir(png_dir)
            print("finished")
    except Exception as e:
        print(e)
        continue
print("Executed correctly: "+str(count))
print("Finito.")






