from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
from flask import Flask
import threading

BOT_TOKEN=os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

# هەموو جنێوەکان
ALL_INSULTS=[
"حیز","حیزە","گەمژە","گەمژ","خوێڕی","خوڕی","گێلە","گێل","حۆلە","حۆل","سەگ","سەگباب",
"گوبخۆ","گۆبخۆ","گومەخۆ","گۆمەخۆ","گوێرەکە","گوێرە","مانگا","کەر","کەرە","حوشتر","وشتر","حمار",
"قحبە","سۆزانی","قوز","کێر","کیر","کوص","قوندەر","گێچ","بۆجی","لەتیف","مەڕ"
]

async def welcome(update, context):
 for m in update.message.new_chat_members:
  if m.id!=context.bot.id:
   await update.message.reply_text(f"بەخێربێی {m.first_name} گیان 👋❤️")

async def handle_all(update, context):
 if not update.message or not update.message.text: return
 if update.effective_user.is_bot: return
 
 text=update.message.text.lower()
 name=update.effective_user.first_name

 # --- پشکنینی تاگ و ناو و ڕیپلەی ---
 is_reply_to_bot=False
 if update.message.reply_to_message:
  if update.message.reply_to_message.from_user.id==context.bot.id:
   is_reply_to_bot=True
 
 is_mentioned=False
 if "سۆنی" in text or "sony" in text:
  is_mentioned=True
 if update.message.entities:
  for ent in update.message.entities:
   if ent.type=="mention" or ent.type=="text_mention":
    is_mentioned=True
 
 # ئەگەر ناوی نەهێنرا و تاگ نەکرا و ڕیپلەیش نەبوو، هیچ مەڵێ
 if not (is_mentioned or is_reply_to_bot):
  return

 # --- ئەگەر جنێوی پێ وترا ---
 for w in ALL_INSULTS:
  if w in text:
   await update.message.reply_text(f"کەمێ تەربێتت هەبێ {name} گیان 😒")
   return

 # --- ئەگەر بانگی کرد ---
 if "سۆنی" in text or "sony" in text:
  await update.message.reply_text(f"بەڵێ {name} گیان گوێم لێتە 👂")

# Flask بۆ Render
app=Flask(name)
@app.route('/')
def home(): return "SONY Alive"
threading.Thread(target=lambda: app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000))),daemon=True).start()

application=Application.builder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,welcome))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_all))
application.run_polling()
