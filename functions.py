import os
import random
import ffmpeg
import string
from telegram import InputFile, InlineQueryResultVoice
from gtts import gTTS
from dotenv import load_dotenv


load_dotenv()

storage_id = os.getenv("STORAGE_GROUP_ID")

async def handle_voice(update, context):
    voice = update.message.voice
    file = await voice.get_file()  # Get the voice file
    file_name = "".join(random.choices(string.ascii_letters + string.digits, k= 6)) + ".mp3"
    await file.download_to_drive(file_name)
    # Now I am gonna use @ffmpeg
    changed_file = "".join(random.choices(string.ascii_letters + string.digits, k= 6)) + ".mp3"
    ffmpeg.input(file_name).output(changed_file, af='asetrate=44100*1.5,aresample=44100').run()
    os.remove(file_name)

    with open(changed_file, "rb") as modulated_file:
        await update.message.reply_voice(voice=InputFile(modulated_file))
    os.remove(changed_file)

async def handle_tts(update, context):
    query = update.inline_query.query
    if query == "" :
        return
    file_name = "".join(random.choices(string.ascii_letters + string.digits, k= 6)) + ".mp3"
    tts = gTTS(query, lang = "en-uk")
    tts.save(file_name)

    changed_file = "".join(random.choices(string.ascii_letters + string.digits, k= 6)) + ".mp3"
    ffmpeg.input(file_name).output(changed_file, af='atempo=1.5').run()
    os.remove(file_name)

    with open(changed_file, 'rb') as voice_file:
        sent_file = await context.bot.send_voice(chat_id = storage_id, voice = InputFile(voice_file, filename = changed_file))
    
    os.remove(changed_file)
    file_id = sent_file.voice.file_id
    
    results = [
        InlineQueryResultVoice(
            id = 1,
            voice_url = file_id,
            title = "Tap 👆 To send"
        )
    ]

    await update.inline_query.answer(results)
