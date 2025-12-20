#code by conduttanza
#
#created the 17/12/2025

#simple torch based change detection for image recognition
import torch
import time
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



def handRecognition():
    #time.sleep(Config.delay) 
    I_finger = None
    Thumb = None
    
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
            '''
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = True
            
            '''
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
