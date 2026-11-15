import cv2
from ultralytics import YOLO
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


# ---------------- INITIALIZATION ----------------

arduino = serial.Serial('COM5', 9600, timeout=0)

time.sleep(2)

model = YOLO("yolo26n.pt")

allowed_classes = [
    cls_id for cls_id in model.names
    if cls_id != 0
]

detection_timer = Timer(0.15)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


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

        serial_buffer.extend(arduino.read(arduino.in_waiting))

        if b'\n' in serial_buffer:

            response, serial_buffer = serial_buffer.split(b'\n', 1)

            return response.decode('utf-8').strip()

    return None


# ---------------- MAIN LOOP ----------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # STATE 1: SCANNING

    if not waiting_for_arduino:

        if detection_timer.check():

            results = model(
                frame,
                classes=allowed_classes,
                imgsz=416,
                conf=0.4,
                verbose=False
            )

            if len(results[0].boxes) > 0:

                send_data("Object detected")

                waiting_for_arduino = True

    # STATE 2: WAITING FOR ARDUINO

    else:

        print("Waiting...", end="\r")

        response = read_arduino()

        if response:

            print(f"\nArduino responded: {response}")

            waiting_for_arduino = False

    # CAMERA DISPLAY

    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ---------------- CLEANUP ----------------

cap.release()
cv2.destroyAllWindows()

arduino.close()