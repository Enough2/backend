from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from stream import Camera

app = FastAPI()
camera = Camera()


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
