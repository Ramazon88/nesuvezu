from django.core.management import BaseCommand

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config.settings import NESU_TOKEN
from nesu.views import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater(NESU_TOKEN)
        updater.dispatcher.add_handler(CommandHandler(command='start', callback=start, filters=Filters.chat_type.private))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.location & Filters.chat_type.private, callback=order))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.all & Filters.chat_type.private, callback=order))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback))
        updater.start_polling()
        updater.idle()
