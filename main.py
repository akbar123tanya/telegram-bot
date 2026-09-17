import os
from keep_alive import keep_alive
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
BAD = ["ÞÍÈ?", "˜íÑ", "˜?ä", "fuck", "˜æÓ"]
FIGHT = ["Ô??", "ÏÇí˜Ê", "È˜æŽ?", "á?í ÈÏ?"]

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for m in update.message.new_chat_members:
        if m.is_bot and m.id != context.bot.id:
            try:
                await context.bot.ban_chat_member(update.effective_chat.id, m.id)
                await context.bot.unban_chat_member(update.effective_chat.id, m.id)
                await update.message.reply_text(f"?? È?Êí {m.first_name} Ï?Ñ˜ÑÇ! Ê?äåÇ Ó?äí ãÇæ? ??")
            except:
                await update.message.reply_text(f"?? È?Ê?˜í ÊÑ åÇÊ {m.first_name} !")
            return
        if not m.is_bot:
            await update.message.reply_text(f"È?Î?ÑÈ?í {m.first_name} ??")

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if update.effective_user.is_bot: return
    low = update.message.text.lower()
    name = update.effective_user.first_name

    for b in BAD:
        if b in low:
            try: await update.message.delete()
            except: pass
            return

    for f in FIGHT:
        if f in low:
            await update.message.reply_text(f"?? {name} Ô?? Þ?Ï?Û?í? ??")
            return

    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    is_tag = "Ó?äí" in low or "sony" in low or context.bot.username.lower() in low

    if not (is_tag or is_reply):
        return

    clean = low.replace("Ó?äí","").replace("sony","").replace(f"@{context.bot.username.lower()}","").strip()

    # Æ?ã? äæ?í?
    if "ÍíÒ" in clean or "ÞÍÈ?" in clean or "ÞÇÍÈ?" in clean or "Îæ?Ñí" in clean or "ÎæíÑí" in clean:
        await update.message.reply_text(f"˜?ã?˜ Ê?ÑÈí?ÊÊ å?È? {name} ??")
    elif "ÌæÇäí" in clean:
        await update.message.reply_text(f"ÇæÊ ÌæÇä? È?ÓÇÞ? {name} ??")
    elif "Î?Ôã?æ?í" in clean or "ÞæÑÈÇäÊ" in clean or "Ú?ÔÞã" in clean:
        await update.message.reply_text(f"R íÑÇæã {name} íÇä ????")
    elif "?áí" in clean or "˜?Ñí" in clean or "æã" in clean:
        await update.message.reply_text("Ê?æã?Î?á?ÊíÝ ??")
    elif "?äí" in clean:
        await update.message.reply_text(f"ÈÇÔã {name} íÇä Ê? ?äí¿ ????")
    elif clean == "":
        await update.message.reply_text(f"íÇä Æ?ãÑ˜? {name}¿ ??")
    else:
        await update.message.reply_text(f"æ?ã á?Ê? {name} íÇä ??")

keep_alive()
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
print("Bot Online ?")
app.run_polling(drop_pending_updates=True)
