---
name: ghost-avatar
description: 把任意图像转成"重影/多重曝光"风格头像——主体水平错位复制多层并半透明叠加。当用户想对照片/头像做重影、多重曝光、ghost、double-exposure 效果时调用。支持整图偏移的简单模式，也支持用 rembg 抠出主体后只对主体做重影、背景保持干净的进阶模式；含批量处理脚本。
---

# ghost-avatar

生成"重影头像"效果的 Claude Code skill。

## 什么时候用

用户请求里出现以下任一意图时触发：

- "把这张图做成重影效果" / "重影头像" / "多重曝光"
- "ghost effect" / "double exposure" / "motion blur duplicate"
- 提供一张人物/头像图，要求"复制错位叠加"、"多个自己"、"多眼效果"

## 三个脚本，怎么选

| 场景 | 用 | 依赖 |
|---|---|---|
| 只想快速试效果，不在乎背景也有轻微重影 | `scripts/ghost_effect.py` | Pillow |
| 想让背景保持干净，只有主体重影（推荐） | `scripts/ghost_effect_pro.py` | Pillow + rembg + onnxruntime |
| 批量处理整个文件夹 | `scripts/batch_ghost.py` | 同上 |

## 使用流程

1. **确认依赖**：`pip install -r requirements.txt`
2. **默认参数跑一次**：`python scripts/ghost_effect_pro.py input.jpg output.jpg`
3. **看效果调参**：如果重影太弱，在脚本尾部调大这三项：
   - `copies` 4→6（层数）
   - `offset` 按图宽 5%→12%（偏移像素）
   - `base_alpha` 0.4→0.7（透明度）
4. **批量**：`python scripts/batch_ghost.py <输入文件夹> <输出文件夹>`

## 参数调节经验

- **卡通/描边风**的图，重影天然明显，offset 5% 就够
- **写实 AI 生成图**边缘柔和，需要加大到 10%+ 才看得清
- **浅色主体+深色背景**（或反之）重影最清楚；主体和背景反差小时效果弱
- rembg 首次运行会下载 ~180MB 模型文件到 `~/.u2net/`
- 非人像（猫、物品）用 `model="u2net"`；纯人像用 `model="u2net_human_seg"` 效果略好

## 目录

```
ghost-avatar/
├── SKILL.md                 # 本文件
├── README.md                # GitHub 展示说明
├── LICENSE                  # MIT
├── requirements.txt
├── scripts/
│   ├── ghost_effect.py      # 简单版（整图偏移）
│   ├── ghost_effect_pro.py  # 进阶版（抠主体+偏移）
│   └── batch_ghost.py       # 批量处理
└── examples/
    ├── before.jpg
    └── after.jpg
```
