import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def check_color(h, s, v):
    if 35 <= h <= 85 and s >= 70 and 40 <= v <= 255:
        return 'Green'

    elif (h <= 10 or h >= 170) and s >= 100 and v >= 100:
        return 'Red'

    elif 100 <= h <= 130 and s >= 100 and v >= 100:
        return 'Blue'

    else:
        return 'Color not chosen'


# Define HSV ranges
colors = {
    "Green": ([35, 70, 40], [85, 255, 255]),
    "Red1": ([0, 100, 100], [10, 255, 255]),
    "Red2": ([170, 100, 100], [179, 255, 255]),
    "Blue": ([100, 100, 100], [130, 255, 255])
}


while True:

    ret, frame = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for each color
    for color, (lower, upper) in colors.items():

        lower = np.array(lower)
        upper = np.array(upper)

        mask = cv2.inRange(hsv, lower, upper)

        # Combine the two red masks
        if color == "Red2":
            red_mask = cv2.bitwise_or(red_mask, mask)
            continue

        if color == "Red1":
            red_mask = mask
            continue

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Draw bounding boxes
        for contour in contours:

            area = cv2.contourArea(contour)

            if area > 500:

                x, y, w, h = cv2.boundingRect(contour)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0) if color == "Green" else (255, 0, 0),
                    2
                )

                cv2.putText(
                    frame,
                    color,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

    # Process red separately
    contours, _ = cv2.findContours(
        red_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:

        if cv2.contourArea(contour) > 500:

            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "Red",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()