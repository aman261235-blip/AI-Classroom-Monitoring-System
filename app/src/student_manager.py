import os
import uuid
import numpy as np
from werkzeug.utils import secure_filename

from app.src.database import get_connection
from app.src.face_detection import detect_face
from app.src.arcface_model import generate_embedding

UPLOAD_FOLDER = "static/students"

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------
# Get All Students
# ---------------------------------

def get_all_students():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY student_id
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students


# ---------------------------------
# Get Single Student
# ---------------------------------

def get_student(student_id):

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM students
        WHERE student_id=%s
    """, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return student


# ---------------------------------
# Update Student
# ---------------------------------

def update_student(student_id, form, photo):

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM students
        WHERE student_id=%s
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        cursor.close()
        connection.close()
        return False, "Student not found."

    image_path = student["image_path"]

    # ---------------------------------
    # Upload New Photo
    # ---------------------------------

    if photo and photo.filename:

        if not allowed_file(photo.filename):
            cursor.close()
            connection.close()
            return False, "Only JPG, JPEG and PNG files are allowed."

        # Delete old image
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        # Generate unique filename
        filename = f"{uuid.uuid4().hex}_{secure_filename(photo.filename)}"

        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        # Save new image
        photo.save(image_path)

        # Detect face
        face, image = detect_face(image_path)

        # Generate embedding
        embedding = generate_embedding(face)

        embedding_bytes = embedding.astype(
            np.float32
        ).tobytes()

        # Delete old embedding
        cursor.execute("""
            DELETE FROM face_embeddings
            WHERE student_id=%s
        """, (student_id,))

        # Insert new embedding
        cursor.execute("""
            INSERT INTO face_embeddings
            (
                student_id,
                embedding
            )
            VALUES
            (
                %s,
                %s
            )
        """, (
            student_id,
            embedding_bytes
        ))

    # ---------------------------------
    # Update Student Details
    # ---------------------------------

    cursor.execute("""
        UPDATE students
        SET
            name=%s,
            roll_number=%s,
            department=%s,
            semester=%s,
            image_path=%s
        WHERE student_id=%s
    """, (
        form["name"],
        form["roll_number"],
        form["department"],
        form["semester"],
        image_path,
        student_id
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return True, "Student Updated Successfully"
import os

from app.src.database import get_connection


def delete_student(student_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get image path
    cursor.execute("""
        SELECT image_path
        FROM students
        WHERE student_id=%s
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        cursor.close()
        conn.close()
        return False

    image_path = student["image_path"]

    # Delete embedding
    cursor.execute("""
        DELETE FROM face_embeddings
        WHERE student_id=%s
    """, (student_id,))

    # Delete attendance
    cursor.execute("""
        DELETE FROM attendance
        WHERE student_id=%s
    """, (student_id,))

    # Delete student
    cursor.execute("""
        DELETE FROM students
        WHERE student_id=%s
    """, (student_id,))

    conn.commit()

    cursor.close()
    conn.close()

    # Delete photo from disk
    if image_path:

        if os.path.exists(image_path):
            os.remove(image_path)

    return True