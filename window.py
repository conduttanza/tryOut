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
pygame.display.set_caption('hand simulation')
screen = pygame.display.set_mode((side_x, side_y), pygame.RESIZABLE)
clock = pygame.time.Clock()

def Point(input):
    coords = code.outPut(input)
    return coords

running = True
I_finger = None
Thumb = None
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print('quitting...')
            
        screen.fill((0,0,0))
        '''
        #webcam stream
        image.show_stream(screen)
        frame = image.get_frame()
        if frame is not None:
            recognition.process_frame(frame)
        '''
        #hand recon
        
        recognition.handRecognition()
        
        if I_finger is not None and Thumb is not None:
            ix = int(I_finger.x * side_x)
            iy = int(I_finger.y * side_y)

            tx = int(Thumb.x * side_x)
            ty = int(Thumb.y * side_y)
            #future drawings here
            pygame.draw.line(screen, (0,255,0), (ix, iy), (tx, ty), 3)
        
        clock.tick(fps)
        pygame.display.flip()
        if running == False:
            print('\n'+'pygame quit successfully')

except KeyboardInterrupt:
    pygame.quit()
    print('\n'+'kb quit successful')
    running = False