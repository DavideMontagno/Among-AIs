import sys
import os

import datetime
import matplotlib.pyplot as plt
import time


class CellularAutomata_chat():
    def __init__(self,  player, manager_dict,debug=False): 
        self.player = player
        self.debug = debug
        self.impostors={}
        self.allies=[]
        
        self.manager_dict=manager_dict


    def process_message(self,text):

        if("hit" in text):
            if(self.allies==[]):
                self.allies=self.manager_dict["allies"]
                self.impostors={k:0 for k in self.allies}

            message=text.split()
            if(message[2] in self.allies):
                self.impostors[message[2]]+=1
                self.manager_dict["impostors"]=self.impostors

    def read_chat(self):
        end=False
        chat = []
        while(True):
            result = str(self.player.chat.read_until(
            b"\n").decode("utf-8"))
            chat.append(result)

            self.process_message(result)

            if(self.debug): print(result)
            if(result.lower().find("finished!")!=-1): break
                
        while(True):
                    line = str(self.player.chat.read_until(
            b"\n").decode("utf-8"))
                    chat.append(line)
                    if(self.debug): print(line)
            #print(line)
