import telebot
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Render မှာ Port Error မတက်အောင် Server အသေးလေးဖွင့်ပေးခြင်း
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Online')

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Server ကို နောက်ကွယ်မှာ Run ထားမယ်
threading.Thread(target=run_server, daemon=True).start()

# Bot ကုဒ်များ
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "TikTok Link ပို့ပေးပါ၊ Watermark မပါဘဲ ဒေါင်းပေးပါ့မယ်။")

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def handle_tiktok(message):
    url = message.text
    wait_msg = bot.reply_to(message, "ခဏစောင့်ပေးပါ... Watermark ဖျောက်ပေးမယ် ⏳")
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        video_url = response['data']['play']
        bot.send_video(message.chat.id, video_url)
        bot.delete_message(message.chat.id, wait_msg.message_id)
    except Exception as e:
        bot.reply_to(message, "Error! Link ကို ပြန်စစ်ပေးပါ။")

bot.polling()
