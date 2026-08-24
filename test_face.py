import cv2

from app.src.face_detection import detect_face

IMAGE_PATH = "static/students/aman.jpeg"     # Change filename if needed

try:

    face, image = detect_face(IMAGE_PATH)

    x1, y1, x2, y2 = face.bbox.astype(int)

    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    cv2.imshow("Detected Face", image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    print("Face Detected Successfully!")

    print("Embedding Size :", len(face.embedding))

except Exception as e:

    print(e)