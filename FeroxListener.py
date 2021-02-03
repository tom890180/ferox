from telegram.ext import CommandHandler
from telegram.ext import Updater
from core.Config import Config
from core.MongoDB import DB
from core.Logger import Logger
import MotionDetectorThreadHandler
from SunAPI import SunAPI

class FeroxListener:
    def __init__(self):
        self.updater = Updater(token=Config().get()["Telegram"]["Token"], use_context=True)
        self.dispatcher = dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('subscribe', self.subscribe))
        dispatcher.add_handler(CommandHandler('unsubscribe', self.unsubscribe))

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('stop', self.stop))
        dispatcher.add_handler(CommandHandler('status', self.status))
        dispatcher.add_handler(CommandHandler('latest', self.latest))

        dispatcher.add_handler(CommandHandler('sun', self.sun))
        dispatcher.add_handler(CommandHandler('day', self.day))
        dispatcher.add_handler(CommandHandler('cache', self.cache))

        dispatcher.add_handler(CommandHandler('help', self.help))
        dispatcher.add_handler(CommandHandler('update', self.update))

    def update(self, update, context):
        import subprocess
        import sys
        subprocess.Popen("sleep 5 && sh %s &> %s" % (Config().get()['Updater']['Path'], Config().get()['Logger']['Path']), shell=True)
        sys.exit(0)

    def start_polling(self):
        Logger().logger.info("Started polling")
        self.updater.start_polling()

    def sun(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=SunAPI().data)

    def day(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Is day: %s" % SunAPI().isDay())

    def cache(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="CACHE KEY: %s" % SunAPI().cacheKey)

    def start(self, update, context):
        self.subscribe(update, context, False)
        MotionDetectorThreadHandler.MotionDetectorThreadHandler().startThread()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Started motion detector")

    def stop(self, update, context):
        MotionDetectorThreadHandler.MotionDetectorThreadHandler().killThread()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Stopped motion detector")

    def latest(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sending latest..")
        MotionDetectorThreadHandler.MotionDetectorThreadHandler().doSendLatest(update.effective_chat.id)

    def status(self, update, context):
        if MotionDetectorThreadHandler.MotionDetectorThreadHandler().is_alive():
            context.bot.send_message(chat_id=update.effective_chat.id, text="Motion detector is running")
        else: 
            context.bot.send_message(chat_id=update.effective_chat.id, text="Motion detector is not running")

    def subscribe(self, update, context, returnMessage=True):
        obj = DB().chats.find_one({"chat_id": update.effective_chat.id})

        if obj:
            if returnMessage:
                context.bot.send_message(chat_id=update.effective_chat.id, text="You are already subscribed to me.")
            return

        DB().chats.insert_one({
            "chat_id": update.effective_chat.id
        })

        if returnMessage:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You have subscribed to me!")

    def unsubscribe(self, update, context):
        DB().chats.find_one_and_delete({'chat_id': update.effective_chat.id})
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have unsubscribed from me.")

    def help(self, update, context):
        DB().chats.find_one_and_delete({'chat_id': update.effective_chat.id})
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        "/subscribe: Subscribe to me "          + "\n" +
        "/unsubscribe: Unsubscribe from me "    + "\n" +
        "/start: Start detecting motion "       + "\n" +
        "/stop: Stop detecting motion "         + "\n" +
        "/latest: Get latest image     "        + "\n" +
        "/sun: Get sun data     "               + "\n" +
        "/day: Check if day or night     "      + "\n" +
        "" +
        "")
