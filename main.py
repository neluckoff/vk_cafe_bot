from vkbottle.bot import Bot, Message
from vkbottle import load_blueprints_from_package
from data.config import BOT_TOKEN, group_id


if __name__ == "__main__":
    bot = Bot(BOT_TOKEN, group_id)
    bot.labeler.vbml_ignore_case = True

    for bp in load_blueprints_from_package("commands"):
        bp.load(bot)

    bot.run_forever()
