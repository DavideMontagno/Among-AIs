import sys
import os

import datetime
import matplotlib.pyplot as plt





class CellularAutomata_chat():
    def __init__(self,  player):
        self.player = player
    def read_chat(self):
                    while(self.player.finished==False):
                        result = str(self.player.chat.read_until(
                        b"\n").decode("utf-8"))
                        print("Ricevuto: "+result)
                    self.player.command_chat("leave")
                    