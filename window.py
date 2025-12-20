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
image = inputs
recognition = imagRec_logic
recognizer = recognition.Hands_Reckon()


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

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print('quitting...')
            
        screen.fill((0,0,0))
        
        #webcam stream
        #image.Image.show_stream(screen)
        #frame = image.Image.get_frame()
        #if frame is not None:
            #recognition.process_frame(frame)
        
        #hand recon
        
        recognizer.show_recon()
        landmarks = recognizer.returnLandmarks()
        if landmarks:
            
            Thumb = landmarks.landmark[4]
            #print(Thumb)
            tx = config.side_x - int(Thumb.x * config.side_x)
            ty = int(Thumb.y * config.side_y)
            
            I_finger = landmarks.landmark[8]
            #print(Thumb)
            ix = config.side_x - int(I_finger.x * config.side_x)
            iy = int(I_finger.y * config.side_y)
            
            pygame.draw.circle(screen,(0,255,0),(tx, ty), 10)
            pygame.draw.circle(screen,(0,255,0),(ix, iy), 10)
            pygame.draw.line(screen,(0,255,0),(ix,iy),(tx, ty), 3)
        clock.tick(fps)
        pygame.display.flip()
        if running == False:
            print('\n'+'pygame quit successfully')

except KeyboardInterrupt:
    pygame.quit()
    print('\n'+'kb quit successful')
    running = False