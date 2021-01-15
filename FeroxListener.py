from telegram.ext import CommandHandler
from telegram.ext import Updater


class FeroxListener:
    def __init__(self, token, db, logger):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = dispatcher = self.updater.dispatcher
        self.db = db
        self.logger = logger

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('end', self.end))

    def start_polling(self):
        self.logger.info("Started polling")
        self.updater.start_polling()

    def start(self, update, context):
        obj = self.db.chats.find_one({"chat_id": update.effective_chat.id})

        if obj:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You are already subscribed to me.")
            return

        self.db.chats.insert_one({
            "chat_id": update.effective_chat.id
        })

        context.bot.send_message(chat_id=update.effective_chat.id, text="You have subscribed to me!")

    def end(self, update, context):
        self.db.chats.find_one_and_delete({'chat_id': update.effective_chat.id})
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have unsubscribed from me.")