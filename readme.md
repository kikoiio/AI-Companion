# 🤖 AI Companion - Bocchi the Pi!

> 一个运行在树莓派上的个人AI伴侣，拥有可爱的Bocchi主题。她可以与你进行文字对话，并根据对话内容变换生动的表情。

这是一个充满乐趣的DIY项目，旨在将大型语言模型（LLM）与物理硬件相结合，创造一个独一无二的桌面互动伙伴。

![AI Companion Screenshot](./screenshot.png)
*(请将此处的 `screenshot.png` 替换为你自己程序的截图文件名)*

---

## ✨ 主要功能

*   **智能对话**: 基于 Google Gemini 1.5 Flash 模型，可以进行流畅、自然的中文和英文对话。
*   **动态表情**: AI会根据回复内容的情绪，自动选择并展示对应的表情贴纸，让对话更加生动。
*   **自定义界面**: 支持自定义背景图片和全套表情包，打造完全个性化的伴侣形象。
*   **记忆能力**: 能够记住之前的对话内容，进行有上下文的交流。

### 🚀 计划中的功能
*   **人脸识别**: 识别出主人，并加载专属的对话记忆。
*   **情绪感知**: 通过摄像头分析主人的面部表情，并作出相应的关怀和互动。
*   **应用控制**: 实现播放音乐等系统级操作。

---

## 🛠️ 技术栈

*   **硬件**: Raspberry Pi (树莓派)
*   **核心语言**: Python 3
*   **图形界面**: Pygame
*   **AI模型**: Google Gemini 1.5 Flash API
*   **版本控制**: Git & GitHub

---

## ⚙️ 安装与配置指南

想要在你的树莓派上运行自己的AI伴侣吗？请遵循以下步骤。

### 1. 先决条件

*   一台树莓派（推荐 Raspberry Pi 4B 或更高型号）。
*   树莓派操作系统（64位）。
*   一块显示屏。
*   一个Google AI API 密钥。你可以从 [Google AI Studio](https://aistudio.google.com/) 免费获取。

### 2. 克隆仓库

首先，将本仓库克隆到你的树莓派上。
```bash
git clone https://github.com/kikoiio/AI-Companion.git
cd AI-Companion
```
*(请将上面的 `kikoiio/AI-Companion` 替换为你自己的用户名和仓库名)*

### 3. 创建并激活虚拟环境

我们强烈建议使用虚拟环境来管理项目依赖，避免与系统库冲突。

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```
*(当你看到终端提示符前出现 `(venv)` 时，表示已成功激活)*

### 4. 安装依赖库

本项目的所有依赖都记录在 `requirements.txt` 文件中。

```bash
# 使用国内镜像源加速下载
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
*如果项目中还没有 `requirements.txt` 文件，请创建一个并填入以下内容：*
```
pygame
google-generativeai
```

### 5. 准备素材文件

你需要将自己的素材文件放到正确的目录下：
*   **背景图**: 将你的背景图片命名为 `background.jpg`，放在项目根目录下。
*   **表情包**: 将你的表情图片（`.jpg` 格式）全部放入 `expressions/` 文件夹。确保文件名与代码中的 `expression_files` 字典匹配（例如 `happy.jpg`, `sad.jpg` 等）。
*   **中文字体**: 下载一个支持中文的 `.otf` 或 `.ttf` 字体文件（例如[思源黑体](https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf)），将其命名为 `SourceHanSansSC-Regular.otf` 并放在项目根目录下。

### 6. 配置环境变量

在运行程序之前，你需要在终端中设置你的API密钥和网络代理（如果需要）。

```bash
# (如果在中国大陆访问) 设置网络代理，请将7890替换为你的代理端口
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"

# 设置你的Google AI API密钥
export GOOGLE_API_KEY='粘贴你以AIzaSy开头的API密钥'
```
**重要提示**: 每次新开一个终端窗口，都需要重新设置这些环境变量。

---

## 🚀 如何运行

完成以上所有配置后，运行以下命令即可启动你的AI伴侣！
```bash
python3 main.py
```
现在，开始和你的Bocchi聊天吧！

---

## 📜 许可证

本项目采用 [MIT License](LICENSE) 授权。
