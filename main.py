import telebot
import yt_dlp
import os
import threading
from flask import Flask

# --- إعدادات البوت ---
TOKEN = "8817861704:AAEb_ZmWWexvNS6EhCrty9shwFpVZYdRUtU"
bot = telebot.TeleBot(TOKEN)

# --- إعدادات الويب للبقاء نشطاً ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running..."

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web).start()

# --- دالة التحميل المطورة ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! أرسل رابط الفيديو وسأقوم بتنزيله لك فوراً.")

@bot.message_handler(func=lambda message: True)
def download(message):
    url = message.text
    if not url.startswith("http"):
        return
        
    msg = bot.reply_to(message, "⏳ جاري المعالجة... يرجى الانتظار.")
    
    # إعدادات متقدمة لتجاوز الحظر
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(id)s.%(ext)s',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل بنجاح!")
        
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء التحميل: {str(e)}")

print("Bot is ready...")
bot.polling(none_stop=True)
