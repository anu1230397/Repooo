import cv2
import mediapipe as mp
import numpy as np
import math
import time


# -------------------- MediaPipe Setup --------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# -------------------- Utility Functions --------------------

def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def angle(a, b, c):
    """
    Calculates angle ABC.
    """
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])

    cosine = np.dot(ba, bc) / (
        np.linalg.norm(ba) *
        np.linalg.norm(bc) + 1e-8
    )

    cosine = np.clip(cosine, -1, 1)

    return math.degrees(math.acos(cosine))


def finger_extended(lm, tip, pip, mcp):
    """
    Determines whether a finger is extended
    using joint angles.
    """
    a = angle(lm[mcp], lm[pip], lm[tip])
    return a > 155


# -------------------- Gesture Recognition --------------------

def recognize_gesture(lm):

    # Finger states
    thumb = finger_extended(lm, 4, 3, 2)
    index = finger_extended(lm, 8, 6, 5)
    middle = finger_extended(lm, 12, 10, 9)
    ring = finger_extended(lm, 16, 14, 13)
    pinky = finger_extended(lm, 20, 18, 17)

    fingers = [thumb, index, middle, ring, pinky]

    # Count extended fingers
    count = sum(fingers)

    # --------------------------------------------------
    # THUMBS UP / DOWN
    # --------------------------------------------------

    if thumb and not index and not middle and not ring and not pinky:

        wrist = lm[0]
        thumb_tip = lm[4]

        if thumb_tip.y < wrist.y:
            return "THUMBS UP"

        if thumb_tip.y > wrist.y:
            return "THUMBS DOWN"

    # --------------------------------------------------
    # OPEN PALM
    # --------------------------------------------------

    if count == 5:
        return "OPEN PALM"

    # --------------------------------------------------
    # FIST
    # --------------------------------------------------

    if count == 0:
        return "FIST"

    # --------------------------------------------------
    # PEACE
    # --------------------------------------------------

    if index and middle and not ring and not pinky:
        return "PEACE"

    # --------------------------------------------------
    # THREE
    # --------------------------------------------------

    if index and middle and ring and not pinky:
        return "THREE"

    # --------------------------------------------------
    # FOUR
    # --------------------------------------------------

    if index and middle and ring and pinky and not thumb:
        return "FOUR"

    # --------------------------------------------------
    # POINTING
    # --------------------------------------------------

    if index and not middle and not ring and not pinky:
        return "POINTING"

    # --------------------------------------------------
    # ROCK / HORNS
    # --------------------------------------------------

    if index and pinky and not middle and not ring:
        return "ROCK"

    # --------------------------------------------------
    # CALL ME
    # --------------------------------------------------

    if thumb and pinky and not index and not middle and not ring:
        return "CALL ME"

    # --------------------------------------------------
    # OK GESTURE
    # --------------------------------------------------

    thumb_index_distance = distance(lm[4], lm[8])

    palm_size = distance(lm[0], lm[9])

    normalized_distance = thumb_index_distance / (
        palm_size + 1e-8
    )

    if normalized_distance < 0.35 and middle and ring and pinky:
        return "OK"

    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------

    return "UNKNOWN"


# -------------------- Gesture Smoothing --------------------

gesture_history = []
MAX_HISTORY = 7


def smooth_gesture(gesture):

    gesture_history.append(gesture)

    if len(gesture_history) > MAX_HISTORY:
        gesture_history.pop(0)

    # Majority voting
    values, counts = np.unique(
        gesture_history,
        return_counts=True
    )

    return values[np.argmax(counts)]


# -------------------- FPS Counter --------------------

previous_time = 0


def calculate_fps():

    global previous_time

    current_time = time.time()

    fps = 1 / (current_time - previous_time + 1e-8)

    previous_time = current_time

    return int(fps)


# -------------------- Camera --------------------

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while cap.isOpened():

    success, frame = cap.read()

    if not success:
        print("Camera error!")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # MediaPipe processing
    results = hands.process(rgb)

    detected_gestures = []

    if results.multi_hand_landmarks:

        for hand_index, hand_landmarks in enumerate(
            results.multi_hand_landmarks
        ):

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            # Recognize gesture
            gesture = recognize_gesture(lm)

            # Smooth prediction
            gesture = smooth_gesture(gesture)

            detected_gestures.append(gesture)

            # Bounding box
            h, w, _ = frame.shape

            x_coordinates = [
                int(point.x * w)
                for point in lm
            ]

            y_coordinates = [
                int(point.y * h)
                for point in lm
            ]

            x_min = min(x_coordinates)
            y_min = min(y_coordinates)

            x_max = max(x_coordinates)
            y_max = max(y_coordinates)

            # Add padding
            x_min = max(0, x_min - 20)
            y_min = max(0, y_min - 60)
            x_max = min(w, x_max + 20)
            y_max = min(h, y_max + 20)

            # Bounding box
            cv2.rectangle(
                frame,
                (x_min, y_min),
                (x_max, y_max),
                (255, 255, 255),
                2
            )

            # Gesture label
            cv2.putText(
                frame,
                gesture,
                (x_min, y_min + 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

    # FPS
    fps = calculate_fps()

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Number of hands
    cv2.putText(
        frame,
        f"Hands: {len(detected_gestures)}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Display
    cv2.imshow(
        "Advanced Hand Gesture Recognition",
        frame
    )

    # ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
hands.close()