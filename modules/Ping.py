from discord.ext import commands

from core.BaseModule import BaseModule


class Ping(BaseModule):
    def __init__(self, bot):
        super().__init__(bot)
        self.ping_message = self.create_config('PingMessage', default='Pong!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(self.ping_message[ctx.guild.id])


def setup(bot):
    bot.add_cog(Ping(bot))
