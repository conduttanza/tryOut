#code by conduttanza
#
#created the 17/12/2025

#simple torch based change detection for image recognition
import torch
import time
from threading import Thread, Lock
#hand recognition imports
#
#using the mediapipe library 
#
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
    

#self made imports
from window_logic import Config
from inputs import Image
image = Image()
# Module-level state for change detection

class Hands_Reckon:
    
    def __init__(self):
        #time.sleep(Config.delay)
        self.stream_url = Config.stream_url
        self.cap = cv2.VideoCapture(self.stream_url or 0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot use camera")
        self.hand_landmarks = None
        self.ret = False
        self.frame = None
        self.running = True
        self.lock = Lock
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        with mp_hands.Hands(
            model_complexity = 0, 
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5) as hands:
            while self.cap.isOpened() and self.running:
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(Config.delay)
                    print('Empty frame', '\n', 'skipping...')
                    continue
                frame.flags.writeable = False #improved performance
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                results = hands.process(frame)
                if results.multi_hand_landmarks:
                    #print('existent results')
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    self.hand_landmarks = hand_landmarks
                    
                self.ret = True
                self.frame = frame.copy()
                #print('line 64 done')
                #time.sleep(Config.delay)
                #print('imshow done')
    
    def show_recon(self):
        if not self.ret:
            return
        frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('tracker', cv2.flip(frame_rgb, 1))
        
    def returnLandmarks(self):
        #print('sending landmarks')
        return self.hand_landmarks if self.ret else None
    
    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
'''

    
def handRecognition():
    #time.sleep(Config.delay) 
    
    cap = cv2.VideoCapture(Config.stream_url or 0)
    with mp_hands.Hands(
        model_complexity = 0, 
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print('Empty frame, ', '\n', 'Ignoring...')
                continue
            
            # To de-improve performance, optionally mark the image as writeable to
            # pass by reference.
            # 
            
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = True
            
            
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = hands.process(frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    hand_landmarks.landmark[8] 
                    hand_landmarks.landmark[4]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('MediaPipe Hands', cv2.flip(rgb_frame, 1))
            #process_frame(rgb_frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()


'''


old_frame = None
   
def process_frame(frame):
    """Process a single frame for change detection.

    Call this from your main loop and pass the latest frame. This avoids
    instantiating Image() repeatedly (which opens the camera multiple times).
    """
    global old_frame
    if frame is None:
        return

    if old_frame is None:
        old_frame = frame.copy()
        return

    frame_tensor = torch.from_numpy(frame).permute(2, 0, 1).float() / 255.0
    old_frame_tensor = torch.from_numpy(old_frame).permute(2, 0, 1).float() / 255.0
    diff = torch.abs(frame_tensor - old_frame_tensor)
    if diff.mean().item() > Config.threshold_value:
        print("Significant change detected in the frame.")
    else:
        print("No significant change.")
    old_frame = frame.copy()
