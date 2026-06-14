import os
from PIL import Image
from gtts import gTTS
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from inference import detect_from_image
from disease_info import disease_data





# -------------------------------
# TRANSLATION FUNCTION
# -------------------------------
def tr(text, lang):
    if lang == "en":
        return text

    text = text.strip()
    chunks = []

    # Split into safe pieces for Google Translate (limit ~450)
    while len(text) > 450:
        part = text[:450]
        text = text[450:]
        try:
            chunks.append(GoogleTranslator(source="auto", target=lang).translate(part))
        except:
            chunks.append(part)

    try:
        chunks.append(GoogleTranslator(source="auto", target=lang).translate(text))
    except:
        chunks.append(text)

    return " ".join(chunks)


# -------------------------------
# START COMMAND (RESET CONTEXT)
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # CLEAR old user session (important)
    context.user_data.clear()

    await update.message.reply_text(
        "🌴 Coconut Disease Detection Bot\n\n"
        "Send me a **coconut leaf photo**, and I will detect the disease.\n\n"
        "Select language:\n"
        "/english\n/kannada\n/hindi\n/tamil\n/telugu"
    )


# -------------------------------
# LANGUAGE COMMANDS
# -------------------------------
async def english(update, context): 
    context.user_data["lang"] = "en"
    await update.message.reply_text("Language set to English.")

async def kannada(update, context): 
    context.user_data["lang"] = "kn"
    await update.message.reply_text("ಭಾಷೆ ಕನ್ನಡಕ್ಕೆ ಸೆಟ್ ಮಾಡಲಾಗಿದೆ.")

async def hindi(update, context): 
    context.user_data["lang"] = "hi"
    await update.message.reply_text("भाषा हिंदी सेट की गई है।")

async def tamil(update, context): 
    context.user_data["lang"] = "ta"
    await update.message.reply_text("மொழி தமிழாக அமைக்கப்பட்டது.")

async def telugu(update, context): 
    context.user_data["lang"] = "te"
    await update.message.reply_text("భాష తెలుగుకు మార్చబడింది.")



# -------------------------------
# HANDLE IMAGE MESSAGE
# -------------------------------
async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lang = context.user_data.get("lang", "en")

    # Validate gTTS language codes
    valid_langs = ["en", "kn", "hi", "ta", "te"]
    if lang not in valid_langs:
        lang = "en"

    # Download image
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = "received.jpg"
    await file.download_to_drive(image_path)

    await update.message.reply_text(tr("Analyzing image… please wait.", lang))

    # Run YOLO detection
    results = detect_from_image(image_path)

    if len(results[0].boxes) == 0:
        await update.message.reply_text(tr("No disease detected.", lang))
        return

    cls_idx = int(results[0].boxes.cls[0])

    class_names = [
        "bud root dropping",
        "bud rot",
        "gray leaf spot",
        "leaf rot",
        "stembleeding",
    ]

    disease = class_names[cls_idx]

    info = disease_data.get(disease)

    # -------------------------------
    # Build detailed response
    # -------------------------------
    description = tr(info["description"], lang)
    causes = "\n".join([f"• {tr(c, lang)}" for c in info["causes"]])
    symptoms = "\n".join([f"• {tr(s, lang)}" for s in info["symptoms"]])
    treatment = "\n".join([f"• {tr(t, lang)}" for t in info["treatment"]])
    shop = "\n".join([f"{tr(k, lang)}: {v}" for k, v in info["shopping_links"].items()])

    msg = (
        f"🌴 *{tr('Disease Detected', lang)}*: {tr(disease, lang)}\n\n"
        f"📝 *{tr('Description', lang)}*:\n{description}\n\n"
        f"⚠️ *{tr('Causes', lang)}*:\n{causes}\n\n"
        f"❗ *{tr('Symptoms', lang)}*:\n{symptoms}\n\n"
        f"💊 *{tr('Treatment', lang)}*:\n{treatment}\n\n"
        f"🛒 *{tr('Buy Online', lang)}*:\n{shop}"
    )   


    await update.message.reply_markdown(msg)

    # -------------------------------
    # Voice Explanation using gTTS
    # -------------------------------
    voice_text = (
        f"{tr(disease, lang)}. "
        f"{description}. "
        f"{tr('Causes', lang)}: {', '.join([tr(c, lang) for c in info['causes']])}. "
        f"{tr('Symptoms', lang)}: {', '.join([tr(s, lang) for s in info['symptoms']])}. "
        f"{tr('Treatment', lang)}: {', '.join([tr(t, lang) for t in info['treatment']])}."
    )

    tts = gTTS(text=voice_text, lang=lang)
    tts.save("voice.mp3")

    await update.message.reply_voice(open("voice.mp3", "rb"))




# -------------------------------
# MAIN FUNCTION
# -------------------------------
def main():

    TOKEN = "8015587379:AAHfsuW3XYakOij22ZA4wpMFmBfVo14XGaA"



    app = (
    ApplicationBuilder()
    .token(TOKEN)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .build()
)


    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("english", english))
    app.add_handler(CommandHandler("kannada", kannada))
    app.add_handler(CommandHandler("hindi", hindi))
    app.add_handler(CommandHandler("tamil", tamil))
    app.add_handler(CommandHandler("telugu", telugu))

    # Image handler
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))
    

    print("Bot is running... Waiting for messages...")

    app.run_polling()


if __name__ == "__main__":
    main()
