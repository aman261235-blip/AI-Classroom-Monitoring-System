import cv2

from app.src.camera import Camera
from app.src.dashboard import Dashboard
from app.src.yolo_detector import YOLODetector

from app.src.face_recognition import load_registered_students
from app.src.recognizer import FaceRecognizer

from app.src.track_manager import TrackManager
from app.src.attendance_manager import AttendanceManager


def main():

    print("=" * 60)
    print("AI Classroom Monitoring System")
    print("=" * 60)

    print("Loading Registered Students...")

    students = load_registered_students()

    print(f"Registered Students : {len(students)}")

    camera = Camera()

    dashboard = Dashboard()

    detector = YOLODetector()

    recognizer = FaceRecognizer(students)

    tracker = TrackManager()

    attendance = AttendanceManager()

    print("System Ready!")

    while True:

        success, frame = camera.read()

        if not success:
            break

        detections = detector.detect(frame)

        recognized_count = 0
        unknown_count = 0

        for detection in detections:

            x1, y1, x2, y2 = detection["box"]
            track_id = detection["track_id"]

            # -------------------------
            # Track Manager
            # -------------------------

            if tracker.has_track(track_id):

                tracker.update_track(track_id)

            else:

                tracker.add_track(track_id)

            # -------------------------
            # Face Recognition
            # -------------------------

            person_roi = frame[y1:y2, x1:x2]

            if not tracker.is_recognized(track_id):

                student = recognizer.recognize(person_roi)

                if student:

                    tracker.recognize_track(
                        track_id,
                        student["name"]
                    )

                    attendance.mark(student)

            label = tracker.get_name(track_id)

            if tracker.is_recognized(track_id):

                recognized_count += 1
                color = (0, 255, 0)

            else:

                unknown_count += 1
                color = (0, 0, 255)

            # -------------------------
            # Draw Bounding Box
            # -------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        tracker.cleanup()

        dashboard.draw(
            frame,
            total_students=len(detections),
            recognized_students=recognized_count,
            unknown_students=unknown_count
        )

        Camera.show(
            "AI Classroom Monitor",
            frame
        )

        if Camera.exit_pressed():
            break

    camera.release()

    Camera.destroy()


if __name__ == "__main__":
    main()