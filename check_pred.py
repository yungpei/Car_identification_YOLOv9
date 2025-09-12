import torch
from models.yolo import Model
from pathlib import Path

# 測試模型設定，可以改成 yolov9-s.yaml / yolov9-m.yaml / yolov9-c.yaml
CFG = "models/detect/yolov9-s.yaml"

def print_structure(obj, indent=0, max_depth=3):
    """遞迴印出物件結構 (list/tuple/tensor)"""
    prefix = " " * indent
    if isinstance(obj, torch.Tensor):
        print(f"{prefix}Tensor shape: {tuple(obj.shape)} dtype: {obj.dtype}")
    elif isinstance(obj, (list, tuple)):
        print(f"{prefix}{type(obj).__name__} (len={len(obj)})")
        if indent // 2 < max_depth:  # 避免無窮遞迴
            for i, elem in enumerate(obj):
                print(f"{prefix} └── [{i}]")
                print_structure(elem, indent + 4, max_depth)
    else:
        print(f"{prefix}{type(obj)}: {obj}")

if __name__ == "__main__":
    # 建立模型
    model = Model(CFG, ch=3, nc=1, anchors=None)  # nc=1 表示你的車牌資料集
    model.eval()

    # 假資料 (batch=2, RGB, 640x640)
    x = torch.randn(2, 3, 640, 640)

    # 前向傳播
    with torch.no_grad():
        pred = model(x)

    print("=== 模型 forward 輸出結構 ===")
    print_structure(pred)
