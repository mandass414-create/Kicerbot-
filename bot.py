import os, io
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Kicer Online!"

user_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✂️ Hapus Background", callback_data="hapus")],
        [InlineKeyboardButton("⬜ BG Putih", callback_data="putih"), InlineKeyboardButton("⬛ BG Hitam", callback_data="hitam")],
        [InlineKeyboardButton("🟦 BG Biru", callback_data="biru"), InlineKeyboardButton("🟥 BG Merah", callback_data="merah")],
        [InlineKeyboardButton("⚫ Hitam Putih", callback_data="bw"), InlineKeyboardButton("☀️ Terangin", callback_data="terang")],
        [InlineKeyboardButton("🌫️ Blur Background", callback_data="blur")],
    ]
    await update.message.reply_text("Halo Met! Pilih editnya, terus kirim fotonya.\n\nBot Kicer - Benhas Studio", reply_markup=InlineKeyboardMarkup(keyboard))

async def pilih(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_mode[q.from_user.id] = q.data
    await q.message.reply_text(f"Oke, mode {q.data} aktif. Sekarang kirim fotonya!")

async def foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = user_mode.get(update.message.from_user.id, "hapus")
    await update.message.reply_text("Lagi diproses... tunggu 10 detik ya ⏳")
    photo = await update.message.photo[-1].get_file()
    data = await photo.download_as_bytearray()
    img = Image.open(io.BytesIO(data)).convert("RGBA")

    if mode in ["hapus","putih","hitam","biru","merah","blur"]:
        no_bg = remove(img)
        if mode == "hapus":
            out = no_bg
        elif mode == "blur":
            bg = img.convert("RGB").filter(ImageFilter.GaussianBlur(15))
            bg = bg.resize(no_bg.size)
            out = Image.alpha_composite(bg.convert("RGBA"), no_bg)
        else:
            warna = {"putih":(255,255,255,255),"hitam":(0,0,0,255),"biru":(0,120,255,255),"merah":(255,0,0,255)}[mode]
            bg = Image.new("RGBA", no_bg.size, warna)
            out = Image.alpha_composite(bg, no_bg)
    elif mode == "bw":
        out = img.convert("L").convert("RGBA")
    elif mode == "terang":
        out = ImageEnhance.Brightness(img.convert("RGB")).enhance(1.4).convert("RGBA")

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    buf.seek(0)
    await update.message.reply_photo(photo=buf, caption="Nih hasilnya, Met! Kirim foto lain atau /start buat ganti mode.")

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(pilih))
    app_bot.add_handler(MessageHandler(filters.PHOTO, foto))
    app_bot.run_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
