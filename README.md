# 小武侠传说 · 无尽武道篇

一款基于 Kivy 的跨平台武侠 RPG 单机游戏，支持 Android / Windows / Linux。

## 🎮 游戏特色

- **24位金庸侠客**：张无忌、令狐冲、乔峰、杨过、郭靖、黄蓉、小龙女等
- **39种武学**：降龙掌法、独孤九剑、九阳神功、太玄经等，橙/紫/蓝三档稀有度
- **元宝商城**：5大分类23种商品，打怪随机掉落元宝
- **经脉系统**：8条经脉，打通永久加成，全通额外+40%
- **悟性系统**：每点+1%全属性，无上限
- **装备精铸**：每级+10%属性，无上限
- **挑战塔**：无限楼层，每5层紫装、每10层大礼包
- **New Game+**：通关后轮回，全队属性永久+10%，可无限叠加
- **4档难度**：简单/普通/困难/地狱，影响经验/银两/元宝/极品率
- **三结局**：侠之大者 / 一代魔尊 / 逍遥散人

## 📱 Android 打包（GitHub Actions 自动构建）

推送代码到 `main` 分支后，GitHub Actions 会自动：
1. 安装 Python 3.10 + Buildozer + Cython
2. 安装 Android SDK/NDK/JDK
3. 编译生成 APK
4. 上传 APK 为 Artifact（保留30天）

### 手动触发
进入 GitHub 仓库 → Actions → "Build Android APK" → Run workflow

## 🖥️ 本地运行

```bash
pip install kivy==2.3.1
python main.py
```

## 📂 项目结构

```
xiawuxia_kivy/
├── main.py                    # 游戏全部源码（1496行）
├── buildozer.spec             # Android 打包配置
├── icon.png                   # 游戏图标
├── requirements.txt           # Python 依赖
├── .github/workflows/         # GitHub Actions 自动打包
└── README.md
```

## 🛠️ 本地打包 APK

```bash
pip install buildozer cython==0.29.37
sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool \
  pkg-config zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev

buildozer android debug
# 输出: bin/小武侠传说-1.0-debug.apk
```

## 📋 系统要求

- **Android**: 6.0+ (API 23+)
- **Windows**: Python 3.10+ / 直接运行 .py
- **Linux**: Python 3.10+ / 直接运行 .py

## ⚖️ 声明

本游戏为同人致敬作品，所有金庸人物名称仅作彩蛋致敬，游戏剧情、数值、系统均为原创设计。
