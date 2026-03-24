import cv2
import mediapipe as mp
import pyttsx3
import time

# Text to Speech setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_spoken = ""
last_time = 0

def speak(text):
    global last_spoken, last_time
    if text != last_spoken or time.time() - last_time > 3:
        engine.say(text)
        engine.runAndWait()
        last_spoken = text
        last_time = time.time()

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    text = ""

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(handLms)

            if fingers == 1:
                text = "Rakuu bhai ki taraf se Ram Ram"
            elif fingers == 2:
                text = "Hello "
            elif fingers == 3:
                text = "Love You"
            else:
                text = ""

            if text != "":
                speak(text)

    # Display text
    cv2.putText(img, text, (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 3)

    cv2.imshow("Hand Gesture AI", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()