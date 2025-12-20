#code by conduttanza
#
#created the 17/12/2025
import cv2, pygame, time
from threading import Thread, Lock
from window_logic import Config




class Image:
    
    def __init__(self):
        self.stream_url = Config.stream_url
        self.cap = cv2.VideoCapture(self.stream_url or 0, cv2.CAP_DSHOW)  # 0 = default camera
        if not self.cap.isOpened():
            raise RuntimeError("Cannot use camera")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.side_x)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.side_y)
        self.ret = False
        self.frame = None
        self.running = True
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        self.lock = Lock()
        try:
            while self.running:
                ret, frame = self.cap.read()
                #time.sleep(Config.delay)    # to reduce CPU usage
                if ret:
                    with self.lock:
                        self.ret = ret
                        self.frame = frame
        except (Exception or KeyboardInterrupt) as e:
            print(f"Error in camera thread: {e}")
            print("Stopping camera thread.")

    def show_stream(self, surface):
        if self.ret:
            with self.lock:
                #print(self.frame)
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_rgb = cv2.resize(frame_rgb, (surface.get_width(), surface.get_height()))
                surf = pygame.surfarray.make_surface(frame_rgb.swapaxes(0,1))
                surface.blit(surf, (0, 0))
    
    def get_frame(self):
        return self.frame.copy() if self.ret else None
    
    def stop(self):
        self.running = False
        self.cap.release()

