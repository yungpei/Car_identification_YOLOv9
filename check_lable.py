import os

labels_path = r"C:\Users\user\Documents\yolov9\Carplatev9\train\labels"

for file in os.listdir(labels_path):
    if file.endswith(".txt"):
        path = os.path.join(labels_path, file)
        with open(path, "r") as f:
            lines = f.readlines()
        if len(lines) == 0:
            print("⚠️ 空標籤檔:", path)
        else:
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 5:
                    print("⚠️ 格式錯誤:", path, line.strip())
                else:
                    cls, x, y, w, h = parts
                    try:
                        x, y, w, h = map(float, [x, y, w, h])
                        if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                            print("⚠️ 超出範圍:", path, line.strip())
                    except:
                        print("⚠️ 非數字:", path, line.strip())
