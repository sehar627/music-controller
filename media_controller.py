import mediapipe as mp
import pyautogui
import cv2
import time

capture = cv2.VideoCapture(0)
width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mp_hands.Hands(max_num_hands=1)

play = False
mute_active = False

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            index_x, index_y = int(landmarks[8].x * width), int(landmarks[8].y * height)
            thumb_x, thumb_y = int(landmarks[4].x * width), int(landmarks[4].y * height)
            middle_x, middle_y = int(landmarks[12].x * width), int(landmarks[12].y * height)

            cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), -1)

            # ---- Gestures ----

            # Play: Index + Thumb up, others down
            if (landmarks[8].y < landmarks[6].y and  # Index up
                landmarks[4].y < landmarks[3].y and  # Thumb up
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                if not play:
                    pyautogui.press('playpause')
                    play = True
                    time.sleep(0.3)

            # Pause: full fist
            if (landmarks[4].y > landmarks[3].y and
                landmarks[8].y > landmarks[6].y and
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                if play:
                    pyautogui.press('playpause')
                    play = False
                    time.sleep(0.3)

            # Volume Up: Thumb up only
            if (landmarks[4].y < landmarks[3].y and
                landmarks[8].y > landmarks[6].y and
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                pyautogui.press('volumeup')
                time.sleep(0.3)

            # Volume Down: Thumb down only
            if (landmarks[4].y > landmarks[3].y and
                landmarks[8].y > landmarks[6].y and
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                pyautogui.press('volumedown')
                time.sleep(0.3)

            # Next Track: Index up + move right
            if (landmarks[8].y < landmarks[6].y and
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                if index_x > width - 100:
                    pyautogui.press('nexttrack')
                    time.sleep(0.5)

            # Previous Track: Index up + move left
            if (landmarks[8].y < landmarks[6].y and
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                if index_x < 100:
                    pyautogui.press('prevtrack')
                    time.sleep(0.5)

            # Mute/Unmute: V-sign
            if (landmarks[8].y < landmarks[6].y and
                landmarks[12].y < landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y):
                if not mute_active:
                    pyautogui.press('volumemute')
                    mute_active = True
                    time.sleep(0.3)
            else:
                mute_active = False

    cv2.imshow("AI Music Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
