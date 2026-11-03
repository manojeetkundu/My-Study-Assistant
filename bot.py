import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Logging setup karna
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Apni Gemini API Key yahan dalein
genai.configure(api_key="AQ.Ab8RN6LSNsVpQt8Tnj0X9bT5RIW7z5gt9FTeoBpiIhTQc3TiqQ")

generation_config = {
    "temperature": 0.7,
}
safety_settings = []

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

SYSTEM_INSTRUCTION = """
Aap ek helpful AI study assistant hain jo students ke doubts clear karte hain. 
Aapko user ki bhasha ke hisaab se jawab dena hai:
- Agar user Hinglish mein baat kare, toh aap Hinglish mein hi reply karein.
- Agar user Shuddh Hindi mein sawaal pooche, toh Hindi (Devanagari script) mein reply karein.
- Agar user English mein pooche, toh English mein reply karein.
Jawab hamesha clear, accurate aur aasan bhasha mein hone chahiye.
"""

chat = model.start_chat(history=[])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Doubt: {user_message}"
        response = model.generate_content(full_prompt)
        reply_text = response.text
        
        await update.message.reply_text(reply_text)
        
    except Exception as e:
        await update.message.reply_text("Maaf kijiye, kuch technical problem aa gayi hai. Kripya thodi der baad try karein.")

# Error Handler function (Pehle yeh define hoga)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error("Exception while handling an update:", exc_info=context.error)

if __name__ == '__main__':
    # 2. Apna Telegram Bot Token yahan dalein
    TOKEN = "9150760320:AAEjrTAJOKuHIUhUn7hNblvzaZA-M0wbElg"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Error handler register karna
    application.add_error_handler(error_handler)
    
    # Message handler lagana
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("Bot shuru ho gaya hai... (Running)")
    application.run_polling()
