import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Gemini ቅንብር
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

# የለቅሶ ትርጉም ተግባር
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    file_path = "baby_voice.ogg"
    await voice_file.download_to_drive(file_path)
    
    await update.message.reply_text("የልጁን ድምፅ እያዳመጥኩ ነው...")

    audio_file = genai.upload_file(path=file_path)
    prompt = "ይህ የህፃን ለቅሶ ድምፅ ነው። ለምን እንደሆነ (ርሀብ፣ እንቅልፍ፣ ህመም...) በአማርኛ በአጭሩ ተንትን።"
    response = model.generate_content([prompt, audio_file])
    
    await update.message.reply_text(response.text)

# Render እንዳይተኛ የሚያደርግ ትንሽ ሰርቨር
app = Flask('')
@app.route('/')
def home(): return "I am alive"

def run(): app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run).start()
    bot = ApplicationBuilder().token(os.environ['TELEGRAM_TOKEN']).build()
    bot.add_handler(MessageHandler(filters.VOICE, handle_voice))
    bot.run_polling()
