from datetime import datetime
from app.src.database import get_connection


def mark_attendance(student_id, name):
    """
    Mark attendance only once per day.
    Returns True if attendance is newly marked,
    otherwise returns False.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    today = datetime.now().date()

    # Check if already marked today
    cursor.execute("""
        SELECT id
        FROM attendance
        WHERE student_id = %s
        AND attendance_date = %s
    """, (student_id, today))

    record = cursor.fetchone()

    if record:
        cursor.close()
        conn.close()
        return False

    # Insert attendance
    cursor.execute("""
        INSERT INTO attendance
        (
            student_id,
            name,
            attendance_date,
            attendance_time,
            status
        )
        VALUES
        (
            %s,
            %s,
            CURDATE(),
            CURTIME(),
            'Present'
        )
    """, (student_id, name))

    conn.commit()

    cursor.close()
    conn.close()

    return True