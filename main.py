import os
import threading
from flask import Flask
BAD_WORDS = ["دایکت","خوشکت","بگێم","گۆبخۆ","گان دەر","سوک","ڕسوا","حەیوان","گەواد","کێر","مژ","جاش","خۆفرۆش","کۆیلە"]
app = Flask(__name__)

@app.route('/')
def home():
    return "SONY Alive!"

@app.route('/health')
def health():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

import random
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
async def filter_bad(update, context):
    if update.message and update.message.text:
        txt = update.message.text.lower()
        for w in BAD_WORDS:
            if w in txt:
                try:
                    await update.message.delete()
                except:
                    pass
                return

async def hazt_lachya(update, context):
    txt = update.message.text if update.message else ""
    if "حەزت لەچیە" in txt or "حەزت لە چیە" in txt:
        await update.message.reply_text("هێلکە و ساردی دیو 😂")











    
    
threading.Thread(target=run_web, daemon=True).start()
# ===== وەشەکان =====
BAD_WORDS = ["قحبە", "حیز", "گەمژە", "سەگباب", "کونی", "کۆن", "خوێڕی"] # ئەمانە دەسڕێتەوە
FIGHT_WORDS = ["شەڕ", "لیبدەن", "بیکوژن", "بجەن", "دەبێ شەڕ بکەین"]
ANIMALS = ["کەر", "مانگا", "حوشتر", "سەگ", "مەیمون"]

# وەڵامەکان
def get_answer(text):
    text = text.lower()
    if "ناوت چیە" in text: return "ناوم سۆنی یە گیان 😊"
    if "خەڵکی کوێی" in text: return "خەڵکی ئەم گرووپە جوانەم ❤️"
    if "چۆنی" in text: return "باشم گیان، تۆ چۆنی؟"
    if "کاتژمێر" in text: return "سەیرێکی کاتژمێرەکەت بکە گیان 😅"
    if "خۆشم ئەوێی" in text or "خوشمەوێی" in text: return "منیش تۆم خۆشدەوێ گیان 😍"
    if "سڵاو" in text or "سلام" in text: return "سڵاو گیان ❤️"
    return None

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        for m in update.message.new_chat_members:
            if m.id != context.bot.id:
                await update.message.reply_text(f"بەخێربێی {m.first_name} گیان 👋")
    except: pass

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if update.effective_user.is_bot: return

    text = update.message.text
    text_low = text.lower()
    name = update.effective_user.first_name
    user_id = update.effective_user.id

    # 1- مەرجی سڕینەوەی قسەی ناشرین (هەمیشە ئیش دەکات، تەنانەت بێ تاگ)
    for w in BAD_WORDS:
        if w in text_low:
            try:
                await update.message.delete()
                await context.bot.send_message(update.effective_chat.id, f"{name} گیان قسەی ناشرین مەکە با نەیسڕمەوە 😐")
            except: pass
            return

    # 2- تەنها ئەگەر تاگ کرا یان ناوی هێنرا یان ڕیپلەی کرا
    is_reply_to_bot = False
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        is_reply_to_bot = True
    
    is_mentioned = "سۆنی" in text_low or "sony" in text_low or f"@{context.bot.username}" in text_low
    
    if not (is_mentioned or is_reply_to_bot):
        return

    # 3- شەڕ
    for w in FIGHT_WORDS:
        if w in text_low:
            await update.message.reply_text("لەسەر خۆبن گیان، مناقەشە وا ناکرێ 🙏 لەسەر خۆبن")
            return

    # 4- جنێوی تایبەت
    if "گومەخۆ" in text_low or "گوبخۆ" in text_low or "گوێرەکە" in text_low or "حۆلە" in text_low:
        await update.message.reply_text(f"تۆ گومەخۆی لەتیف {name} گیان 😒")
        return

    # 5- کەر و مانگا و حوشتر
    for w in ANIMALS:
        if w in text_low:
            await update.message.reply_text(f"کەمێک تەربێتت هەبێ {name} گیان 😑")
            return

    # 6- وەڵامی پرسیارەکان
    answer = get_answer(text_low)
    if answer:
        await update.message.reply_text(f"{answer} - گیان")
        return
    
    # 7- ئەگەر پرسیاری کرد و نەمانزانی
    if "؟" in text or "?" in text or text_low.startswith("چی") or text_low.startswith("کێ") or text_low.startswith("بۆچی"):
        await update.message.reply_text(f"نازانم گیان {name} 🥺")
        return

    # 8- وەڵامی کۆتایی کە بانگی دەکەن
    await update.message.reply_text(f"گیان ئەمرکە {name} گیان 👂❤️")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    print("SONY Started")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))
    application.run_polling()
   application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad), group=0)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hazt_lachya), group=1) 
    
    
    
    
    
