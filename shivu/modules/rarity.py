from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shivu import user_collection, application

async def add_rarity(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user = await user_collection.find_one({'id': user_id})

    if not user:
        await update.message.reply_html("<b>You haven't caught any characters yet.</b>")
        return

    rarities = ["⛩️ Celestial", "🎀 Pookie", "🖤 Phantom", "🥀 Sexy", "👻 Loli", "🎗️ Eclipse"]
    current_rarity = user.get('selected_rarity')

    keyboard = []
    for i in range(0, len(rarities), 2):
        row = [
            InlineKeyboardButton(f"{rarities[i].title()} {'✅️' if rarities[i] == current_rarity else ''}", 
                                 callback_data=f"add_rarity:{rarities[i]}"),
        ]
        if i + 1 < len(rarities):
            row.append(InlineKeyboardButton(f"{rarities[i + 1].title()} {'✅️' if rarities[i + 1] == current_rarity else ''}", 
                                             callback_data=f"add_rarity:{rarities[i + 1]}"))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ", callback_data="add_rarity:default")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a rarity for your characters:", reply_markup=reply_markup)

async def rarity_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    if data.startswith("add_rarity:"):
        rarity = data.split(':')[1]
        user_id = query.from_user.id

        await user_collection.update_one(
            {'id': user_id},
            {'$set': {'selected_rarity': rarity if rarity != "default" else None}},
            write_concern={'w': 1}  # Adjusted write concern
        )
        await query.answer(f"Rarity set to: {rarity.title() if rarity != 'default' else 'Default'}")
        await query.edit_message_text("Rarity updated successfully.")

application.add_handler(CommandHandler("mode", add_rarity, block=False))
application.add_handler(CallbackQueryHandler(rarity_callback, pattern='^add_rarity:', block=False))
