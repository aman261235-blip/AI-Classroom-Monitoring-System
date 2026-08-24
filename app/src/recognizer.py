from app.src.arcface_model import load_arcface
from app.src.face_recognition import recognize_face


class FaceRecognizer:
    """
    Handles face detection and recognition.
    """

    def __init__(self, students):

        print("Loading Recognition Engine...")

        self.face_app = load_arcface()

        self.students = students

        print("Recognition Engine Ready!")

    def recognize(self, person_roi):
        """
        Detect face inside a person's ROI and recognize it.

        Returns:
            dict -> student information
            None -> face not recognized
        """

        if person_roi is None:
            return None

        if person_roi.size == 0:
            return None

        try:

            faces = self.face_app.get(person_roi)

        except Exception:

            return None

        if len(faces) == 0:
            return None

        # Largest detected face
        face = max(
            faces,
            key=lambda f: (
                (f.bbox[2] - f.bbox[0]) *
                (f.bbox[3] - f.bbox[1])
            )
        )

        embedding = face.embedding

        student = recognize_face(
            embedding,
            self.students
        )

        return student