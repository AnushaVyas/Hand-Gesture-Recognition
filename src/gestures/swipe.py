import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque
import pyautogui

pyautogui.FAILSAFE = False

WINDOW_NAME = "Smooth Swipe Gesture Control"
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

HISTORY = deque(maxlen=14)        # tracks fingertip positions
DIR_HISTORY = deque(maxlen=14)    # stores direction classification
COOLDOWN = 0.45                    # seconds
last_action = 0

# gesture thresholds
MIN_DIST = 0.11       # normalized distance traveled
MIN_VELOCITY = 0.011  # normalized speed
DIR_REQUIRED = 0.78   # directional confidence (78% frames must agree)


def detect_direction():
    """Returns dominant direction or None"""

    if len(HISTORY) < HISTORY.maxlen:
        return None

    dx = HISTORY[-1][0] - HISTORY[0][0]
    dy = HISTORY[-1][1] - HISTORY[0][1]

    dist = np.linalg.norm([dx, dy])
    velocity = dist / HISTORY.maxlen

    if velocity < MIN_VELOCITY or dist < MIN_DIST:
        return None

    # classify frame-wise direction
    DIR_HISTORY.clear()
    for i in range(1, len(HISTORY)):
        x1, y1 = HISTORY[i - 1]
        x2, y2 = HISTORY[i]
        dx_f, dy_f = x2 - x1, y2 - y1

        if abs(dx_f) > abs(dy_f):
            DIR_HISTORY.append("right" if dx_f > 0 else "left")
        else:
            DIR_HISTORY.append("down" if dy_f > 0 else "up")

    # find dominant direction percentage
    for d in ["right", "left", "up", "down"]:
        if DIR_HISTORY.count(d) / len(DIR_HISTORY) >= DIR_REQUIRED:
            return d

    return None


def execute(direction):
    if direction == "right":
        pyautogui.hotkey("ctrl", "pgdn")
    elif direction == "left":
        pyautogui.hotkey("ctrl", "pgup")
    elif direction == "up":
        pyautogui.scroll(1100)
    elif direction == "down":
        pyautogui.scroll(-1100)


def run():
    global last_action

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ ERROR: Camera not available")
        return

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.78,
        min_tracking_confidence=0.78
    ) as hands:

        print("\n✅ Smooth Swipe Control Activated")
        print("👉 Swipe Right = Next Tab")
        print("👉 Swipe Left = Previous Tab")
        print("👉 Swipe Up = Scroll Up")
        print("👉 Swipe Down = Scroll Down")
        print("❌ Press Q to Quit\n")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture_display = ""

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                # index fingertip landmark — most stable for gestures
                x = hand.landmark[8].x
                y = hand.landmark[8].y

                HISTORY.append((x, y))

                direction = detect_direction()
                now = time.time()

                if direction and now - last_action > COOLDOWN:
                    execute(direction)
                    gesture_display = direction.upper()
                    last_action = now

            if gesture_display:
                cv2.putText(
                    frame, gesture_display,
                    (40, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.3, (0, 255, 0), 6
                )

            cv2.imshow(WINDOW_NAME, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
