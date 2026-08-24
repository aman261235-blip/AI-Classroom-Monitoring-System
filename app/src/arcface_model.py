from insightface.app import FaceAnalysis

# Global model instance
face_app = None


def load_arcface():
    """
    Load the InsightFace model only once.
    """

    global face_app

    if face_app is None:

        print("Loading ArcFace Model...")

        face_app = FaceAnalysis(
            name="buffalo_l",
            providers=[
                "CPUExecutionProvider"
            ]
        )

        face_app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

        print("ArcFace Model Loaded Successfully!")

    return face_app


def generate_embedding(face):
    """
    Generate a 512-dimensional embedding
    from a detected InsightFace Face object.
    """

    return face.embedding