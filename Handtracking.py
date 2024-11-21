import mediapipe as mp
import cv2
import numpy
import skimage.feature
from mediapipe.framework.formats import landmark_pb2
import time
import pyautogui
import win32api

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('http://192.168.1.3:8080/video')

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.2) as hands:
    while cap.isOpened():
        _, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image,1)

        image_height,image_width,_ = image.shape

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num,hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 250), thickness=1, circle_radius=2))


        if results.multi_hand_landmarks !=None:
            for handsLandmarks in results.multi_hand_landmarks:
                for points in mp_hands.HandLandmark:
                    normalizedLandmark = handsLandmarks.landmark[points]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, image_width, image_height)

                    points = str(points)

                    if points == 'HandLandmark.INDEX_FINGER_TIP':
                        try:
                            cv2.circle(image, (pixelCoordinatesLandmark[0], pixelCoordinatesLandmark[1]),15,(0,100,0),5)
                            indexfingertip_x = pixelCoordinatesLandmark[0]
                            indexfingertip_y = pixelCoordinatesLandmark[1]
                            win32api.SetCursorPos((indexfingertip_x*2, indexfingertip_y*2))
                            pyautogui.keyDown('w')
                        except:
                            pyautogui.keyDown('r')
                            pass
        cv2.imshow('game', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
