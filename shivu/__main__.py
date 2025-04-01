import importlib
import time
import random
import re
import asyncio
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters
from shivu import (
    collection,
    top_global_groups_collection,
    group_user_totals_collection,
    user_collection,
    user_totals_collection,
    shivuu,
    application,
    SUPPORT_CHAT,
    UPDATE_CHAT,
    db,
    LOGGER
)
from shivu.modules import ALL_MODULES

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("shivu.modules." + module_name)

def escape_markdown(text):
    escape_chars = r'\\*_`~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\1', text)

async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id
    
    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]
    
    async with lock:
        chat_frequency = await user_totals_collection.find_one({'chat_id': chat_id})
        message_frequency = chat_frequency.get('message_frequency', 100) if chat_frequency else 100

        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
                if user_id in warned_users and time.time() - warned_users[user_id] < 600:
                    return
                await update.message.reply_text(
                    f"<blockquote>⚠️ Don't Spam {escape(update.effective_user.first_name)}...\n"
                    "Your Messages Will be ignored for 10 Minutes...</blockquote>", 
                    parse_mode='HTML'
                )
                warned_users[user_id] = time.time()
                return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        message_counts[chat_id] = message_counts.get(chat_id, 0) + 1
        
        if message_counts[chat_id] % message_frequency == 0:
            await send_image(update, context)
            message_counts[chat_id] = 0

async def send_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    all_characters = list(await collection.find({}).to_list(length=None))
    
    if chat_id not in sent_characters:
        sent_characters[chat_id] = []
    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []
    
    character = random.choice([c for c in all_characters if c['id'] not in sent_characters[chat_id]])
    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character
    first_correct_guesses.pop(chat_id, None)
    
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption=f"<blockquote>A New {character['rarity']} Cosplay Character Appeared...\n"
                "/guess Character Name and add in Your Collection</blockquote>",
        parse_mode='HTML'
    )

async def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if chat_id not in last_characters:
        return
    if chat_id in first_correct_guesses:
        await update.message.reply_text(
            '<blockquote>❌️ Already Guessed By Someone.. Try Next Time Bruhh</blockquote>',
            parse_mode='HTML'
        )
        return
    
    guess_text = ' '.join(context.args).lower() if context.args else ''
    if "()" in guess_text or "&" in guess_text.lower():
        await update.message.reply_text("<blockquote>Nahh You Can't use This Types of words in your guess..❌️</blockquote>", parse_mode='HTML')
        return
    
    name_parts = last_characters[chat_id]['name'].lower().split()
    if sorted(name_parts) == sorted(guess_text.split()) or any(part == guess_text for part in name_parts):
        first_correct_guesses[chat_id] = user_id
        await update.message.reply_text(
            f'<blockquote>✅️ Correct Guess! {escape(update.effective_user.first_name)} guessed {last_characters[chat_id]["name"]} from {last_characters[chat_id]["anime"]}</blockquote>',
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text('<blockquote>Please Write Correct Character Name... ❌️</blockquote>', parse_mode='HTML')

async def fav(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text('<blockquote>Please provide Character ID...</blockquote>')
        return
    
    character_id = context.args[0]
    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text('<blockquote>You have not Guessed any characters yet....</blockquote>')
        return
    
    character = next((c for c in user['characters'] if c['id'] == character_id), None)
    if not character:
        await update.message.reply_text('This Character is Not In your collection')
        return
    
    user['favorites'] = [character_id]
    await user_collection.update_one({'id': user_id}, {'$set': {'favorites': user['favorites']}})
    await update.message.reply_text(f'<blockquote>Character {character["name"]} has been added to your favorites...</blockquote>')

def main() -> None:
    application.add_handler(CommandHandler(["guess", "protecc", "collect", "grab", "hunt"], guess, block=False))
    application.add_handler(CommandHandler("fav", fav, block=False))
    application.add_handler(MessageHandler(filters.ALL, message_counter, block=False))
    application.run_polling(drop_pending_updates=True)
    
if __name__ == "__main__":
    shivuu.start()
    LOGGER.info("Bot started")
    main()
