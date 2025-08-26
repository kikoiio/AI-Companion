# -------------------- 导入必要的库 --------------------
import pygame
import google.generativeai as genai
import os
import textwrap
import threading

# -------------------- 1. 初始化和全局设置 --------------------

pygame.init()

# ---- API 设置 ----
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
genai.configure(api_key=api_key)

# ---- 屏幕和布局设置 ----
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Companion")

# 布局常量
PADDING = 15
INPUT_BOX_HEIGHT = 40
STICKER_SIZE = (80, 80)

# ---- 颜色和字体定义 ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INPUT_BOX_COLOR = (220, 220, 220, 200)
TEXT_COLOR = WHITE
OUTLINE_COLOR = BLACK

# ## <-- 修改点: 指定加载我们下载的中文字体文件
try:
    FONT_NAME = "SourceHanSansSC-Regular.otf" # 确保这个文件和main.py在同一个文件夹
    font = pygame.font.Font(FONT_NAME, 32)
    chat_font = pygame.font.Font(FONT_NAME, 24) # 聊天字体可以稍微小一点，效果更好
except FileNotFoundError:
    print(f"警告: 字体文件 {FONT_NAME} 未找到，将使用默认字体。中文可能无法显示。")
    font = pygame.font.Font(None, 32)
    chat_font = pygame.font.Font(None, 28)

# -------------------- 2. 加载资源与状态变量 --------------------

# (后面的代码和上一版完全一样，无需改动)
# ... 省略 ...

# (此处省略和上一版完全相同的代码，你只需修改上面字体部分即可)
# 为了完整性，下面也全部贴出

# ---- 加载图片资源 ----
try:
    background_image = pygame.image.load("background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("警告: background.jpg 未找到。将使用纯黑背景。")
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.fill(BLACK)

expression_stickers = {}
expression_files = {
    'neutral': 'expressions/neutral.jpg', 'happy': 'expressions/happy.jpg',
    'sad': 'expressions/sad.jpg', 'thinking': 'expressions/thinking.jpg',
}
for name, path in expression_files.items():
    try:
        img = pygame.image.load(path).convert()
        expression_stickers[name] = pygame.transform.scale(img, STICKER_SIZE)
    except pygame.error:
        print(f"警告: {path} 未找到。将跳过这个表情。")

# ---- 程序状态变量 ----
input_text = ""
chat_history = []
is_ai_thinking = False
ai_reply_data = None

# -------------------- 3. 辅助与核心功能函数 --------------------

def draw_text_with_outline(surface, text, font_obj, pos, text_color, outline_color):
    """在文字周围绘制一圈轮廓，使其更清晰"""
    x, y = pos
    text_surface = font_obj.render(text, True, outline_color)
    surface.blit(text_surface, (x-1, y-1))
    surface.blit(text_surface, (x+1, y-1))
    surface.blit(text_surface, (x-1, y+1))
    surface.blit(text_surface, (x+1, y+1))
    text_surface = font_obj.render(text, True, text_color)
    surface.blit(text_surface, (x, y))

def get_ai_response_worker(history):
    """在后台线程中调用AI，返回包含内容和表情的字典"""
    global is_ai_thinking, ai_reply_data
    system_prompt = (
        "你是一个AI伴侶，名字叫Bocchi。请用简短、口语化的方式回答问题。"
        "在你的回答之后，请必须从以下列表中选择一个最能代表你回答情绪的词："
        "[happy, sad, thinking, neutral]，并以'EMOTION:词'的格式附加在新的一行。"
    )
    gemini_history = [{'role': m['role'] if m['role']=='user' else 'model', 'parts': [m['content']]} for m in history]
    try:
        print("正在向 Google AI 发送请求...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        chat = model.start_chat(history=[{'role': 'user', 'parts': [system_prompt]}, {'role': 'model', 'parts': ["好的。"]}])
        response = chat.send_message(gemini_history[-1]['parts'][0])
        full_response = response.text
        print(f"从 Google AI 收到回复: {full_response}")
        ai_message, new_emotion = full_response, 'neutral'
        if "\nEMOTION:" in full_response:
            parts = full_response.split("\nEMOTION:")
            ai_message = parts[0].strip()
            emotion_tag = parts[1].strip()
            if emotion_tag in expression_stickers: new_emotion = emotion_tag
        ai_reply_data = {'content': ai_message, 'expression': new_emotion}
    except Exception as e:
        print(f"!!! 调用 Google AI 时发生严重错误: {e} !!!")
        ai_reply_data = {'content': "抱歉，我的大脑好像短路了...", 'expression': 'sad'}
    finally:
        is_ai_thinking = False

# -------------------- 4. 游戏主循环 --------------------

running = True
while running:
    # --- 4.1 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if not is_ai_thinking:
                if event.key == pygame.K_RETURN:
                    if input_text:
                        chat_history.append({"role": "user", "content": input_text})
                        is_ai_thinking = True
                        ai_thread = threading.Thread(target=get_ai_response_worker, args=(chat_history,))
                        ai_thread.start()
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
                else: input_text += event.unicode
    
    if ai_reply_data is not None:
        new_message = {'role': 'assistant'}
        new_message.update(ai_reply_data)
        chat_history.append(new_message)
        ai_reply_data = None

    # --- 4.2 绘制界面 ---
    screen.blit(background_image, (0, 0))

    y_cursor = SCREEN_HEIGHT - INPUT_BOX_HEIGHT - PADDING * 2
    for message in reversed(chat_history):
        wrapped_text = textwrap.wrap(message['content'], width=40)
        for i, line in enumerate(reversed(wrapped_text)):
            line_height = chat_font.get_linesize()
            draw_text_with_outline(screen, line, chat_font, (PADDING, y_cursor - line_height), TEXT_COLOR, OUTLINE_COLOR)
            y_cursor -= line_height
        if message['role'] == 'assistant' and 'expression' in message:
            sticker = expression_stickers.get(message['expression'])
            if sticker:
                y_cursor -= STICKER_SIZE[1]
                screen.blit(sticker, (PADDING, y_cursor))
        y_cursor -= PADDING
        if y_cursor < 0:
            break

    input_box_surface = pygame.Surface((SCREEN_WIDTH, INPUT_BOX_HEIGHT + PADDING), pygame.SRCALPHA)
    input_box_surface.fill(INPUT_BOX_COLOR)
    screen.blit(input_box_surface, (0, SCREEN_HEIGHT - INPUT_BOX_HEIGHT - PADDING))
    draw_text_with_outline(screen, "> " + input_text, font, (PADDING, SCREEN_HEIGHT - INPUT_BOX_HEIGHT - 2), WHITE, BLACK)

    if is_ai_thinking:
        thinking_text = "Thinking..."
        text_w, text_h = font.size(thinking_text)
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        box_rect = pygame.Rect(center_x - text_w//2 - PADDING, center_y - text_h//2 - PADDING, text_w + PADDING*2, text_h + PADDING*2)
        pygame.draw.rect(screen, (0,0,0,150), box_rect, border_radius=10)
        draw_text_with_outline(screen, thinking_text, font, (center_x - text_w//2, center_y - text_h//2), WHITE, BLACK)

    # --- 4.3 更新屏幕 ---
    pygame.display.flip()

# -------------------- 5. 退出程序 --------------------
pygame.quit()
