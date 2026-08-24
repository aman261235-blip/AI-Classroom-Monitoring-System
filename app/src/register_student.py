import os
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

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_student(form, photo):

    student_id = form["student_id"]
    name = form["name"]
    roll_number = form["roll_number"]
    department = form["department"]
    semester = form["semester"]

    if photo.filename == "":
        return False, "No image selected."

    if not allowed_file(photo.filename):
        return False, "Only JPG, JPEG and PNG images are allowed."

    filename = secure_filename(photo.filename)

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    photo.save(image_path)

    connection = get_connection()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    # Check duplicate student
    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE student_id=%s
        OR roll_number=%s
        """,
        (
            student_id,
            roll_number
        )
    )

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False, "Student already exists."

    # Save student details
    cursor.execute(
        """
        INSERT INTO students
        (
            student_id,
            name,
            roll_number,
            department,
            semester,
            image_path
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            student_id,
            name,
            roll_number,
            department,
            semester,
            image_path
        )
    )

    # -------------------------
    # AI FACE REGISTRATION
    # -------------------------

    try:

        face, image = detect_face(image_path)

        embedding = generate_embedding(face)

        embedding_bytes = embedding.astype(
            np.float32
        ).tobytes()

        cursor.execute(
            """
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
            """,
            (
                student_id,
                embedding_bytes
            )
        )

    except Exception as e:

        connection.rollback()

        cursor.close()
        connection.close()

        return False, f"Face Registration Failed : {e}"

    connection.commit()

    cursor.close()
    connection.close()

    return True, "Student Registered Successfully"