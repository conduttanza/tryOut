#code by conduttanza
#
#created the 17/12/2025

#universal imports
import pygame, numpy as np

#self made imports
import logic, inputs, imagRec_logic

config = logic.Config()
code = logic.Logic()
fps = config.fps
side = config.side

side_x = side
side_y = side
center = np.array((
    [side_x/2, side_y/2]
))

pygame.init()
pygame.display.set_caption('project x')
screen = pygame.display.set_mode((side_x, side_y))
clock = pygame.time.Clock()

def Point(input):
    coords = code.outPut(input)
    return coords
    
running = True

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print('quitting...')
            
        screen.fill((0,0,0))
        point = Point(1)
        pygame.draw.circle(
            screen,(255,255,255), point+center, 5)
        clock.tick(fps)
        
        if running == False:
            print('\n'+'pygame quit successfully')

except KeyboardInterrupt:
    pygame.quit()
    print('\n'+'kb quit successful')
    running = False