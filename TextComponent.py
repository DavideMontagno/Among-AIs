#!/usr/bin/env python
# https://github.com/spro/char-rnn.pytorch

import torch
import os
import argparse

from helpers import *
from model import *

def generate(decoder, prime_str='A', predict_len=100, temperature=0.8, cuda=False):
    try:
        hidden = decoder.init_hidden(1)
        prime_input = Variable(char_tensor(prime_str).unsqueeze(0))

        if cuda:
            hidden = hidden.cuda()
            prime_input = prime_input.cuda()
        predicted = prime_str
        to_return=""
        # Use priming string to "build up" hidden state
        for p in range(len(prime_str) - 1):
            _, hidden = decoder(prime_input[:,p], hidden)
            
        inp = prime_input[:,-1]
        
        for p in range(predict_len):
            output, hidden = decoder(inp, hidden)
            
            # Sample from the network as a multinomial distribution
            output_dist = output.data.view(-1).div(temperature).exp()
            top_i = torch.multinomial(output_dist, 1)[0]

            # Add predicted character to string and use as next input
            predicted_char = all_characters[top_i]
            if(predicted_char!="-"):
                predicted += predicted_char
                to_return+=predicted_char
                if(predicted_char=="." or predicted_char=="!" or predicted_char=="?" ):
                    return to_return
                inp = Variable(char_tensor(predicted_char).unsqueeze(0))
                if cuda:
                    inp = inp.cuda()
            else:
                p=p-1

        return to_return
    except:
        return ""

