import cv2

from app.src.frame_processor import FrameProcessor

processor = FrameProcessor()


def generate_frames():

    camera = cv2.VideoCapture(0)

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame = processor.process(frame)

        _, buffer = cv2.imencode(".jpg", frame)

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + buffer.tobytes() +
            b'\r\n'
        )

    camera.release()