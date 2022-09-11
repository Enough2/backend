import io
from threading import Condition, Thread
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
