class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6584789596"
    sudo_users = "6584789596", "2010819209", "5702598840", "6764240805", "6101457748", "6154972031", "6100011620", "6412447141", "1643054031"
    GROUP_ID = -1002214016605
    TOKEN = "6639816047:AAERIAvgZV2iJQMqmTw1l1_9ZBhuigyOTiE"
    mongo_url = ""
    PHOTO_URL = ["https://telegra.ph/file/ed23556d07d33db18402d.jpg", "https://telegra.ph//file/e64337bbc6cdac7e6b178.jpg"]
    SUPPORT_CHAT = "Grabbing_Your_WH_Group"
    UPDATE_CHAT = "FLEX_BOTS_NEWS"
    BOT_USERNAME = "Grabbing_Your_Waifu_XBot"
    CHARA_CHANNEL_ID = "-1002214016605"
    api_id = 24089031
    api_hash = "0615e3afe13ddaaf8e9ddbd3977d35ff"

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