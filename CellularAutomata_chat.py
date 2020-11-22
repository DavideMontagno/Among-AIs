import sys
import os

import datetime
import matplotlib.pyplot as plt
import time





class CellularAutomata_chat():
    def __init__(self,  player):
        self.player = player
        
    def read_chat(self):
                    end=False
                    while(True):
                        result = str(self.player.chat.read_until(
                        b"\n").decode("utf-8"))
                        #print("Ricevuto: "+result)
                        if(result.lower().find("finished!")!=-1): 
                            while(True):
                                line = str(self.player.chat.read_until(
                        b"\n").decode("utf-8"))
                                
                        #print(line)
                    
                    
                    
    
                   