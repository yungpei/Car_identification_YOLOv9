import os
import glob

def poly2bbox(coords):
    """
    將多邊形 (polygon) 座標轉換成 YOLO 格式的 bounding box
    coords: [x1, y1, x2, y2, ...]
    return: xc, yc, w, h
    """
    xs = coords[0::2]
    ys = coords[1::2]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    xc = (x_min + x_max) / 2
    yc = (y_min + y_max) / 2
    w = x_max - x_min
    h = y_max - y_min
    return xc, yc, w, h


def fix_labels(label_path):
    """
    批次修正 YOLO label 檔案:
    - 如果是 polygon → 轉成 bbox
    - 如果已經是 bbox → 保持原樣
    """
    txt_files = glob.glob(os.path.join(label_path, "*.txt"))

    print(f"找到 {len(txt_files)} 個標籤檔案，開始修正...")

    for file in txt_files:
        with open(file, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                # 格式錯誤或空檔案
                continue

            cls = parts[0]
            coords = list(map(float, parts[1:]))

            if len(coords) == 4:
                # 已經是 bbox (class xc yc w h)
                new_lines.append(line.strip())
            elif len(coords) >= 6 and len(coords) % 2 == 0:
                # polygon → 轉 bbox
                xc, yc, w, h = poly2bbox(coords)
                new_lines.append(f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
            else:
                print(f" 無法處理: {file}, line={line.strip()}")

        # 覆寫修正後的標籤
        with open(file, "w") as f:
            for l in new_lines:
                f.write(l + "\n")

    print("所有標籤已修正完成！")


if __name__ == "__main__":
    label_dir = r"C:\Users\user\Documents\yolov9\Carplatev9\train\labels"
    fix_labels(label_dir)
