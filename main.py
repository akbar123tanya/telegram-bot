from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

# --- لیستی وشەکان ---
BAD_WORDS = ["کێر", "قحبە", "سۆزانی", "گێچ", "بۆجی", "قوز", "کوص", "fuck", "sex"]
LOVE_WORDS = ["خۆشم ئەوێی", "خۆشمدەوێی", "ئاشقتم", "ئاشقی توم", "دەمەوێی", "بمخۆشەوی", "love you"]
FIGHT_WORDS = ["شەڕ", "بەجەنگ", "لێیدەم", "دەکوژم", "بمرە", "بیگرە"]

# --- 1. بەخێرهاتن ---
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id != context.bot.id:
            await update.message.reply_text(f"بەخێربێی {member.first_name} گیان بۆ گرووپەکەمان 👋❤️")

# --- 2. کۆنترۆڵی هەموو نامەکان ---
async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    text_original = update.message.text
    user_name = update.message.from_user.first_name
    
    # ئایا بۆتەکە تاگ کراوە یان ڕیپلەی کراوە؟
    is_reply_to_bot = False
    if update.message.reply_to_message:
        if update.message.reply_to_message.from_user.id == context.bot.id:
            is_reply_to_bot = True

    is_mention = False
    if context.bot.username.lower() in text:
        is_mention = True
    if update.message.entities:
        for ent in update.message.entities:
            if ent.type == "mention":
                is_mention = True

    # --- ئەگەر داوای خۆشەویستی لێکردی ---
    if any(w in text for w in LOVE_WORDS):
        await update.message.reply_text(f"{user_name} گیان ببورە گیراوم 😅❤️ ئەزانی خۆشم دەوێی وەک هاوڕێ بەڵام دڵم لای کەسێکی ترە!")
        return

    # --- ئەگەر قسەی نەشیاوی پێوتی ---
    if any(w in text for w in BAD_WORDS):
        try:
            await update.message.delete()
        except:
            pass
        
        # ئەگەر تاگی کردبووی یان ڕیپلەی کردبووی
        if is_reply_to_bot or is_mention:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{user_name} تۆ گۆمەخۆ لەتیف 😒 داوای خۆشەویستی و قسەی ناشرین لەگەڵ من مەکە، ببورە گیراوم!"
            )
        else:
            # ئەگەر لە گرووپ قسەی ناشرینی کرد
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{user_name} گیان قسەی ناشرین مەکە بابە، کەمێک تەربیەتت هەبێ 🙏 نامەکەت سڕایەوە."
            )
        return

    # --- ئەگەر شەڕیان کرد ---
    if any(w in text for w in FIGHT_WORDS):
        await update.message.reply_text(f"هاوڕێیان @ {user_name} مناقەشە وا ناکرێ لەسەر خۆبن 🕊️ تکایە قسەتان تێک نەچێ، ئارام بنەوە.")
        return

    # --- ئەگەر تەنها تاگی کردی (بێ قسەی ناشرین) ---
    if is_reply_to_bot or is_mention:
        await update.message.reply_text(f"بەڵێ {user_name} گیان؟ گوێم لێتە 👂")

# --- سەرەکی ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))
    print("Bot is running...")
    app.run_polling()

if name == "main":
    main()
