#code by conduttanza
#
#created the 17/12/2025

import math, numpy as np

class Config:
    #universal values
    stream_url = None
    threshold_value = 0.01   # threshold for change detection
    #config values
    fps = 30
    delay = 1 / (5*fps)   # camera read delay to reduce CPU usage
    side_x = 640
    side_y = 480

class Logic:
    def outPut(self, input):
        output = np.array((
            [input, input]
        ))
        #print('im doing something')
        return output