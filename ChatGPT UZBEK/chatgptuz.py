import telebot
import google.generativeai as genai

# API kalitlar
BOT_TOKEN = "7625805271:AAG1oux0rAQjRE7R-UhvJ45Pum1bl8zw8lw"
GEMINI_API_KEY = "AIzaSyAQH97EwcO0RxKtIDOroOBl76yAel5A85E"

# Bot va AI modelni ishga tushirish
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Admin ID
ADMIN_ID = 907402803  # Sizning Telegram ID

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    user_id = message.chat.id
    user_link = f"[👤 User](tg://user?id={user_id})"
    
    try:
        # AI javobini olish
        response = model.generate_content(f"O‘zbek tilida lotinchda javob ber: {user_text}")
        reply_text = response.text if response and response.text else "Kechirasiz, javob topilmadi."
        
        # Foydalanuvchiga javob yuborish
        bot.send_message(user_id, reply_text)
        
        # Adminni xabardor qilish
        admin_message = (
            f"{user_link} yozdi:\n\n"
            f"📩 *Savol:* {user_text}\n\n"
            f"🤖 *Bot javobi:* {reply_text}"
        )
        bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
    
    except Exception as e:
        error_message = "Xatolik yuz berdi, keyinroq urinib ko‘ring."
        bot.send_message(user_id, error_message)
        bot.send_message(ADMIN_ID, f"⚠️ Xatolik: {str(e)}")

# Botni ishga tushirish
bot.polling(none_stop=True)