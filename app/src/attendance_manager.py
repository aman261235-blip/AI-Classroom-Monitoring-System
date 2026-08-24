from app.src.attendance import mark_attendance


class AttendanceManager:
    """
    Handles attendance marking and prevents
    duplicate attendance during a session.
    """

    def __init__(self):

        self.marked_students = set()

    def mark(self, student):

        """
        student -> recognize_face() result

        Returns:
            True  -> Newly marked
            False -> Already marked
        """

        if student is None:
            return False

        student_id = student["student_id"]

        if student_id in self.marked_students:
            return False

        success = mark_attendance(
            student_id,
            student["name"]
        )

        if success:

            self.marked_students.add(
                student_id
            )

            print(
                f"✅ Attendance Marked : {student['name']}"
            )

        return success

    def reset(self):
        """
        Clear session attendance cache.
        """

        self.marked_students.clear()

    def total_marked(self):

        return len(
            self.marked_students
        )