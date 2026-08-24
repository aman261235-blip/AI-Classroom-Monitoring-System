"""
AI Classroom System Configuration
"""

# ==========================
# CAMERA SETTINGS
# ==========================

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# ==========================
# FACE DETECTION
# ==========================

DETECTION_SIZE = (640, 640)

# Process every Nth frame
# Higher value = Faster
# Lower value = More Accurate
PROCESS_EVERY_N_FRAMES = 5

# ==========================
# FACE RECOGNITION
# ==========================

# Recognition similarity threshold
RECOGNITION_THRESHOLD = 0.55

# Cache recognized faces (seconds)
FACE_CACHE_SECONDS = 3

# ==========================
# PERFORMANCE
# ==========================

ENABLE_FACE_CACHE = True

ENABLE_FRAME_SKIP = True

ENABLE_FACE_TRACKING = False

ENABLE_MULTITHREADING = False

# ==========================
# ATTENDANCE
# ==========================

MARK_ONLY_ONCE_PER_SESSION = True

# ==========================
# DISPLAY
# ==========================

FONT_SCALE = 0.7

BOX_THICKNESS = 2

TEXT_THICKNESS = 2