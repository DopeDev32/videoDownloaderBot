import os
from dotenv import load_dotenv
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 Send me a link from Instagram, YouTube, TikTok, Twitter, Facebook, or Reddit!\n"
        "I'll fetch the video in best quality for you. 🚀"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *Help & Info*\n\n"
        "✅ Supported Platforms:\n"
        "• Instagram Reels\n"
        "• TikTok\n"
        "• YouTube\n"
        "• Twitter (X)\n"
        "• Facebook\n"
        "• Reddit\n\n"
        "⚠️ Limitations:\n"
        "• Max file size: 50MB (Telegram restriction)\n"
        "• Some very long videos may not work\n\n"
        "👉 Just send me a link — I’ll do the rest 🚀"
    )
    await update.message.reply_markdown(help_text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instructions = (
        "👋 Hi! I'm your Social Media Video Saver Bot.\n\n"
        "📌 How to use:\n"
        "1️⃣ Send me a video link (Instagram, TikTok, YouTube, Twitter, FB, Reddit).\n"
        "2️⃣ I’ll fetch it in best quality (≤50MB).\n"
        "3️⃣ You’ll get it back as MP4 🎥\n\n"
        "ℹ️ Type /help for more info."
    )
    await update.message.reply_text(instructions)


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "http" not in url:
        await update.message.reply_text("❌ Please send a valid video link.")
        return

    await update.message.reply_text("⏳ Downloading in best quality...")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "video.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        caption = f"🎬 {info.get('title', 'Unknown Title')}\n👤 {info.get('uploader', 'Unknown Author')}"

        # Ensure file is within Telegram limit
        if os.path.getsize(filename) <= 50 * 1024 * 1024:  # 50MB
            with open(filename, "rb") as video:
                await update.message.reply_video(video, caption=caption, timeout=180)
        else:
            await update.message.reply_text("⚠️ Video is too large for Telegram (50MB limit).")

        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    print("🤖 Bot running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
