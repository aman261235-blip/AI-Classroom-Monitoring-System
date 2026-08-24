import cv2

from app.src.face_detection import detect_and_crop_face

IMAGE_PATH = "static/students/aman.jpeg"

try:
    face = detect_and_crop_face(IMAGE_PATH)

    cv2.imshow("Detected Face", face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Face detected successfully!")

except Exception as e:
    print("Error:", e)