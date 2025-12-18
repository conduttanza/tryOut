#code by conduttanza
#
#created the 17/12/2025

import math, numpy as np

class Config:
    #universal values
    #constants
    G = 6.67*10**-11
    R = 8.31
    Eta = 8.854*10**-12
    
    #config values
    fps = 60
    side = 600

class Logic:
    def outPut(self, input):
        output = np.array((
            [input, input]
        ))
        print('im doing something')
        return output