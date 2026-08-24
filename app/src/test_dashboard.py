from app.src.camera import Camera
from app.src.dashboard import Dashboard

camera = Camera()

dashboard = Dashboard()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = dashboard.draw(
        frame,
        total_students=5,
        recognized_students=3,
        unknown_students=2
    )

    Camera.show(
        "Dashboard Test",
        frame
    )

    if Camera.exit_pressed():
        break

camera.release()

Camera.destroy()