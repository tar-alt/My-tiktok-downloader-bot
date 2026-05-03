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
    # စာသားအသစ် ထည့်လိုက်တဲ့နေရာ
    wait_msg = bot.reply_to(message, "ခဏစောင့်ပေးပါ... Watermark မပါအောင်လုပ်ပေးမယ် ⏳")
    
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        video_url = response['data']['play']
        bot.send_video(message.chat.id, video_url)
        
        # ဗီဒီယိုပို့ပြီးရင် "ခဏစောင့်ပေးပါ" ဆိုတဲ့စာကို ပြန်ဖျက်ပေးမှာပါ
        bot.delete_message(message.chat.id, wait_msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, "Error! Link ကို ပြန်စစ်ပေးပါ။")

bot.polရှာနေပါတယ်တယ်
