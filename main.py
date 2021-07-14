import os

import discord
from discord.ext import commands

from core.BaseBot import IAMBOT


def get_prefix(iambot, msg):
    return commands.when_mentioned(iambot, msg) + (
        list(iambot.prefix[msg.guild.id]) if msg.guild is not None else list('?'))


bot = IAMBOT(
    command_prefix=get_prefix,
    case_insensitive=True,
    owner_id=853589947209482281,
    intents=discord.Intents.default()
)

if __name__ == '__main__':
    for ext in os.listdir("./modules/"):
        if ext.endswith(".py") and not ext.startswith("_"):
            try:
                module_name = ext[:-3]
                bot.load_extension(f'modules.{module_name}')
                print(f'Module {module_name} chargé')
            except Exception as e:
                print(e)

    bot.run(os.getenv('IAMBOT_TOKEN'))
