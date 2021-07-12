import os

import discord

from core.BaseBot import IAMBOT

bot = IAMBOT(
    command_prefix='?',
    case_insensitive=True,
    owner_id=853589947209482281,
    intents=discord.Intents.default()
)

if __name__ == '__main__':
    bot.run(os.getenv('IAMBOT_TOKEN'))
