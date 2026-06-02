import telebot
from telebot import types
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# Загрузка информации об университете
university_info = ""
try:
    with open("files/university_info.txt", "r", encoding="utf-8") as file:
        university_info = file.read()
except FileNotFoundError:
    print("university_info.txt табылган жок!")

# Контекст пользователей
user_university_context = {}

def generate_gemini_response(prompt, context=None):
    """ Генерация ответа через Gemini API """
    try:
        full_prompt = f"Контекст:\n{context}\n\nПайдалануучунун суроосу: {prompt}" if context else prompt
        response = model.generate_content(full_prompt)
        return response.text if hasattr(response, 'text') else "Жоопту алуу мүмкүн эмес. ❌"
    except Exception as e:
        return f"Жоопту түзүүдө ката кетти: {str(e)} ❌"

@bot.message_handler(commands=['start'])
def start(message):
    """ Главное меню """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🏛 Университет жөнүндө маалымат")
    btn4 = types.KeyboardButton("📖 Гуманитардык илимдер")
    btn5 = types.KeyboardButton("🔬 Табигый-Так илимдер")
    markup.add(btn1, btn4, btn5)
    bot.send_message(message.chat.id, "Салам! 👋 Мен сага экзаменге даярданууга жардам берем! 🎯", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🏛 Университет жөнүндө маалымат")
def universitet_info(message):
    """ Включение режима контекста при вопросах об университете """
    user_university_context[message.chat.id] = "university"
    bot.send_message(message.chat.id, "Сизди университет жөнүндө эмне кызыктырат? Сурооңузду жазыңыз. 🏫💡")

@bot.message_handler(func=lambda message: message.text in ["📖 Гуманитардык илимдер", "🔬 Табигый-Так илимдер"])
def disable_context(message):
    """ Выключение контекста при выборе общего раздела наук """
    user_university_context[message.chat.id] = False
    if message.text == "📖 Гуманитардык илимдер":
        gum_ilimder(message)
    else:
        tabigyi_tak_ilimder(message)

@bot.message_handler(func=lambda message: message.text in ["📜 Кыргыз тили", "📚 Адабият", "🏛 Тарых", "🌍 География",
                                                            "🧮 Математика", "⚛ Физика", "🧬 Биология", "🧪 Химия"])
def subject_context(message):
    """ Включение контекста на 1 запрос при выборе предмета """
    user_university_context[message.chat.id] = "subject"
    bot.send_message(message.chat.id, f"Сиз {message.text} боюнча эмнени билгиңиз келет? 📚")

@bot.message_handler(func=lambda message: True)
def ai_response(message):
    """ Универсальный обработчик сообщений """
    chat_id = message.chat.id
    context_mode = user_university_context.get(chat_id, False)

    if context_mode == "university":
        response_text = generate_gemini_response(message.text, context=university_info)
    elif context_mode == "subject":
        response_text = generate_gemini_response(message.text, context=university_info)
        user_university_context[chat_id] = False  # Отключение контекста после 1 ответа
    else:
        response_text = generate_gemini_response(message.text)

    bot.send_message(chat_id, response_text)

@bot.message_handler(func=lambda message: message.text == "📖 Гуманитардык илимдер")
def gum_ilimder(message):
    """ Гуманитардык илимдердин тизмеси """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📜 Кыргыз тили", "📚 Адабият", "🏛 Тарых", "🌍 География")
    bot.send_message(message.chat.id, "Гуманитардык илимдерден тандаңыз: 📖", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔬 Табигый-Так илимдер")
def tabigyi_tak_ilimder(message):
    """ Табигый-Так илимдердин тизмеси """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🧮 Математика", "⚛ Физика", "🧬 Биология", "🧪 Химия")
    bot.send_message(message.chat.id, "Табигый-Так илимдерден тандаңыз: 🔬", reply_markup=markup)

bot.polling(none_stop=True)
