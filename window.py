#code by conduttanza
#
#created the 17/12/2025

#universal imports
import pygame, numpy as np, cv2

#self made imports
import window_logic, inputs, imagRec_logic

config = window_logic.Config()
code = window_logic.Logic()
fps = config.fps
side_x = config.side_x
side_y = config.side_y
image = inputs.Image()
recognition = imagRec_logic



center = np.array((
    [side_x/2, side_y/2]
))

pygame.init()
pygame.display.set_caption('project x')
screen = pygame.display.set_mode((side_x, side_y), pygame.RESIZABLE)
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
        
        #webcam stream
        image.show_stream(screen)
        frame = image.get_frame()
        if frame is not None:
            recognition.process_frame(frame)
        #future drawings here
        
        #point = Point(1)
        #pygame.draw.circle(
            #screen,(255,255,255), point+center, 10)
        
        clock.tick(fps)
        pygame.display.flip()
        if running == False:
            print('\n'+'pygame quit successfully')

except KeyboardInterrupt:
    pygame.quit()
    print('\n'+'kb quit successful')
    running = False