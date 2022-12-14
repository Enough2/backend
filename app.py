from fastapi import FastAPI, WebSocket
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


@app.websocket("/detect")
async def detect(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            res = camera.detect()
            if res:
                await websocket.send_text('1')
            else:
                await websocket.send_text('0')
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@app.get("/predict")
def predict():
    img = camera.cam.capture_image()
    img = img.convert("RGB")
    res = pipeline.predict_image(img)
    return res
