# ghost-avatar

把任意图像转成"重影/多重曝光"风格的小工具。也是一个 Claude Code Skill。

## 安装

```bash
git clone https://github.com/Qiuuc/ghost-avatar.git
cd ghost-avatar
pip install -r requirements.txt
```

## 用法

```bash
# 简单版（只依赖 Pillow）
python scripts/ghost_effect.py input.jpg output.jpg

# 进阶版（抠出主体，背景保持干净，推荐）
python scripts/ghost_effect_pro.py input.jpg output.jpg

# 批量处理整个文件夹
python scripts/batch_ghost.py 输入文件夹 输出文件夹
```

## 参数

在脚本末尾调整：

| 参数 | 说明 | 推荐范围 |
|---|---|---|
| `copies` | 重影层数 | 4–6 |
| `offset` | 每层水平偏移像素 | 30–60 |
| `base_alpha` | 重影透明度 | 0.35–0.7 |
| `direction` | `right` / `left` / `both` | — |

## License

[MIT](LICENSE) © [Qiuuc](https://github.com/Qiuuc)
