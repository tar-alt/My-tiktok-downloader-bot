import telebot
import requests
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "TikTok Link ပို့ပေးပါ၊ Watermark မပါဘဲ ဒေါင်းပေးပါ့မယ်။")

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def handle_tiktok(message):
    url = message.text
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        video_url = response['data']['play']
        bot.send_video(message.chat.id, video_url)
    except:
        bot.reply_to(message, "Error! Link ကို ပြန်စစ်ပေးပါ။")

bot.polling()
