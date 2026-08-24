import cv2
from ultralytics import YOLO

# Load YOLO Model
model = YOLO("yolov8n.pt")

# Open Webcam
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    total_students = 0

    if len(results):

        boxes = results[0].boxes

        if boxes.id is not None:

            total_students = len(boxes.id)

        annotated = results[0].plot()

    else:

        annotated = frame

    # -----------------------------
    # Monitoring Panel
    # -----------------------------

    cv2.rectangle(
        annotated,
        (10, 10),
        (330, 140),
        (40, 40, 40),
        -1
    )

    cv2.putText(
        annotated,
        "AI Classroom Monitor",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        annotated,
        f"Students Detected : {total_students}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # Temporary values
    recognized_students = 0
    unknown_students = total_students

    cv2.putText(
        annotated,
        f"Recognized : {recognized_students}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated,
        f"Unknown : {unknown_students}",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "AI Classroom Monitoring",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()