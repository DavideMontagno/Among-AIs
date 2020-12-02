import sys
import os

import datetime
import time


class CellularAutomata_chat():
    def __init__(self,  player,debug=False):
        self.player = player
        self.debug = debug

    
    def read_chat(self):
        end=False
        chat = []
        while(True):
            result = str(self.player.chat.read_until(
            b"\n").decode("utf-8"))
            chat.append(result)
            if(self.debug): print(result)
            if(result.lower().find("finished!")!=-1): break
                
        while(True):
                    line = str(self.player.chat.read_until(
            b"\n").decode("utf-8"))
                    chat.append(line)
                    if(self.debug): print(line)
            #print(line)
