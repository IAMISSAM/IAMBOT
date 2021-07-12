from discord.ext import commands

from core.Config import ConfigType


class BaseModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_config(self, name, config_type=ConfigType.STR, default=None, required=False, description=None):
        return self.bot.config.add(name, config_type, default, required,
                                   description, self.qualified_name)
