import cv2
import time
from ultralytics import YOLO

# Load YOLO model (downloads automatically on first run)
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

prev_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame.")
        break

    # Run YOLO detection
    results = model(frame, verbose=False)

    person_count = 0

    for result in results:
        boxes = result.boxes

        for box in boxes:
            cls = int(box.cls[0])

            # COCO class 0 = Person
            if cls == 0:
                person_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                cv2.rectangle(frame,
                              (x1, y1),
                              (x2, y2),
                              (0, 255, 0),
                              2)

                cv2.putText(
                    frame,
                    f"Person {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display count and FPS
    cv2.putText(frame,
                f"Students: {person_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2)

    cv2.putText(frame,
                f"FPS: {fps:.1f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2)

    cv2.imshow("AI Classroom - Student Counter", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()