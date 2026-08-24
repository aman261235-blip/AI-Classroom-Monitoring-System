from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)
from flask import send_file
from app.src.report_generator import export_attendance_excel
from flask import Response
from app.src.video_stream import generate_frames
from app.src.database import get_connection
from app.src.register_student import save_student
from app.src.student_manager import (
    get_all_students,
    get_student,
    update_student,
    delete_student
)


app = Flask(__name__)


# ---------------- Dashboard ----------------

@app.route("/")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Students
    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    # Today's Attendance Count
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE attendance_date = CURDATE()
    """)
    todays_attendance = cursor.fetchone()["total"]

    # Today's Attendance Records
    cursor.execute("""
        SELECT
            student_id,
            name,
            attendance_date,
            attendance_time,
            status
        FROM attendance
        WHERE attendance_date = CURDATE()
        ORDER BY attendance_time DESC
    """)

    attendance_list = cursor.fetchall()

    unknown_persons = 0
    camera_status = "OFF"

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        todays_attendance=todays_attendance,
        unknown_persons=unknown_persons,
        camera_status=camera_status,
        attendance_list=attendance_list
    )
@app.route("/attendance_data")
def attendance_data():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Students
    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    # Today's Attendance
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE attendance_date = CURDATE()
    """)
    todays_attendance = cursor.fetchone()["total"]

    # Attendance List
    cursor.execute("""
        SELECT
            student_id,
            name,
            attendance_date,
            attendance_time,
            status
        FROM attendance
        WHERE attendance_date = CURDATE()
        ORDER BY attendance_time DESC
    """)

    attendance = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "total_students": total_students,
        "todays_attendance": todays_attendance,
        "attendance": attendance
    })

# ---------------- Student List ----------------

@app.route("/students")
def students():

    students = get_all_students()

    return render_template(
        "students.html",
        students=students
    )


# ---------------- Edit Student Page ----------------

@app.route("/edit_student/<student_id>")
def edit_student(student_id):

    student = get_student(student_id)

    return render_template(
        "edit_student.html",
        student=student
    )
@app.route("/update_student/<student_id>", methods=["POST"])
def update_student_route(student_id):

    photo = request.files.get("photo")

    success, message = update_student(
        student_id,
        request.form,
        photo
    )

    if success:
        return redirect(url_for("students"))

    return message

@app.route("/delete_student/<student_id>")
def delete_student_route(student_id):

    delete_student(student_id)

    return redirect(url_for("students"))

# ---------------- Add Student Page ----------------

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")


# ---------------- Save Student ----------------

@app.route("/save_student", methods=["POST"])
def save_student_route():

    success, message = save_student(
        request.form,
        request.files["photo"]
    )

    if success:
        return redirect(url_for("students"))

    return message


# ---------------- Run Flask ----------------
@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )
@app.route("/export_excel")
def export_excel():

    filename = export_attendance_excel()

    return send_file(
        filename,
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)