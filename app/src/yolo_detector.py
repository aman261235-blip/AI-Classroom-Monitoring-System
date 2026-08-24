from ultralytics import YOLO


class YOLODetector:
    """
    YOLOv8 + ByteTrack Detector
    """

    def __init__(self):

        print("Loading YOLOv8...")

        self.model = YOLO("yolov8n.pt")

        print("YOLO Loaded Successfully!")

    def detect(self, frame):
        """
        Detect and track persons.

        Returns:
            [
                {
                    "track_id": int,
                    "box": [x1, y1, x2, y2],
                    "confidence": float
                }
            ]
        """

        results = self.model.track(
            frame,
            persist=True,
            classes=[0],      # Person class only
            verbose=False
        )

        detections = []

        if len(results) == 0:
            return detections

        boxes = results[0].boxes

        if boxes.id is None:
            return detections

        ids = boxes.id.int().cpu().tolist()
        coordinates = boxes.xyxy.cpu().numpy()
        confidences = boxes.conf.cpu().numpy()

        for track_id, box, confidence in zip(
            ids,
            coordinates,
            confidences
        ):

            x1, y1, x2, y2 = map(int, box)

            detections.append({
                "track_id": track_id,
                "box": (x1, y1, x2, y2),
                "confidence": float(confidence)
            })

        return detections