import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===================== SOZLAMALAR =====================
BOT_TOKEN = "8810033706:AAEgroZ5E-wENwywytdwg70OFi_gWTiUVYU"
ADMIN_IDS = [7771521469]

# ===================== KINO BAZASI =====================
# Format: "KOD": {"nomi": "...", "link": "..."}
# Yoki fayl yuborish uchun: "file_id": "Telegram file_id"
movies = {
    "1001": {
        "nomi": "Avengers: Endgame",
        "link": "https://t.me/kino_kanal/123",  # yoki file_id
    },
    "1002": {
        "nomi": "Inception",
        "link": "https://t.me/kino_kanal/456",
    },
    "1003": {
        "nomi": "Interstellar",
        "link": "https://t.me/kino_kanal/789",
    },
}

# ===================== LOGGING =====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ===================== BUYRUQLAR =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botni ishga tushirish"""
    await update.message.reply_text(
        "🎬 *Kino Botga Xush Kelibsiz!*\n\n"
        "Kino kodini yuboring va filmni oling.\n\n"
        "📋 Mavjud kinolar ro'yxati: /list\n"
        "❓ Yordam: /help",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam"""
    text = (
        "ℹ️ *Foydalanish yo'riqnomasi:*\n\n"
        "1️⃣ Kino kodini yuboring (masalan: `1001`)\n"
        "2️⃣ Bot sizga kino linkini yuboradi\n\n"
        "📋 /list — barcha kinolar ro'yxati\n"
    )
    if update.effective_user.id in ADMIN_IDS:
        text += (
            "\n👨‍💼 *Admin buyruqlari:*\n"
            "/add `<kod> | <nomi> | <link>` — kino qo'shish\n"
            "/remove `<kod>` — kino o'chirish\n"
        )
    await update.message.reply_text(text, parse_mode="Markdown")


async def list_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kinolar ro'yxati"""
    if not movies:
        await update.message.reply_text("❌ Hozircha kino bazasi bo'sh.")
        return

    text = "🎬 *Mavjud Kinolar:*\n\n"
    for kod, info in movies.items():
        text += f"🔹 `{kod}` — {info['nomi']}\n"
    text += "\nKod yuboring va filmni oling!"
    await update.message.reply_text(text, parse_mode="Markdown")


async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: kino qo'shish — /add 1004 | Titanic | https://t.me/..."""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Siz admin emassiz!")
        return

    try:
        args = " ".join(context.args).split("|")
        kod = args[0].strip()
        nomi = args[1].strip()
        link = args[2].strip()

        movies[kod] = {"nomi": nomi, "link": link}
        await update.message.reply_text(
            f"✅ Kino qo'shildi!\n\n"
            f"🔹 Kod: `{kod}`\n"
            f"🎬 Nomi: {nomi}\n"
            f"🔗 Link: {link}",
            parse_mode="Markdown",
        )
    except (IndexError, ValueError):
        await update.message.reply_text(
            "❗ To'g'ri format:\n`/add KOD | NOMI | LINK`\n\n"
            "Masalan:\n`/add 1004 | Titanic | https://t.me/kanal/100`",
            parse_mode="Markdown",
        )


async def remove_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: kino o'chirish — /remove 1004"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Siz admin emassiz!")
        return

    if not context.args:
        await update.message.reply_text("❗ Format: `/remove KOD`", parse_mode="Markdown")
        return

    kod = context.args[0].strip()
    if kod in movies:
        nomi = movies[kod]["nomi"]
        del movies[kod]
        await update.message.reply_text(f"🗑️ `{kod}` — {nomi} o'chirildi.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ `{kod}` kodi topilmadi.", parse_mode="Markdown")


async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi kod yuborganda kino link qaytarish"""
    kod = update.message.text.strip()

    if kod in movies:
        movie = movies[kod]
        await update.message.reply_text(
            f"🎬 *{movie['nomi']}*\n\n"
            f"🔗 [Kinoni ko'rish]({movie['link']})\n\n"
            f"🍿 Yaxshi tomosha!",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"❌ `{kod}` kodi topilmadi.\n\n"
            f"📋 Barcha kinolar: /list",
            parse_mode="Markdown",
        )


# ===================== BOTNI ISHGA TUSHIRISH =====================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_movies))
    app.add_handler(CommandHandler("add", add_movie))
    app.add_handler(CommandHandler("remove", remove_movie))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_movie))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
