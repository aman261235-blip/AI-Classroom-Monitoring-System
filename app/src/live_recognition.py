import cv2

from app.src.arcface_model import load_arcface
from app.src.face_recognition import (
    load_registered_students,
    recognize_face
)
from app.src.attendance import mark_attendance

# Load ArcFace model
face_app = load_arcface()

# Load registered students
students = load_registered_students()

# Students already marked during this session
marked_students = set()

print(f"Loaded {len(students)} registered students.")

# Start webcam
cap = cv2.VideoCapture(0)

# Reduce webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

frame_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # Process every 3rd frame
    if frame_count % 3 != 0:

        cv2.imshow("AI Classroom - Live Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue

    # Detect faces
    faces = face_app.get(frame)

    for face in faces:

        x1, y1, x2, y2 = face.bbox.astype(int)

        # Get face embedding
        embedding = face.embedding

        # Recognize student
        result = recognize_face(embedding, students)

        if result:

            student_id = result["student_id"]

            # Mark attendance only once during this session
            if student_id not in marked_students:

                attendance_marked = mark_attendance(
    student_id,
    result["name"]
)

                if attendance_marked:
                    print(f"✅ Attendance Marked : {result['name']}")
                else:
                    print(f"Already Present : {result['name']}")

                marked_students.add(student_id)

            label = f"{result['name']} ({result['score']})"
            color = (0, 255, 0)

        else:

            label = "Unknown"
            color = (0, 0, 255)

        # Draw face rectangle
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Draw name
        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("AI Classroom - Live Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()