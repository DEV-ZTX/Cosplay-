from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from html import escape
import math
from shivu import collection, user_collection, application

async def harem(update: Update, context: CallbackContext, page=0, edit=False) -> None:
    user_id = update.effective_user.id
    harem_mode_mapping = {
        "celestial": "⛩️ Celestial",
        "pookie": "🎀 Pookie",
        "phantom": "🖤 Phantom",
        "sexy": "🥀 Sexy",
        "loli": "👻 Loli",
        "eclipse": "🎗️ Eclipse",
        "default": None
    }

    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text("You need to register first by starting the bot in DM.")
        return

    characters = user.get('characters', [])
    hmode = user.get('smode', 'default')
    rarity_value = "all" if hmode == "default" else harem_mode_mapping.get(hmode)

    characters = [char for char in characters if isinstance(char, dict) and (hmode == "default" or char.get('rarity') == rarity_value)]
    characters = sorted(characters, key=lambda x: (x.get('anime', ''), x.get('id', '')))

    if not characters:
        await update.message.reply_text("You don't have any characters matching the current rarity. Please change it from /hmode.")
        return

    total_pages = math.ceil(len(characters) / 10)
    page = max(0, min(page, total_pages - 1))
    current_characters = characters[page * 10:(page + 1) * 10]

    harem_message = f"<b>{escape(update.effective_user.first_name)}'s Harem - Page {page + 1}/{total_pages}</b>\n"
    for character in current_characters:
        anime = character.get("anime", "Unknown")
        count = await collection.count_documents({"anime": anime})
        harem_message += f'\n𖤍 <b>{anime}</b> ｛{len(characters)}/{count}｝\n'
        harem_message += f'⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n'
        harem_message += f'<b>𒄬</b> {character["id"]} [ {character["rarity"][0]} ] {character["name"]}\n'
        harem_message += f'⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n'

    keyboard = [[InlineKeyboardButton("💠 Inline 💠", switch_inline_query_current_chat=f"collection.{user_id}")]]
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⤂", callback_data=f"harem:{page - 1}:{user_id}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("⤃", callback_data=f"harem:{page + 1}:{user_id}"))
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await update.callback_query.edit_message_text(harem_message, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(harem_message, reply_markup=reply_markup, parse_mode='HTML')

async def harem_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    _, page, user_id = query.data.split(':')
    await harem(update, context, int(page), edit=True)

async def set_hmode(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ", callback_data="default"),
         InlineKeyboardButton("ʀᴀʀɪᴛʏ", callback_data="rarity")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(
        photo="https://graph.org/file/4b0da20b223036b6c7989.jpg",
        caption=f"{escape(update.effective_user.first_name)} ᴘʟᴇᴀꜱᴇ ᴄʜᴏᴏꜱᴇ ʀᴀʀɪᴛʏ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜱᴇᴛ ᴀꜱ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ",
        reply_markup=reply_markup
    )

async def hmode_rarity(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🟢 Common", callback_data="celestial"),
         InlineKeyboardButton("🟣 Rare", callback_data="pookie")],
        [InlineKeyboardButton("🟡 Legendary", callback_data="phantom"),
         InlineKeyboardButton("💮 Special Edition", callback_data="spacial_edition")],
        [InlineKeyboardButton("🔮 Premium Edition", callback_data="premium_edition"),
         InlineKeyboardButton("🎗️ Supreme", callback_data="supreme")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query

    await query.edit_message_caption(
        caption="𝐂𝐡𝐚𝐧𝐠𝐞 𝐒𝐨𝐫𝐭𝐢𝐧𝐠 𝐌𝐨𝐝𝐞 𝐓𝐨 : ʀᴀʀɪᴛʏ",
        reply_markup=reply_markup
    )
    await query.answer()

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data in ["common", "rare", "legendary", "spacial_edition", "premium_edition", "supreme"]:
        await user_collection.update_one({'id': user_id}, {'$set': {'smode': data}})
        await query.answer(f"Harem mode set to {data}!")
        await harem(update, context)

    elif data == "default":
        await user_collection.update_one({'id': user_id}, {'$set': {'smode': 'default'}})
        await query.answer("Harem mode set to default!")
        await harem(update, context)

# Adding the handlers to the application
application.add_handler(CommandHandler(["hharem"], harem, block=False))
application.add_handler(CallbackQueryHandler(harem_callback, pattern='^harem', block=False))
application.add_handler(CommandHandler("hhmode", set_hmode))
application.add_handler(CallbackQueryHandler(button, pattern='^default$|^rarity$|^common$|^rare$|^legendary$|^spacial_edition$|^premium_edition$|^supreme$', block=False))
