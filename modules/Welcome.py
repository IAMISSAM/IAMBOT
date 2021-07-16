import discord
from discord.ext import commands

from core.BaseModule import BaseModule
from core.Config import ConfigType


class Welcome(BaseModule):
    def __init__(self, bot):
        super().__init__(bot)
        self.welcome_channel = self.create_config(
            name='WelcomeChannel',
            description='Salon où indiquer les arrivées et départs.',
            config_type=ConfigType.CHANNEL,
            required=True
        )
        self.join_message = self.create_config(
            name='JoinMessage',
            default='@m a rejoint le serveur.',
            description='Message a envoyer quand un membre rejoint le serveur.\n**@m** mention | **@u** nom d\'utilisateur'
        )
        self.leave_message = self.create_config(
            name='LeaveMessage',
            default='@u a quitté le serveur.',
            description='Message a envoyer quand un membre quitte le serveur.\n**@m** mention | **@u** nom d\'utilisateur'
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not self.is_enabled(member.guild.id):
            return
        welcome_channel_id = self.welcome_channel[member.guild.id]
        await self.bot.get_channel(welcome_channel_id).send(
            self.join_message[member.guild.id].replace('@m', member.mention).replace('@u', str(member))
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.is_enabled(member.guild.id):
            return
        welcome_channel_id = self.welcome_channel[member.guild.id]
        await self.bot.get_channel(welcome_channel_id).send(
            self.leave_message[member.guild.id].replace('@m', member.mention).replace('@u', str(member))
        )


def setup(bot):
    bot.add_cog(Welcome(bot))
