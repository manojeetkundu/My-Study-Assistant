import os
from flask import Flask

# Ek chhota dummy server banana taaki Render ka port check pass ho jaye
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Isse server alag thread mein chalega aur bot bhi kaam karega
import threading
t = threading.Thread(target=run_web)
t.start()
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Logging setup karna taaki errors track ho sakein
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Apni Gemini API Key yahan dalein
genai.configure(api_key="AQ.Ab8RN6LSNsVpQt8Tnj0X9bT5RIW7z5gt9FTeoBpiIhTQc3TiqQ")

# Model configuration (Gemini 1.5 Flash fast aur efficient hai)
generation_config = {
    "temperature": 0.7,
}
safety_settings = []

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# System prompt taaki bot Hinglish, Hindi aur English mein achhe se jawab de
SYSTEM_INSTRUCTION = """
Aap ek helpful AI study assistant hain jo students ke doubts clear karte hain. 
Aapko user ki bhasha ke hisaab se jawab dena hai:
- Agar user Hinglish mein baat kare, toh aap Hinglish mein hi reply karein.
- Agar user Shuddh Hindi mein sawaal pooche, toh Hindi (Devanagari script) mein reply karein.
- Agar user English mein pooche, toh English mein reply karein.
Jawab hamesha clear, accurate aur aasan bhasha mein hone chahiye.
"""

# Chat session start karna with instructions
chat = model.start_chat(history=[])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        # Prompt ke sath system instruction combine karna
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Doubt: {user_message}"
        
        # Gemini AI se response lena
        response = model.generate_content(full_prompt)
        reply_text = response.text
        
        # Telegram par user ko reply bhejna
        await update.message.reply_text(reply_text)
        
    except Exception as e:
        await update.message.reply_text("Maaf kijiye, kuch technical problem aa gayi hai. Kripya thodi der baad try karein.")

if __name__ == '__main__':
    TOKEN = "9150760320:AAEjrTAJOKuHIUhUn7hNblvzaZA-M0wbElg"

    application = ApplicationBuilder().token(TOKEN).build()

    # Error handler register karein
    application.add_error_handler(error_handler)

    # Message handler
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    print("Bot shuru ho gaya hai...")
    application.run_polling()
