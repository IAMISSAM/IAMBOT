from discord.ext import commands

from core.Config import ConfigType


class BaseModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_config(self, name, config_type=ConfigType.STR, default=None, required=False, description=None):
        return self.bot.config.add(name, config_type, default, required,
                                   description, self.qualified_name)

    async def cog_check(self, ctx):
        return self.is_enabled(ctx.guild.id)

    def is_enabled(self, guild_id):
        return self.bot.config.get_or("_enabled", guild_id, False, self.qualified_name)
