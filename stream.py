import io
import cv2
import numpy as np
from threading import Condition
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class Output(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class Camera:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(
            self.cam.create_video_configuration(main={"size": (640, 480)})
        )
        self.output = Output()
        self.cam.start_recording(JpegEncoder(), FileOutput(self.output))

    def generate(self):
        while True:
            with self.output.condition:
                self.output.condition.wait()
                frame = self.output.frame
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    def detect(self):
        imgs = [self.cam.capture_array() for i in range(3)]
        gray = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in imgs]

        diff_a = cv2.absdiff(gray[0], gray[1])
        diff_b = cv2.absdiff(gray[1], gray[2])

        ret, diff_a = cv2.threshold(diff_a, 25, 255, cv2.THRESH_BINARY)
        ret, diff_b = cv2.threshold(diff_b, 25, 255, cv2.THRESH_BINARY)

        diff = cv2.bitwise_and(diff_a, diff_b)
        diff_cnt = cv2.countNonZero(diff)

        return diff_cnt
