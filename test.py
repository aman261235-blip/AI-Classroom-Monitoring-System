from app.src.face_recognition import load_registered_students

students = load_registered_students()

print("=" * 50)
print("REGISTERED STUDENTS")
print("=" * 50)

print("Total Students :", len(students))
print()

for student in students:

    print("Student ID :", student["student_id"])
    print("Name       :", student["name"])
    print("Department :", student["department"])
    print("Semester   :", student["semester"])
    print("Embedding Shape :", student["embedding"].shape)
    print("-" * 50)