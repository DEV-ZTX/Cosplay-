from pyrogram import filters
from pyrogram.types import Message

from shivu import shivuu as app
from shivu import sudo_users 

DEV_LIST = [7678359785]

@app.on_message(filters.command(["addsudo"]) & filters.reply & filters.user(DEV_LIST))
async def sudoadd(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ."
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if int(user.id) in sudo_users:
            return await message.reply_text(f"» {user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
        try:
            sudo_users.add(int(user.id))
            await message.reply_text(f"ᴀᴅᴅᴇᴅ {user.mention} ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.")
        except:
            return await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴜsᴇʀ ɪɴ sᴜᴅᴏᴇʀs.")

    if message.reply_to_message.from_user.id in sudo_users:
        return await message.reply_text(
            f"» {message.reply_to_message.from_user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ."
        )
    try:
        sudo_users.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            f"ᴀᴅᴅᴇᴅ {message.reply_to_message.from_user.mention} ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ."
        )
    except:
        return await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴜsᴇʀ ɪɴ sᴜᴅᴏᴇʀs.")


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(DEV_LIST))
async def sudodel(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ."
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if int(user.id) not in sudo_users:
            return await message.reply_text(
                f"» {user.mention} ɪs ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ."
            )
        try:
            sudo_users.remove(int(user.id))
            return await message.reply_text(
                f"» ʀᴇᴍᴏᴠᴇᴅ {user.mention} ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ."
            )
        except:
            return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ ғʀᴏᴍ sᴜᴅᴏᴇʀs.")
    else:
        user_id = message.reply_to_message.from_user.id
        if int(user_id) not in sudo_users:
            return await message.reply_text(
                f"» {message.reply_to_message.from_user.mention} ɪs ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ."
            )
        try:
            sudo_users.remove(int(user_id))
            return await message.reply_text(
                f"» ʀᴇᴍᴏᴠᴇᴅ {message.reply_to_message.from_user.mention} ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ."
            )
        except:
            return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ ғʀᴏᴍ sᴜᴅᴏᴇʀs.")


@app.on_message(filters.command(["sudolist", "sudoers", "sudo"]))
async def sudoers_list(_, message: Message):
    hehe = await message.reply_text("» ɢᴇᴛᴛɪɴɢ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ...")
    text = "<u>🥀 ᴏᴡɴᴇʀ :</u>\n"
    count = 0
    user = await app.get_users(DEV_LIST)
    user = user.first_name if not user.mention else user.mention
    count += 1
    text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in sudo_users:
        if user_id != DEV_LIST:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n<u>✨ sᴜᴅᴏᴇʀs :</u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("» ɴᴏ sᴜᴅᴏ ᴜsᴇʀs ғᴏᴜɴᴅ.")
    else:
        await hehe.edit_text(text)
