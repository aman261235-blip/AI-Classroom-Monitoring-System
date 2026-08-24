from app.src.camera import Camera

camera = Camera()

while True:

    success, frame = camera.read()

    if not success:
        break

    Camera.show(
        "Camera Test",
        frame
    )

    if Camera.exit_pressed():
        break

camera.release()

Camera.destroy()