import cv2

from app.src.dashboard import Dashboard
from app.src.yolo_detector import YOLODetector
from app.src.face_recognition import load_registered_students
from app.src.recognizer import FaceRecognizer
from app.src.track_manager import TrackManager
from app.src.attendance_manager import AttendanceManager


class FrameProcessor:

    def __init__(self):

        students = load_registered_students()

        self.detector = YOLODetector()

        self.recognizer = FaceRecognizer(students)

        self.tracker = TrackManager()

        self.attendance = AttendanceManager()

        self.dashboard = Dashboard()

    def process(self, frame):

        detections = self.detector.detect(frame)

        recognized = 0
        unknown = 0

        for detection in detections:

            x1, y1, x2, y2 = detection["box"]

            track_id = detection["track_id"]

            if self.tracker.has_track(track_id):

                self.tracker.update_track(track_id)

            else:

                self.tracker.add_track(track_id)

            person_roi = frame[y1:y2, x1:x2]

            if not self.tracker.is_recognized(track_id):

                student = self.recognizer.recognize(person_roi)

                if student:

                    self.tracker.recognize_track(
                        track_id,
                        student["name"]
                    )

                    self.attendance.mark(student)

            label = self.tracker.get_name(track_id)

            if self.tracker.is_recognized(track_id):

                color = (0,255,0)

                recognized += 1

            else:

                color = (0,0,255)

                unknown += 1

            cv2.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                color,
                2
            )

            cv2.putText(
                frame,
                label,
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        self.tracker.cleanup()

        self.dashboard.draw(
            frame,
            len(detections),
            recognized,
            unknown
        )

        return frame