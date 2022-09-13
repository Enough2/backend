# backend

> ⚙️ RPi 카메라 스트리밍 및 API 서버

```
* PyTorch를 통한 쓰레기 이미지 분류 AI 개발을 위해 시작된 프로젝트입니다.
  Picamera2는 현재 베타 버전으로 예상치 못한 버그가 발생할 수 있습니다.
```

<br>

Raspberry Pi OS Bullseye의 **RPi 레거시 카메라 스택**을 위한 스트리밍 및 API 백엔드 서버입니다. MJPEG 카메라 스트리밍, 모션(움직임) 감지, PyTorch 분류 예측 기능을 지원합니다.

[_FastAPI_](https://github.com/tiangolo/fastapi)를 웹 프레임워크로 하여, 카메라 접근에 [_Picamera2_](https://github.com/raspberrypi/picamera2)를, 모션 감지에 [_opencv-python_](https://github.com/opencv/opencv-python)를, 이미지 분류에 [_PyTorch_](https://github.com/pytorch/pytorch)의 ResNet152 전이학습 모델을 사용합니다. 모델에 관한 자세한 사항은 [_Enough2/ml_](https://github.com/Enough2/ml)을 참고해주세요.

<br>

```
$ pip3 install -r requirements.txt
```

```
$ uvicorn app:app (--host 0.0.0.0)
```

-   `/stream` - RPi 카메라 MJPEG 스트리밍
-   `/detect` - 모션 감지 여부 확인 (웹소켓)
-   `/predict` - 이미지 분류 예측

<br>

\* _Raspberry Pi OS Bullseye ARM64 Full (2022-09-06)_ 의 _Python 3.9.2_ 환경에서 테스트되었습니다.
