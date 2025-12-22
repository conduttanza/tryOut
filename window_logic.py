#code by conduttanza
#
#created the 17/12/2025

import math, numpy as np
from threading import Thread, Lock
class Config:
    
    #universal values
    stream_url = None
    threshold_value = 0.01   # threshold for change detection
    #config values
    fps = 30
    delay = 1 / (5*fps)   # camera read delay to reduce CPU usage
    side_x = 640
    side_y = 400
    size_tolerance = 10
    
    def __init__(self):
        self.side_x = 640
        self.side_y = 400
        Thread(target=self.scaling, daemon=True).start()
        
    def scaling(self, scale):
        if self.side_x and self.side_y and scale:
            return self.side_x * scale, self.side_y * scale
        else:
            return self.side_x, self.side_y
        

class Logic:
    def outPut(self, input):
        output = np.array((
            [input, input]
        ))
        #print('im doing something')
        return output