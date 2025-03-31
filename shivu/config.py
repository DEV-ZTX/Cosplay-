class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "8177810307"
    sudo_users = "7757912959", "7678359785"
    GROUP_ID = -1002653736596
    TOKEN = "7964376351:AAFydh26PEkefcCIocN9KSEz0oH61lCLcv4"
    mongo_url = "mongodb+srv://Lord_ichigo:Roshni@cluster0.ytuss.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://telegra.ph/file/ed23556d07d33db18402d.jpg", "https://telegra.ph//file/e64337bbc6cdac7e6b178.jpg"]
    SUPPORT_CHAT = "Indian_Anime_Chat_Group"
    UPDATE_CHAT = "Beast_Tuhin"
    BOT_USERNAME = "CosplayGusserBot"
    BOT_NAME = "𝗚𝘂𝗲𝘀𝘀 𝗧𝗵𝗲 𝗖𝗼𝘀𝗽𝗹𝗮𝘆 ꕥ"
    CHARA_CHANNEL_ID = "-1002673491787"
    api_id = 23568641
    api_hash = "a39098e8752a45c2d6d1889941547bbc"

    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
