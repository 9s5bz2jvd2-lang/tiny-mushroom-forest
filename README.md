# 🍄 Tiny Mushroom Forest

中文 | [English](#english)

一个轻量、可爱、透明的桌面小森林：每隔 5–15 秒，屏幕上会悄悄长出一朵彩色小蘑菇。蘑菇最多保留 20 朵，旧蘑菇会自动让位给新朋友。所有蘑菇都由 `QPainter` 绘制，不需要任何图片素材。

> 愿你的屏幕边角，也能长出一点点温柔的小生命。

## ✨ 功能

- Python 3.11+ / PySide6
- 透明、无边框、置顶 overlay
- 每 5–15 秒随机长出一朵蘑菇
- 最多 20 朵，超过后删除最早的一朵
- 红、橙、黄、绿、蓝、紫、粉随机颜色
- 10% → 100% 的 2 秒生长动画
- `ESC` 退出，系统托盘菜单也可退出
- 托盘菜单可手动 `Grow one mushroom`
- 蘑菇完全由代码绘制，无图片依赖

## 🚀 运行

```bash
git clone https://github.com/huangzesen/tiny-mushroom-forest.git
cd tiny-mushroom-forest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

> Windows 用户可将激活命令替换为：`.venv\\Scripts\\activate`

## 🧚 可爱的提示词（中文）

如果你想让 AI 帮你继续改造这个小项目，可以这样说：

> 请把这个桌面小蘑菇森林做得更可爱一点：保持轻量、透明、温柔，不要打扰用户工作。蘑菇要像悄悄从屏幕边角冒出来的小朋友，可以有柔和的颜色、轻微摇晃、可爱的名字、季节变化或小彩蛋。请优先保证代码简洁、可运行、无图片依赖，用 PySide6/QPainter 绘制，并保留 ESC 和系统托盘退出。

## 🌱 可以继续长出的点子

- 给每朵蘑菇随机名字
- 点击托盘菜单切换“雨后森林 / 星空森林 / 糖果森林”主题
- 加一点非常轻微的摇晃动画
- 按时间生成不同季节的蘑菇颜色
- 让蘑菇偶尔长出小小的发光孢子

## 📁 文件结构

```text
TinyMushroomForest/
├── main.py
├── mushroom.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 📴 退出

按 `ESC`，或在系统托盘图标菜单中选择 `Exit`。

## License

MIT

---

<a id="english"></a>

# 🍄 Tiny Mushroom Forest

A tiny, gentle, transparent desktop forest: every 5–15 seconds, a colorful little mushroom quietly grows on your screen. Up to 20 mushrooms are kept; the oldest one steps aside when a new friend appears. All mushrooms are drawn with `QPainter`, with no image assets required.

> May a small corner of your screen grow something soft and alive.

## ✨ Features

- Python 3.11+ / PySide6
- Transparent, frameless, always-on-top overlay
- A new mushroom grows every 5–15 seconds
- Keeps at most 20 mushrooms, removing the oldest one first
- Random red, orange, yellow, green, blue, purple, and pink caps
- 10% → 100% growth animation in 2 seconds
- Press `ESC` to exit, or use the system tray menu
- Tray menu includes `Grow one mushroom`
- Fully drawn in code; no image files needed

## 🚀 Run

```bash
git clone https://github.com/huangzesen/tiny-mushroom-forest.git
cd tiny-mushroom-forest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows, use `.venv\\Scripts\\activate` instead of the `source` command.

## 🧚 Cute prompt (English)

If you want an AI assistant to keep improving this project, try this prompt:

> Please make this tiny desktop mushroom forest even cuter while keeping it lightweight, transparent, gentle, and non-intrusive. The mushrooms should feel like shy little friends quietly growing from the corners of the screen. Add soft colors, subtle motion, cute names, seasonal variations, or tiny easter eggs if appropriate. Prioritize clean, runnable code with no image dependencies, draw everything with PySide6/QPainter, and keep both ESC and system-tray exit support.

## 🌱 Ideas for future sprouts

- Give each mushroom a random cute name
- Add tray-menu themes: “after-rain forest”, “starry forest”, “candy forest”
- Add a very subtle swaying animation
- Change colors by season or time of day
- Let mushrooms occasionally release tiny glowing spores

## 📴 Exit

Press `ESC`, or choose `Exit` from the system tray menu.

## License

MIT
