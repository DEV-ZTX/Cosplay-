from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from itertools import groupby
import math
import random

# Assuming you have these collections defined for your database
from shivu import collection, user_collection, application

async def harem(update: Update, context: CallbackContext, page=0) -> None:
    user_id = update.effective_user.id  
    user = await user_collection.find_one({'id': user_id})

    if not user:
        await reply_no_characters(update)
        return

    selected_rarity = user.get('selected_rarity')
    characters = sorted(user['characters'], key=lambda x: (x['anime'], x['id']))

    if selected_rarity:
        characters = [character for character in characters if character['rarity'][0] == selected_rarity[0]]

    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}
    unique_characters = list({character['id']: character for character in characters}.values())
    total_pages = math.ceil(len(unique_characters) / 15)

    if page < 0 or page >= total_pages:
        page = 0

    harem_message = f"{update.effective_user.first_name}'s ʜᴀʀᴇᴍ - ᴘᴀɢᴇ {page + 1}/{total_pages}\n"   
    current_characters = unique_characters[page * 15:(page + 1) * 15]
    current_grouped_characters = {k: list(v) for k, v in groupby(current_characters, key=lambda x: x['anime'])}

    for anime, characters in current_grouped_characters.items():
        harem_message += f'\n𖤍 {anime} ｛{len(characters)}/{await collection.count_documents({"anime": anime})}｝\n'
        harem_message += f'⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n'
        for character in characters:
            count = character_counts[character['id']]
            harem_message += f'𒄬 {character["id"]} [ {character["rarity"][0]} ] {character["name"]} ×{count}\n'
        harem_message += f'⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n'

    total_count = len(user['characters'])
    keyboard = [
        [InlineKeyboardButton(f"sᴇᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ({total_count})", switch_inline_query_current_chat=f"collection.{user_id}")],
        [InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="ignore")]
    ]

    if total_pages > 1:
        nav_buttons = [
            InlineKeyboardButton("⬅️1x", callback_data=f"harem:{page - 1}:{user_id}") if page > 0 else None,
            InlineKeyboardButton("1x➡️", callback_data=f"harem:{page + 1}:{user_id}") if page < total_pages - 1 else None
        ]
        if page >= 6:
            nav_buttons.insert(0, InlineKeyboardButton("⏪x6", callback_data=f"harem:{page - 6}:{user_id}"))
        if page + 6 < total_pages:
            nav_buttons.append(InlineKeyboardButton("6x⏩", callback_data=f"harem:{page + 6}:{user_id}"))
        keyboard.append(list(filter(None, nav_buttons)))

    reply_markup = InlineKeyboardMarkup(keyboard)
    await send_harem_message(update, harem_message, reply_markup, user)

async def reply_no_characters(update: Update):
    if update.message:
        await update.message.reply_text('ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ɢᴜᴇssᴇᴅ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀs ʏᴇᴛ.')
    else:
        await update.callback_query.edit_message_text('ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ɢᴜᴇssᴇᴅ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀs ʏᴇᴛ.')

async def send_harem_message(update, harem_message, reply_markup, user):
    if 'favorites' in user and user['favorites']:
        fav_character_id = user['favorites'][0]
        fav_character = next((c for c in user['characters'] if c['id'] == fav_character_id), None)
        if fav_character and 'img_url' in fav_character:
            if update.message:
                await update.message.reply_photo(photo=fav_character['img_url'], caption=harem_message, reply_markup=reply_markup)
            else:
                await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
        else:
            await reply_with_message(update, harem_message, reply_markup)
    else:
        await reply_with_random_character(update, harem_message, reply_markup, user)

async def reply_with_message(update, harem_message, reply_markup):
    if update.message:
        await update.message.reply_text(harem_message, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(harem_message, reply_markup=reply_markup)

async def reply_with_random_character(update, harem_message, reply_markup, user):
    if user['characters']:
        random_character = random.choice(user['characters'])
        if 'img_url' in random_character:
            if update.message:
                await update.message.reply_photo(photo=random_character['img_url'], caption=harem_message, reply_markup=reply_markup)
            else:
                await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup)
        else:
            await reply_with_message(update, harem_message, reply_markup)
    else:
        await update.message.reply_text("ʏᴏᴜʀ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ :)")

async def harem_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    _, page, user_id = data.split(':')
    page = int(page)
    user_id = int(user_id)

    if query.from_user.id != user_id:
        await query.answer("ᴅᴏɴ'ᴛ sᴛᴀʟᴋ ᴏᴛʜᴇʀ ᴜsᴇʀ's ʜᴀʀᴇᴍ..  OK", show_alert=True)
        return

    await harem(update, context, page)

# Handlers
application.add_handler(CommandHandler("hharem", harem, block=False))
application.add_handler(CallbackQueryHandler(harem_callback, pattern='^harem', block=False))