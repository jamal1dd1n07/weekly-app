import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8262765329:AAH8UWW1uMcEsZRpa0rypPgWUDQjbAgvNkw"

# Bazaviy API URL (oxirida slesh bilan)
API_URL = "http://127.0.0.1:8000/"

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):   
    chat_id = message.chat.id
    user_data[chat_id] = {}

    try:
        # PING tekshiruvi: status 200 yoki 401/403 bo'lsa ham server yoniq deb hisoblaymiz
        response = requests.get(f"{API_URL}api/token/", timeout=5)
        
        markup = InlineKeyboardMarkup()
        r_button = InlineKeyboardButton(text="Ro'yxatdan o'tish", callback_data="register")
        l_button = InlineKeyboardButton(text="Akkauntga kirish", callback_data="login")
        markup.add(r_button, l_button)

        bot.send_message(
            chat_id, 
            "Assalomu alaykum! Weekly ilovasi botiga xush kelibsiz.\n\nDavom etish uchun tizimga kiring yoki ro'yxatdan o'ting:", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
            
    except requests.exceptions.ConnectionError:
        bot.send_message(chat_id, "❌ Django serveringiz yoqilmagan! Iltimos, `python manage.py runserver` ishlayotganini tekshiring.")

# ==================== LOGIN QISMI ====================

@bot.callback_query_handler(func=lambda call: call.data == 'login')
def login_start(call):
    chat_id = call.message.chat.id
    user_data[chat_id] = {'action': 'login'}

    bot.send_message(chat_id, "🔑 Akkauntga kirish.\n\n**Username**ingizni kiriting:", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, process_username)

def process_username(message):
    chat_id = message.chat.id
    user_data[chat_id]['username'] = message.text
    
    bot.send_message(chat_id, "🔒 **Parol**ingizni kiriting:", parse_mode="Markdown")
    bot.register_next_step_handler(message, process_password)

def process_password(message):
    chat_id = message.chat.id
    password = message.text
    user_data[chat_id]['password'] = password
    
    bot.send_message(chat_id, "⏳ Tizimga kirilmoqda...")
    
    payload = {
        "username": user_data[chat_id]['username'],
        "password": user_data[chat_id]['password']
    }
    
    try:
        # AYNAN SimpleJWT endpointiga yuboramiz: /api/token/
        response = requests.post(f"{API_URL}api/token/", json=payload, timeout=10)
        
        if response.status_code == 200:
            res_data = response.json()
            
            access_token = res_data.get('access')
            refresh_token = res_data.get('refresh')
            
            user_data[chat_id]['access_token'] = access_token
            user_data[chat_id]['refresh_token'] = refresh_token
            
            # Markdown parse xatosini oldini olish uchun f-string joylashuvi:
            success_msg = (
                f"🎉 *Muvaffaqiyatli tizimga kirdingiz!*\n\n"
                f"👤 *Username:* {user_data[chat_id]['username']}\n\n"
                f"🔑 *Access Token:*\n`{access_token}`"
            )
            
            bot.send_message(chat_id, success_msg, parse_mode="Markdown")
        
        elif response.status_code == 401:
            bot.send_message(chat_id, "❌ **401 Unauthorized:** Username yoki parol noto'g'ri!")
        else:
            errors = response.json()
            bot.send_message(chat_id, f"❌ Xatolik yuz berdi ({response.status_code}):\n`{errors}`", parse_mode="Markdown")
            
    except Exception as e:
        bot.send_message(chat_id, "❌ Django server bilan ulanishda xatolik yuz berdi!")
        print(f"API Error: {e}")

if __name__ == "__main__":
    print("Weekly Telegram Bot ishga tushdi...")
    bot.infinity_polling()