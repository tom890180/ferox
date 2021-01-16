from telegram.ext import CommandHandler
from telegram.ext import Updater
from core.Config import Config
from core.MongoDB import DB
from core.Logger import Logger


class FeroxListener:
    def __init__(self):
        self.updater = Updater(token=Config().get()["Telegram"]["Token"], use_context=True)
        self.dispatcher = dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('end', self.end))

    def start_polling(self):
        Logger().logger.info("Started polling")
        self.updater.start_polling()

    def start(self, update, context):
        obj = DB().chats.find_one({"chat_id": update.effective_chat.id})

        if obj:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You are already subscribed to me.")
            return

        DB().chats.insert_one({
            "chat_id": update.effective_chat.id
        })

        context.bot.send_message(chat_id=update.effective_chat.id, text="You have subscribed to me!")

    def end(self, update, context):
        DB().chats.find_one_and_delete({'chat_id': update.effective_chat.id})
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have unsubscribed from me.")