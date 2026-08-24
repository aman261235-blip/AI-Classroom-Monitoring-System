import cv2


class Camera:

    def __init__(
        self,
        camera_index=0,
        width=640,
        height=480
    ):

        print("Opening Camera...")

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Cannot open webcam.")

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height
        )

        print("Camera Ready!")

    def read(self):
        """
        Read one frame.

        Returns:
            success (bool)
            frame (numpy array)
        """

        return self.cap.read()

    def release(self):
        """
        Release camera.
        """

        self.cap.release()

    @staticmethod
    def show(window_name, frame):
        """
        Display a frame.
        """

        cv2.imshow(window_name, frame)

    @staticmethod
    def exit_pressed():
        """
        Returns True if Q is pressed.
        """

        return cv2.waitKey(1) & 0xFF == ord("q")

    @staticmethod
    def destroy():
        """
        Close all OpenCV windows.
        """

        cv2.destroyAllWindows()