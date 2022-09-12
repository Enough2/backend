from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from stream import Camera
from model import Pipeline

app = FastAPI()
camera = Camera()
pipeline = Pipeline()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/stream")
def stream():
    return StreamingResponse(
        camera.generate(),
        headers={"Cache-Control": "no-cache, private", "Pragma": "no-cache"},
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.get("/detect")
def detect():
    res = camera.detect()
    return {"detected": res}


@app.get("/predict")
def predict():
    img = camera.cam.capture_image()
    img = img.convert("RGB")
    res = pipeline.predict_image(img)
    return res
