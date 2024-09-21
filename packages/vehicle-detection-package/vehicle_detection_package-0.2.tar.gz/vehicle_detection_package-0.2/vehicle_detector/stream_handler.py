import cv2

class StreamHandler:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.cap = cv2.VideoCapture(self.stream_url)

        if not self.cap.isOpened():
            raise ValueError("Error: Unable to open video stream!")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Unable to read frame from stream!")
            return None
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def show_frame(self, frame, window_name='Vehicle Detection and Tracking'):
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.release()
            exit()

