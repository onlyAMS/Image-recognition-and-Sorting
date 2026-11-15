import cv2
import numpy as np
import serial
import time


# ---------------- TIMER ----------------

class Timer:
    def __init__(self, interval):
        self.interval = interval
        self.last_time = time.perf_counter()

    def check(self):
        current_time = time.perf_counter()

        if current_time - self.last_time >= self.interval:
            self.last_time = current_time
            return True

        return False
    def reset(self):
        self.last_time = time.perf_counter()


# ---------------- INITIALIZATION ----------------

arduino = serial.Serial('COM5', 9600, timeout=0)

time.sleep(2)

detection_timer = Timer(0.15)

cooldown_timer = Timer(2)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# ---------------- COLOR CONFIGURATION ----------------

colors = {

    "green": {
        "lower": np.array([35, 70, 40]),
        "upper": np.array([85, 255, 255]),
        "draw_color": (0, 255, 0)
    },

    "red": {
        "lower": np.array([0, 100, 100]),
        "upper": np.array([10, 255, 255]),
        "draw_color": (0, 0, 255)
    },

    "red2": {
        "lower": np.array([170, 100, 100]),
        "upper": np.array([179, 255, 255]),
        "draw_color": (0, 0, 255)
    },

    "blue": {
        "lower": np.array([100, 100, 100]),
        "upper": np.array([130, 255, 255]),
        "draw_color": (255, 0, 0)
    }

}


MIN_AREA = 500


# ---------------- SYSTEM STATE ----------------

waiting_for_arduino = False

serial_buffer = bytearray()


# ---------------- SERIAL COMMUNICATION ----------------

def send_data(data):

    arduino.write(f"{data}\n".encode('utf-8'))

    print(f"\nSent: {data}")


def read_arduino():

    global serial_buffer

    if arduino.in_waiting:

        serial_buffer.extend(
            arduino.read(arduino.in_waiting)
        )

        if b'\n' in serial_buffer:

            response, serial_buffer = serial_buffer.split(b'\n', 1)

            return response.decode('utf-8').strip()

    return None


# ---------------- COLOR DETECTION ----------------

def detect_colors(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_colors = set()

    detections = []

    red_mask = None

    for color, config in colors.items():

        mask = cv2.inRange(
            hsv,
            config["lower"],
            config["upper"]
        )

        # Combine red masks
        if color == "red":

            red_mask = mask
            continue

        elif color == "red2":

            red_mask = cv2.bitwise_or(red_mask, mask)

            mask = red_mask
            color_name = "red"

        else:

            color_name = color

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:

            area = cv2.contourArea(contour)

            if area > MIN_AREA:

                x, y, w, h = cv2.boundingRect(contour)

                detected_colors.add(color_name)

                detections.append({
                    "color": color_name,
                    "area": area,
                    "box": (x, y, w, h),
                    "draw_color": config["draw_color"]
                })

    # Draw bounding boxes
    for detection in detections:

        x, y, w, h = detection["box"]

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            detection["draw_color"],
            2
        )

        cv2.putText(
            frame,
            detection["color"].upper(),
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            detection["draw_color"],
            2
        )

    return detected_colors, detections


# ---------------- MAIN LOOP ----------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Detect colors
    detected_colors, detections = detect_colors(frame)


    # STATE 1: SCANNING

    if not waiting_for_arduino:

        if detection_timer.check() and cooldown_timer.check():

            if detections:
                largest_detection = max(
                    detections,
                    key=lambda item: item["area"]
                )

                detected_color = largest_detection["color"]

                send_data(detected_color)

                waiting_for_arduino = True


    # STATE 2: WAITING FOR ARDUINO

    else:

        print("Waiting...", end="\r")

        response = read_arduino()

        if response:
            print(f"\nArduino responded: {response}")

            cooldown_timer.reset()  # Start a fresh 2-second cooldown

            waiting_for_arduino = False


    # CAMERA DISPLAY

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ---------------- CLEANUP ----------------

cap.release()

cv2.destroyAllWindows()

arduino.close()