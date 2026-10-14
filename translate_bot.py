import logging, json, urllib.request, time, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LANGS = {"ar": "العربية", "fr": "الفرنسية", "en": "الإنجليزية", "es": "الإسبانية", "tr": "التركية"}

def translate(text, target_lang):
    lang_names = {"ar":"Arabic","fr":"French","en":"English","es":"Spanish","tr":"Turkish"}
    target = lang_names.get(target_lang, "English")
    prompt = "Translate the following text to " + target + ". Reply ONLY with the translation, without any extra words:\n\n" + text
    for attempt in range(3):
        try:
            body = json.dumps({
                "messages": [
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt}
                ],
                "model": "openai"
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://text.pollinations.ai/",
                data=body,
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = resp.read().decode("utf-8").strip()
                if result:
                    return result
        except Exception as e:
            logging.error("translate attempt " + str(attempt+1) + ": " + str(e)[:80])
            time.sleep(3)
    return "تعذر الترجمة، حاول مرة أخرى."

def lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇩🇿 العربية", callback_data="lang_ar"), InlineKeyboardButton("🇫🇷 الفرنسية", callback_data="lang_fr"), InlineKeyboardButton("🇬🇧 الإنجليزية", callback_data="lang_en")],
        [InlineKeyboardButton("🇪🇸 الإسبانية", callback_data="lang_es"), InlineKeyboardButton("🇹🇷 التركية", callback_data="lang_tr")]])

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌍 بوت الترجمة\n\nأرسل نصًا وسأترجمه.\nاختر اللغة أولًا:", reply_markup=lang_keyboard())

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lang = update.callback_query.data.replace("lang_", "")
    context.user_data["target_lang"] = lang
    await update.callback_query.message.reply_text("✅ " + LANGS.get(lang, lang) + "\nأرسل النص الآن.")

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text or not text.strip(): return
    target = context.user_data.get("target_lang")
    if not target:
        await update.message.reply_text("⚠️ اختر اللغة أولًا:", reply_markup=lang_keyboard()); return
    await update.message.chat.send_action("typing")
    await update.message.reply_text("⏳ جاري الترجمة...")
    result = translate(text.strip(), target)
    await update.message.reply_text("🌍 " + LANGS.get(target, target) + ":\n\n" + result, reply_markup=lang_keyboard())

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).read_timeout(60).connect_timeout(30).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    print("Bot running..."); app.run_polling()

if __name__ == "__main__":
    main()
