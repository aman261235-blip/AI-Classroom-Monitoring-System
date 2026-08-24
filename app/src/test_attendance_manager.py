from app.src.attendance_manager import AttendanceManager

manager = AttendanceManager()

student = {
    "student_id": "0001",
    "name": "aiyan shaikh"
}

print(manager.mark(student))
print(manager.mark(student))

print(
    "Total Marked:",
    manager.total_marked()
)
