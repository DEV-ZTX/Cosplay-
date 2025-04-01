import random
from html import escape
from pymongo import ASCENDING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from shivu import pm_users as collection

def get_keyboard():
    """Generate the bot's main menu keyboard."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("HELP", callback_data='help')],
        [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new'),
         InlineKeyboardButton("UPDATES", url=f'https://t.me/{UPDATE_CHAT}')]
    ])

async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    user = update.effective_user
    user_id, first_name, username = user.id, user.first_name, user.username or "Unknown"

    # Store user details in the database
    user_data = await collection.find_one({"_id": user_id})
    if not user_data:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"New user started the bot: <a href='tg://user?id={user_id}'>{escape(first_name)}</a>",
            parse_mode='HTML'
        )
    elif user_data['first_name'] != first_name or user_data['username'] != username:
        await collection.update_one(
            {"_id": user_id}, {"$set": {"first_name": first_name, "username": username}}
        )

    # Send welcome message
    caption = (
        "<blockquote><b>❖ Welcome, Cosplay Enthusiast!</b></blockquote>\n\n"
        "<blockquote><b>❍ I am the Ultimate Cosplay Character Collector Bot!</b></blockquote>\n"
        "Add me to your group, and I'll drop random Cosplay Character images every 100 messages!\n"
        "Use <code>/guess</code> to collect your favorite characters and view them with <code>/coscollection</code>.\n"
        "๏ Time to build your ultimate Cosplay Gallery!"
    )

    photo_url = random.choice(PHOTO_URL)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=get_keyboard(),
        parse_mode='HTML'
    )

async def button(update: Update, context: CallbackContext) -> None:
    """Handles button callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = (
            "<blockquote><b>Cosplay Collector Help Section:</b></blockquote>\n\n"
            "<code>/guess</code> - Guess the cosplay character (group only)\n"
            "<code>/fav</code> - Add your favorite cosplay character\n"
            "<code>/trade</code> - Trade cosplay characters\n"
            "<code>/gift</code> - Gift a cosplay character to another user (group only)\n"
            "<code>/harem</code> - View your cosplay character collection\n"
            "<code>/topgroups</code> - See top groups with the most active collectors\n"
            "<code>/top</code> - View top cosplay collectors\n"
            "<code>/changetime</code> - Adjust cosplay drop frequency (group only)\n"
            "<code>/hmode</code> - Opens the harem mode (group only)"
        )
        await query.edit_message_caption(
            caption=help_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⤾ Back", callback_data='back')]]),
            parse_mode='HTML'
        )
    elif query.data == 'back':
        await query.edit_message_caption(
            caption=(
                "<blockquote><b>Welcome, Cosplay Enthusiast!</b></blockquote>\n\n"
                "<blockquote><b>I am the Ultimate Cosplay Character Collector Bot!</b></blockquote>\n"
                "Add me to your group to start collecting amazing cosplay characters!"
            ),
            reply_markup=get_keyboard(),
            parse_mode='HTML'
        )

# Ensure database indexes are created properly
try:
    db.characters.create_index([('id', ASCENDING)])
    db.characters.create_index([('anime', ASCENDING)])
    db.characters.create_index([('img_url', ASCENDING)])
except Exception as e:
    print(f"Error creating database indexes: {e}")

# Add handlers to the bot
application.add_handler(CallbackQueryHandler(button, pattern='^(help|back)$', block=False))
application.add_handler(CommandHandler('start', start, block=False))
        
