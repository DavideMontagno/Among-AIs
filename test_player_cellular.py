from player import Player
from CellularAutomata import CellularAutomata
import time
import datetime
import threading
import os
import imageio

count=0
png_gif = "./gif/"
tot=10
for i in range(0,10):
    try:
        #CREATION
        NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        png_dir = str(NAME_GAME)

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

        pl5=Player(NAME_GAME,"pl5")
        print(pl5.interact("join"))

        pl6=Player(NAME_GAME,"pl6")
        print(pl6.interact("join"))

        pl7=Player(NAME_GAME,"pl7")
        print(pl7.interact("join"))

        pl8=Player(NAME_GAME,"pl8")
        print(pl8.interact("join"))

        pl9=Player(NAME_GAME,"pl9")
        print(pl9.interact("join"))

        pl10=Player(NAME_GAME,"pl10")
        print(pl10.interact("join"))

        pl11=Player(NAME_GAME,"pl11")
        print(pl11.interact("join"))

        pl12=Player(NAME_GAME,"pl12")
        print(pl12.interact("join"))

        pl13=Player(NAME_GAME,"pl13")
        print(pl13.interact("join"))

        pl14=Player(NAME_GAME,"pl14")
        print(pl14.interact("join"))

        pl15=Player(NAME_GAME,"pl15")
        print(pl15.interact("join"))

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
        name=""
        if(result==True):
            count = count+1
            name="work_"
        else:
            name="error"
        images = []
        for file_name in os.listdir(png_dir):
            if file_name.endswith('.png'):
                file_path = os.path.join(png_dir, file_name)
                images.append(imageio.imread(file_path))
                os.remove(file_path)
        imageio.mimsave(png_gif+name+NAME_GAME+"_"+str(count)+".gif", images)
        os.rmdir(png_dir)
        print("finished")
    except Exception as e:
        print(e)
        continue
print("Executed correctly: "+str(count)+" on "+str(tot))
print("Finito.")






