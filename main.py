import telebot
import yt_dlp
import os
import threading
from flask import Flask, render_template_string

# --- إعدادات البوت ---
TOKEN = "8817861704:AAEb_ZmWWexvNS6EhCrty9shwFpVZYdRUtU"
bot = telebot.TeleBot(TOKEN)

# --- لوحة التحكم ويب ---
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>Bot Dashboard Active</h1><p>The downloader bot is running smoothly.</p>"

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web).start()

# --- دوال البوت ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً! أرسل لي رابط أي فيديو (يوتيوب، تيك توك، إلخ) وسأقوم بتنزيله لك فوراً.")

@bot.message_handler(func=lambda message: True)
def download(message):
    url = message.text
    if not url.startswith("http"):
        return
        
    msg = bot.reply_to(message, "⏳ جاري المعالجة والتحميل... يرجى الانتظار.")
    
    try:
        ydl_opts = {'format': 'best', 'outtmpl': '%(id)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل بنجاح!")
        
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

bot.polling(none_stop=True)
