import numpy as np
from app.src.database import get_connection
from app.src.arcface_model import load_arcface

# Load ArcFace once
face_app = load_arcface()

# Threshold for recognition
SIMILARITY_THRESHOLD = 0.55


def load_registered_students():
    """
    Load all registered students and their embeddings.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            f.embedding
        FROM students s
        INNER JOIN face_embeddings f
        ON s.student_id = f.student_id
    """)

    rows = cursor.fetchall()

    students = []

    for row in rows:

        embedding = np.frombuffer(
            row["embedding"],
            dtype=np.float32
        )

        students.append({
            "student_id": row["student_id"],
            "name": row["name"],
            "embedding": embedding
        })

    cursor.close()
    conn.close()

    return students


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two embeddings.
    """

    vec1 = vec1.astype(np.float32)
    vec2 = vec2.astype(np.float32)

    similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

    return float(similarity)


def recognize_face(face_embedding, students):
    """
    Compare a live face embedding against all registered students.

    Returns:
        student dictionary if matched
        None if unknown
    """

    best_student = None
    best_score = -1

    for student in students:

        score = cosine_similarity(
            face_embedding,
            student["embedding"]
        )

        if score > best_score:
            best_score = score
            best_student = student

    if best_score >= SIMILARITY_THRESHOLD:
        return {
            "student_id": best_student["student_id"],
            "name": best_student["name"],
            "score": round(best_score, 3)
        }

    return None