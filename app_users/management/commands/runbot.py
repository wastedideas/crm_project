from bot_notifier import bot
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Runs the bot'

    def handle(self, *args, **options):
        bot.polling(none_stop=True)
