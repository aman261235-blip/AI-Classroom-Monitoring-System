import cv2
from app.src.arcface_model import load_arcface


def detect_face(image_path):
    """
    Detect the largest face in an image.

    Returns:
        face_object
        image
    """

    # Load ArcFace Model
    face_app = load_arcface()

    # Read Image
    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Unable to read image: {image_path}")

    # Detect Faces
    faces = face_app.get(image)

    if len(faces) == 0:
        raise Exception("No face detected in uploaded image.")

    # Select largest face
    largest_face = max(
        faces,
        key=lambda face:
        (face.bbox[2] - face.bbox[0]) *
        (face.bbox[3] - face.bbox[1])
    )

    return largest_face, image