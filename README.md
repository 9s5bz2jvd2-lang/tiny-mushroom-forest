# 🍄 Tiny Mushroom Forest

中文 | [English](#english)

Tiny Mushroom Forest 是一片会偷偷住进你屏幕里的小蘑菇森林。它很轻、很安静、透明得像一层晨雾：每隔 5–15 秒，就会有一朵彩色小蘑菇从桌面角落悄悄冒头，像在说：今天也辛苦啦，给你长一点点可爱。

蘑菇最多保留 20 朵，旧朋友会轻轻让位给新朋友。所有蘑菇都由 `QPainter` 现场画出来，不需要任何图片素材。

> 给忙碌的桌面种一小片不会打扰人的森林。

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

## 🍄 介绍词（中文）

> 一片会悄悄长在桌面上的小蘑菇森林。
> 它不会吵你，也不会挡住你，只是在屏幕角落慢慢冒出彩色小蘑菇，陪你工作、发呆、写代码。
> 每一朵蘑菇都像一个安静的小朋友：轻轻出现，乖乖待着，把忙碌的电脑变成一点点温柔的森林。

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

Tiny Mushroom Forest is a tiny mushroom woodland that quietly moves into your desktop. It is lightweight, transparent, and gentle — like a layer of morning mist. Every 5–15 seconds, a colorful little mushroom shyly pops up from a corner of your screen, as if whispering: you worked hard today; here is a little bit of cute.

Up to 20 mushrooms are kept at a time, and older friends softly step aside for new ones. Every mushroom is drawn live with `QPainter`, with no image assets required.

> Plant a small, non-intrusive forest on your busy desktop.

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

## 🍄 Introduction copy (English)

> A tiny mushroom forest that quietly grows on your desktop.
> It does not interrupt you or cover your work — it simply lets colorful little mushrooms appear in the corners of your screen, keeping you company while you work, think, or code.
> Each mushroom feels like a shy little friend: softly arriving, calmly staying, and turning a busy computer into a gentler place.

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
