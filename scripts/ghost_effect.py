"""
重影头像效果生成器
将任意图片转换为"多重曝光/重影"风格
"""
from PIL import Image
import os
import sys


def ghost_effect(
    input_path: str,
    output_path: str,
    copies: int = 5,
    offset: int = 40,
    base_alpha: float = 0.35,
    direction: str = "right",
):
    """
    生成重影效果。

    参数：
        input_path: 输入图片路径
        output_path: 输出图片路径
        copies: 重影数量（含原图），推荐 4~6
        offset: 每层水平偏移像素，推荐 30~60
        base_alpha: 每层重影的基础透明度 (0~1)，推荐 0.3~0.5
        direction: "right" / "left" / "both"
    """
    src = Image.open(input_path).convert("RGBA")
    w, h = src.size

    # 画布：底层先铺一份原图
    canvas = src.copy()

    directions = []
    if direction in ("right", "both"):
        directions.append(1)
    if direction in ("left", "both"):
        directions.append(-1)

    for sign in directions:
        for i in range(1, copies):
            dx = sign * offset * i
            # 线性衰减透明度
            alpha = base_alpha * (1 - (i - 1) / copies)

            layer = src.copy()
            # 调整整层透明度
            a = layer.split()[3].point(lambda p, a=alpha: int(p * a))
            layer.putalpha(a)

            # 平移
            shifted = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            shifted.paste(layer, (dx, 0), layer)

            canvas = Image.alpha_composite(canvas, shifted)

    # 如果原图是 JPG，输出时转 RGB
    ext = os.path.splitext(output_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        bg = Image.new("RGB", canvas.size, (255, 255, 255))
        bg.paste(canvas, mask=canvas.split()[3])
        bg.save(output_path, quality=95)
    else:
        canvas.save(output_path)

    print(f"[OK] {input_path} -> {output_path}")


if __name__ == "__main__":
    # 命令行用法： python ghost_effect.py 输入.jpg 输出.jpg
    if len(sys.argv) >= 3:
        ghost_effect(sys.argv[1], sys.argv[2])
    else:
        # 默认：处理当前文件夹下的 1.jpg
        here = os.path.dirname(os.path.abspath(__file__))
        ghost_effect(
            os.path.join(here, "1.jpg"),
            os.path.join(here, "1_ghost.jpg"),
            copies=5,
            offset=45,
            base_alpha=0.4,
            direction="right",
        )
