import random
import time
import threading
import telebot
from password_logic import gen_pass

bot = telebot.TeleBot("8099630029:AAHxCgxpsFbRb3ay79WUZwceYvoWkXNI55k")

user_states = {}

reminders = {}

def send_reminder(chat_id, stop_event):
    while not stop_event.is_set():
        time.sleep(5)  # Напоминание каждый час
        bot.send_message(chat_id, "Это ваше напоминание!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Telegram бот. Я отвечаю на много вопросов. Вот мои командды: /hello , /bye , /password , /globalwarming , /calculator, "
    "/remind .")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    user_states[message.chat.id] = 'waiting_for_feedback'  

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == 'waiting_for_feedback')
def handle_response(message):
    if message.text.lower() == "хорошо":
        bot.reply_to(message, "Очень хорошо слышать")
        user_states.pop(message.chat.id)  
    else:
        bot.reply_to(message, "ивините я не понимаю что вы говорите, напишите хорошо или плохо.")

    if message.text.lower() == "плохо":
        bot.reply_to(message, "Извинте, это очень грустно слышать")
        user_states.pop(message.chat.id)
    else:
        bot.reply_to(message, "ивините я не понимаю что вы говорите, напишите хорошо или плохо.")

@bot.message_handler(commands=['bye'])
def send_bye(message):

    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['password'])
def gen_password(message):
    bot.reply_to(message,  gen_pass(10))

@bot.message_handler(commands=['globalwarming'])
def send_globalwarming(message):
    bot.reply_to(message, ("По прогнозам Всемирной метеорологической организации (ВМО), в период с 2025 по 2029 год "
                  "глобальная среднегодовая температура будет на 1,2–1,9 градуса Цельсия выше доиндустриального уровня (1850–1900 годы). "
                  "Существует восьмидесятипроцентная вероятность того, что по крайней мере один год в этот период будет теплее, чем самый тёплый год за всю историю наблюдений — 2024-й. "
                  "Некоторые последствия глобального потепления: более интенсивные волны жары; экстремальные осадки; сильная засуха; таяние ледников; нагревание океана и повышение уровня моря. "
                  "Учёные предупреждают, что в 2025 году и последующих годах экстремальные погодные явления начнут происходить ещё чаще. "
                  "По мнению научного руководителя Гидрометцентра России Романа Вильфанда, существует вероятность, что 2025 год войдёт в пятёрку самых тёплых."))

@bot.message_handler(commands=['remind'])
def start_reminder(message):
    chat_id = message.chat.id
    if chat_id not in reminders:
        stop_event = threading.Event()
        reminders[chat_id] = stop_event
        threading.Thread(target=send_reminder, args=(chat_id, stop_event)).start()
        bot.reply_to(message, "Начинаю отправлять напоминания каждый часб напишите /stop и после след. напоминания оно прикратится.")
    else:
        bot.reply_to(message, "Напоминания уже запущены.")

@bot.message_handler(commands=['stop'])
def stop_reminder(message):
    chat_id = message.chat.id
    if chat_id in reminders:
        reminders[chat_id].set()  
        del reminders[chat_id]  
        bot.reply_to(message, "Остановил отправку напоминаний, сейчас придёт последние и оно остановится.")
    else:
        bot.reply_to(message, "Напоминания не запущены.")


@bot.message_handler(commands=['calculator'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела? я могу быть калькулятором, напишите пример")

@bot.message_handler(func=lambda message: True)  
def calculate(message):
    """Выполняет вычисление и отправляет результат."""
    try:
        expression = message.text
        result = eval(expression)   
        bot.reply_to(message, f"Результат: {result}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")
        bot.reply_to(message, f"напишите число, боту не нравятся обычные слова")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()