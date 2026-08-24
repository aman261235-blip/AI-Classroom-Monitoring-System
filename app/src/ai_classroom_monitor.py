import cv2
import time

from ultralytics import YOLO

from app.src.arcface_model import load_arcface
from app.src.face_recognition import (
    load_registered_students,
    recognize_face
)
from app.src.track_manager import TrackManager
from app.src.attendance import mark_attendance

# ==========================================================
# CONFIGURATION
# ==========================================================

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

FRAME_SKIP = 2

CONFIDENCE_THRESHOLD = 0.50

TRACK_TIMEOUT = 5

# ==========================================================
# LOAD AI MODELS
# ==========================================================

print("=" * 60)
print("      AI Classroom Monitor Starting")
print("=" * 60)

print("Loading YOLO...")

yolo = YOLO("yolov8n.pt")

print("YOLO Loaded")

print("Loading ArcFace...")

arcface = load_arcface()

print("ArcFace Loaded")

print("Loading Registered Students...")

students = load_registered_students()

print(f"Registered Students : {len(students)}")

track_manager = TrackManager()

attendance_cache = set()

# ==========================================================
# CAMERA
# ==========================================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():

    print("Cannot open webcam.")

    exit()

frame_count = 0

start_time = time.time()

print("=" * 60)
print("AI Classroom Monitor Started Successfully")
print("=" * 60)

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # Frame Skipping
    if frame_count % FRAME_SKIP != 0:

        cv2.imshow(
            "AI Classroom Monitor",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue

    # ----------------------------------------
    # YOLO Tracking
    # ----------------------------------------

    results = yolo.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    display = frame.copy()

    total_students = 0
    recognized_students = 0
    unknown_students = 0

    fps = int(
        frame_count /
        (time.time() - start_time)
    )

    # ======================================================
    # PART B CONTINUES FROM HERE
    # ======================================================

    cv2.imshow(
        "AI Classroom Monitor",
        display
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()