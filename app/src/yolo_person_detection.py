import cv2
from ultralytics import YOLO

# ----------------------------
# Configuration
# ----------------------------

CONFIDENCE_THRESHOLD = 0.50

FRAME_WIDTH = 640
FRAME_HEIGHT = 480


def load_yolo():
    """
    Load YOLOv8 model.
    """

    print("Loading YOLOv8 Model...")

    model = YOLO("yolov8n.pt")

    print("YOLOv8 Model Loaded Successfully!")

    return model


def main():

    model = load_yolo()

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():

        print("Cannot open webcam.")
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(
            frame,
            verbose=False
        )

        person_count = 0

        for box in results[0].boxes:

            class_id = int(box.cls[0])

            # Only detect PERSON
            if class_id != 0:
                continue

            confidence = float(box.conf[0])

            # Ignore weak detections
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            person_count += 1

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"Person {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # Person Counter
        cv2.putText(
            frame,
            f"Persons Detected : {person_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.imshow(
            "AI Classroom - YOLO Person Detection",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()