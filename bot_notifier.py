import os
import telebot
from crm_project.settings import load_dotenv
from app_users.models import Users

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = os.getenv('BOT_NAME')
bot = telebot.TeleBot(BOT_TOKEN)


def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


def in_storage(unique_code):
    return Users.objects.get(unique_code=unique_code)


def get_username_from_storage(unique_code):
    return Users.objects.get(unique_code=unique_code).username if in_storage(unique_code) else None


def save_chat_id(chat_id, username, unique_code):
    user_to_save = Users.objects.get(username=username, unique_code=unique_code)
    user_to_save.chat_id = chat_id
    user_to_save.save()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    unique_code = extract_unique_code(message.text)
    if unique_code:
        username = get_username_from_storage(unique_code)
        if username:
            save_chat_id(message.chat.id, username, unique_code)
            reply = "Hello {0}, how are you?".format(username)
        else:
            reply = "I have no clue who you are..."
    else:
        reply = "Please visit me via a provided URL from the website."
    bot.reply_to(message, reply)
