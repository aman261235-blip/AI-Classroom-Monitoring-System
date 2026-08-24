import cv2

from app.src.face_recognition import load_registered_students
from app.src.recognizer import FaceRecognizer

students = load_registered_students()

recognizer = FaceRecognizer(students)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = recognizer.recognize(frame)

    if result:

        text = f"{result['name']} ({result['score']})"

        color = (0, 255, 0)

    else:

        text = "Unknown"

        color = (0, 0, 255)

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow(
        "Recognition Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()
