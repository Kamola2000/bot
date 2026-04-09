import os

from telegram import Update
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CommandHandler
import instaloader
import re


TOKEN='8693569858:AAHGC0XfbsMpWoMpNUlu7oY2RUmaB8DAj3M'

L = instaloader.Instaloader(
    save_metadata=False,
    download_geotags=False,
    download_comments=False,


)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Salom men Kamola yaratgan botman va '
                              'sizga instagramdan video olib beraman 😊')

def short_cut(url:str):
    march = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?]+)",url)
    return march.group(1) if march else None


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if "instagram.com" not in text:
        update.message.reply_text('link notogri')
        return
    shortcode = short_cut(text)
    if not shortcode:
        update.message.reply_text('link notogri')
        return

    try:
        update.message.reply_text("video yuklanmoqda.....")

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target="download")

        for file in os.listdir("download"):
            if file.endswith(".mp4"):
                path = f'download/{file}'
                update.message.reply_video(video=open(path, "rb"))
                os.remove(path)
        update.message.reply_text("Tayyor\n"
                                  "botdan foydalanganingiz uchun rahmat 😉")


    except Exception as e:
        update.message.reply_text("Video olishda xatolik! ")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()











