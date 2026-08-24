import cv2
import time


class Dashboard:

    def __init__(self):

        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0

    def update_fps(self):

        self.frame_count += 1

        elapsed = time.time() - self.start_time

        if elapsed >= 1:

            self.fps = self.frame_count / elapsed

            self.frame_count = 0
            self.start_time = time.time()

    def draw(
        self,
        frame,
        total_students,
        recognized_students,
        unknown_students
    ):

        self.update_fps()

        # Background Panel
        cv2.rectangle(
            frame,
            (10, 10),
            (370, 170),
            (40, 40, 40),
            -1
        )

        cv2.putText(
            frame,
            "AI Classroom Monitor",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Students : {total_students}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Recognized : {recognized_students}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Unknown : {unknown_students}",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"FPS : {self.fps:.1f}",
            (220, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Camera : ON",
            (220, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        return frame