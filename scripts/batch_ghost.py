"""
批量重影：处理一个文件夹里的所有图片
"""
from PIL import Image
from rembg import remove, new_session
import os
import sys

SUPPORTED = (".jpg", ".jpeg", ".png", ".webp", ".bmp")


def ghost_effect_pro(
    src: Image.Image,
    subject: Image.Image,
    copies: int = 5,
    offset: int = None,
    base_alpha: float = 0.7,
    direction: str = "right",
) -> Image.Image:
    w, h = src.size
    # 偏移按图宽自适应（约占宽度 12%）
    if offset is None:
        offset = max(20, int(w * 0.12))

    canvas = src.copy()

    directions = []
    if direction in ("right", "both"):
        directions.append(1)
    if direction in ("left", "both"):
        directions.append(-1)

    for sign in directions:
        for i in range(copies - 1, 0, -1):
            dx = sign * offset * i
            alpha = base_alpha * (1 - (i - 1) / copies)

            layer = subject.copy()
            a = layer.split()[3].point(lambda p, a=alpha: int(p * a))
            layer.putalpha(a)

            shifted = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            shifted.paste(layer, (dx, 0), layer)
            canvas = Image.alpha_composite(canvas, shifted)

    canvas = Image.alpha_composite(canvas, subject)
    return canvas


def save_image(img: Image.Image, out_path: str):
    ext = os.path.splitext(out_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        bg.save(out_path, quality=95)
    else:
        img.save(out_path)


def batch(in_dir: str, out_dir: str, model: str = "u2net"):
    os.makedirs(out_dir, exist_ok=True)
    session = new_session(model)

    files = sorted(
        f for f in os.listdir(in_dir)
        if f.lower().endswith(SUPPORTED)
    )
    print(f"找到 {len(files)} 张图片")

    for i, name in enumerate(files, 1):
        in_path = os.path.join(in_dir, name)
        stem, ext = os.path.splitext(name)
        # 统一用简洁编号命名，避免中文长文件名
        out_name = f"ghost_{i:02d}.png"
        out_path = os.path.join(out_dir, out_name)

        try:
            src = Image.open(in_path).convert("RGBA")
            subject = remove(src, session=session)
            result = ghost_effect_pro(src, subject)
            save_image(result, out_path)
            print(f"[{i}/{len(files)}] {name} -> {out_name}")
        except Exception as e:
            print(f"[{i}/{len(files)}] {name} 失败: {e}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    in_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "新建文件夹")
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "ghost_output")
    batch(in_dir, out_dir)
