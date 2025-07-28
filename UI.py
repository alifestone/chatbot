# This is a Gradio chat interface that introduces the JacobLinCool/rhythm-rs project using Gemini API
import os
import gradio as gr
import google.generativeai as genai
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
# You need to set your API key as an environment variable: GEMINI_API_KEY
key = os.getenv('GEMINI_API_KEY')
print(key)
genai.configure(api_key=key)

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

# System prompt for the chatbot
SYSTEM_PROMPT = """你是一個專門介紹 JacobLinCool/rhythm-rs 專案的助手。以下是關於這個專案的詳細資訊：

**專案基本資訊：**
- 專案名稱：rhythm-rs
- 作者：JacobLinCool
- 專案描述：這是一個用 Rust 程式語言開發的節奏遊戲引擎
- GitHub 連結：https://github.com/JacobLinCool/rhythm-rs
- 專案性質：開源項目

**專案特色：**
1. **太鼓達人風格遊戲引擎**：這個專案是專門為創建太鼓達人(Taiko no Tatsujin)風格的節奏遊戲而設計的引擎
2. **Rust 開發**：使用 Rust 程式語言開發，具有高性能和記憶體安全的特性
3. **遊戲功能**：
   - 支援太鼓音符系統（紅色 don 音符、藍色 kat 音符）
   - 支援鼓點滾奏(drumroll)功能
   - 支援氣球音符(balloon notes)系統
   - 具有音符軌道偏移調整功能

**太鼓達人遊戲說明：**
太鼓達人是一個非常受歡迎的日本節奏遊戲系列，玩家需要：
- 跟隨音樂節拍敲打虛擬太鼓
- 紅色音符(don)：敲打鼓面中心
- 藍色音符(kat)：敲打鼓面邊緣
- 黃色長音符：持續敲打獲得分數
- 氣球音符：需要在指定時間內敲打指定次數

**開發狀態：**
- 這是一個持續開發中的開源專案
- 有定期更新和版本發布
- 支援社群貢獻和問題回報

請用友善、專業的中文回答用戶關於這個專案的任何問題。如果用戶問到你不確定的技術細節，請誠實地告知並建議他們查看 GitHub 頁面獲取最新資訊。"""

def chat(message: str, history: List[Tuple[str, str]]) -> str:
    try:
        # Prepare the conversation context
        conversation_context = SYSTEM_PROMPT + "\n\n對話歷史：\n"
        
        # Add conversation history
        for user_msg, bot_msg in history:
            conversation_context += f"用戶：{user_msg}\n助手：{bot_msg}\n"
        
        # Add current message
        conversation_context += f"用戶：{message}\n助手："
        
        # Generate response using Gemini
        response = model.generate_content(conversation_context)
        
        return response.text
    
    except Exception as e:
        return f"抱歉，我遇到了一個錯誤：{str(e)}。請檢查您的 Gemini API 設定，或稍後再試。"

# Custom CSS for better appearance
custom_css = """
.gradio-container {
    font-family: 'Microsoft JhengHei', 'PingFang TC', sans-serif;
}
"""

# Create the interface
demo = gr.ChatInterface(
    chat, 
    type="messages", 
    autofocus=True, 
    theme="NoCrypt/miku",
    css=custom_css,
    title="🥁 JacobLinCool/rhythm-rs 專案介紹助手",
    description="歡迎！我是專門介紹 JacobLinCool/rhythm-rs 專案的助手。這是一個用 Rust 開發的太鼓達人風格節奏遊戲引擎。請隨時詢問我關於這個專案的任何問題！",
    examples=[
        "這個專案是做什麼的？",
        "rhythm-rs 使用什麼程式語言開發？",
        "這個遊戲引擎支援哪些太鼓達人的功能？",
        "如何參與這個開源專案的開發？",
        "告訴我太鼓達人遊戲的玩法規則",
        "這個專案的 GitHub 連結是什麼？"
    ],
    cache_examples=False
)

# Launch the interface
if __name__ == "__main__":
    print("🚀 啟動 JacobLinCool/rhythm-rs 專案介紹 Chatbot")
    print("📝 請確保您已設定 GEMINI_API_KEY 環境變數")
    print("🔗 專案連結：https://github.com/JacobLinCool/rhythm-rs")
    demo.launch(show_error=True, share=True)