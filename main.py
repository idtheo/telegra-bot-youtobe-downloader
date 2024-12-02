from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

BOT_TOKEN = ''

# دستور /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! لینک یوتیوب خود را ارسال کنید تا آن را دانلود کنم.")

# هندلر دانلود ویدیو
def download_video(update: Update, context: CallbackContext):
    link = update.message.text
    if "youtube.com" in link or "youtu.be" in link:
        update.message.reply_text("در حال دانلود ویدیو...")
        try:
            # دانلود ویدیو با yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.%(ext)s',
                'noplaylist': True,  # فقط یک ویدیو دانلود شود
                'restrictfilenames': True,  # جلوگیری از نام‌های طولانی
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # اضافه کردن user-agent
                'socket_timeout': 60,  # افزایش زمان تایم‌اوت (60 ثانیه)
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            video_file = "video.mp4"
            if os.path.exists(video_file):
                update.message.reply_text("دانلود تکمیل شد! در حال ارسال...")
                update.message.reply_video(video=open(video_file, 'rb'))
                os.remove(video_file)  # حذف فایل پس از ارسال
            else:
                update.message.reply_text("مشکلی پیش آمد و ویدیو پیدا نشد.")
        except Exception as e:
            update.message.reply_text(f"خطا در دانلود: {e}")
    else:
        update.message.reply_text("لینک یوتیوب معتبر ارسال کنید.")

# تابع اصلی
def main():
    # ساخت Updater
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # افزودن هندلرها
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # اجرا
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
