"""
重影头像效果（进阶版）
抠出人物后，只对人物做水平重影，背景保持干净。
"""
from PIL import Image
from rembg import remove, new_session
import os
import sys


def ghost_effect_pro(
    input_path: str,
    output_path: str,
    copies: int = 5,
    offset: int = 45,
    base_alpha: float = 0.45,
    direction: str = "right",
    model: str = "u2net",
):
    """
    参数：
        input_path:  输入图片
        output_path: 输出图片
        copies:      重影层数（含原图主体），推荐 4~6
        offset:      每层水平偏移像素，推荐 30~60
        base_alpha:  重影层透明度，推荐 0.35~0.55
        direction:   "right" / "left" / "both"
        model:       rembg 模型名，人像可用 "u2net_human_seg"
    """
    src = Image.open(input_path).convert("RGBA")
    w, h = src.size

    # 1) 抠图：拿到只含主体的 RGBA 图
    session = new_session(model)
    subject = remove(src, session=session)  # 背景已透明

    # 2) 背景层：用原图（被主体遮挡的部分会被覆盖）
    canvas = src.copy()

    directions = []
    if direction in ("right", "both"):
        directions.append(1)
    if direction in ("left", "both"):
        directions.append(-1)

    # 3) 先叠偏移后的重影（从远到近），再把原始主体放最上层
    for sign in directions:
        # i 从大到小：远处的先画，近处的后画（更自然）
        for i in range(copies - 1, 0, -1):
            dx = sign * offset * i
            alpha = base_alpha * (1 - (i - 1) / copies)

            layer = subject.copy()
            a = layer.split()[3].point(lambda p, a=alpha: int(p * a))
            layer.putalpha(a)

            shifted = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            shifted.paste(layer, (dx, 0), layer)
            canvas = Image.alpha_composite(canvas, shifted)

    # 最后把原始主体（不透明）盖在最上面，保证主体清晰
    canvas = Image.alpha_composite(canvas, subject)

    ext = os.path.splitext(output_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        bg = Image.new("RGB", canvas.size, (255, 255, 255))
        bg.paste(canvas, mask=canvas.split()[3])
        bg.save(output_path, quality=95)
    else:
        canvas.save(output_path)

    print(f"[OK] {input_path} -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        ghost_effect_pro(sys.argv[1], sys.argv[2])
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        ghost_effect_pro(
            os.path.join(here, "1.jpg"),
            os.path.join(here, "1_ghost_pro.jpg"),
            copies=5,
            offset=45,
            base_alpha=0.45,
            direction="right",
            model="u2net_human_seg",  # 专门的人像模型
        )
