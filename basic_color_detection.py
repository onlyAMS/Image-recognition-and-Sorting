import cv2

cap = cv2.VideoCapture(0)

def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = param
        color = check_color(hsv[y, x][0], hsv[y, x][1], hsv[y, x][2])
        print(f"HSV: {hsv[y, x]}"
              f"color: {color}")


        #print(type(hsv[y, x][0]))

def check_color(h, s, v):
    if 35 <= h <= 85 and s >= 70 and 40 <= v <= 255:
        return 'Green'

    elif (h <= 10 or h >= 170) and s >= 100 and v >= 100:
        return 'Red'

    elif 100 <= h <= 130 and s >= 100 and v >= 100:
        return 'Blue'

    else:
        return 'Color not chosen'

cv2.namedWindow("Camera")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.setMouseCallback("Camera", get_color, hsv)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()