import cv2

from insightface.app import FaceAnalysis

# Load InsightFace model
face_app = FaceAnalysis(
    name="buffalo_l",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)
face_app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open webcam.")
    exit()

print("Webcam Started...")

while True:

    success, frame = camera.read()

    if not success:
        break

    # Detect faces
    faces = face_app.get(frame)

    for face in faces:

        x1, y1, x2, y2 = face.bbox.astype(int)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "AI Classroom - Face Detection",
        frame
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()