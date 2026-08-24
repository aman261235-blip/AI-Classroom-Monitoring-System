import cv2
from ultralytics import YOLO

# -----------------------------
# Load YOLO Model
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Open Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

print("Starting Student Tracking...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # -----------------------------
    # Track Persons
    # -----------------------------
    results = model.track(
        frame,
        persist=True,
        classes=[0],      # Person only
        verbose=False
    )

    if len(results) == 0:
        continue

    boxes = results[0].boxes

    if boxes.id is not None:

        ids = boxes.id.int().cpu().tolist()

        coordinates = boxes.xyxy.cpu().numpy()

        confidences = boxes.conf.cpu().numpy()

        for track_id, box, confidence in zip(
            ids,
            coordinates,
            confidences
        ):

            x1, y1, x2, y2 = map(int, box)

            # Bounding Box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Student Label
            label = f"Student {track_id}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # Total Count
    total_students = 0

    if boxes.id is not None:
        total_students = len(boxes.id)

    cv2.putText(
        frame,
        f"Students Detected : {total_students}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.imshow(
        "AI Classroom Student Tracking",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()