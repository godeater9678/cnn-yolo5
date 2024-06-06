import os
import pathlib
import platform
from pathlib import Path, PosixPath, WindowsPath

# 윈도우에서 만든 모델을 로드할때 패스 에러가 발생하는 것을 막기위함
# Check if the OS is macOS
if platform.system() == 'Darwin':
    # Override WindowsPath to PosixPath
    pathlib.WindowsPath = PosixPath

import torch
from PIL import Image
from common.util import get_root_path

# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
# python train.py --img 640 --batch 16 --epochs 50 --data data/dataset/data.yaml --weights yolov5s.pt  --name kr-food
modelPath = f'{get_root_path()}/domain/yolo/model/best.pt'
# modelPath = f'best.pt'
if not os.path.exists(modelPath):
    raise Exception(f"Model file not found at {modelPath}")

model = torch.hub.load('ultralytics/yolov5', 'custom', path=modelPath, force_reload=False)
model.conf = 0.4


def classify_image(image_path):
    img = Image.open(image_path)
    results = model(img)
    predictions = results.pandas().xyxy[0]
    if predictions.empty:
        return None
    else:
        return {
            'names': predictions['name'].tolist(),
            'results': results
        }
