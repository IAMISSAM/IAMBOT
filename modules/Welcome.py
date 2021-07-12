from discord.ext import commands

from core.BaseModule import BaseModule


class Welcome(BaseModule):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!')


def setup(bot):
    bot.add_cog(Welcome(bot))
