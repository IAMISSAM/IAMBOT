from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import Context, MemberConverter, TextChannelConverter, ChannelNotFound, UserNotFound

from core.Config import config_to_string, ConfigType


class ConfigModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def modules(self, ctx: Context):
        description = ""

        for module in [e[8:] for e in self.bot.extensions]:
            emoji = 'white_check_mark' if self.bot.config.get_or("_enabled", ctx.guild.id, False, module) else 'x'
            description += f'**{module}** :{emoji}:\n'

        if len(description) == 0:
            await ctx.send("Aucun module disponible.")
        else:
            embed = Embed(title="Liste des modules:", colour=Colour(0xFABC20),
                          description=description)
            await ctx.send(embed=embed)

    @commands.command()
    async def enable(self, ctx: Context, module_name):
        if module_name not in [e[8:] for e in self.bot.extensions]:
            await ctx.send(f'Module **{module_name}** invalide.')
        else:
            if self.bot.config.has_missing_required_config(ctx.guild.id, module_name):
                await ctx.send(f'Des paramètres requis sont manquants pour activer le module **{module_name}**.')
            else:
                self.bot.config.set("_enabled", ctx.guild.id, True, module_name)
                await ctx.send(f'Module **{module_name}** activé :white_check_mark:')

    @commands.command()
    async def disable(self, ctx: Context, module_name):
        if module_name not in [e[8:] for e in self.bot.extensions]:
            await ctx.send(f'Module **{module_name}** invalide.')
        else:
            self.bot.config.set("_enabled", ctx.guild.id, False, module_name)
            await ctx.send(f'Module **{module_name}** désactivé :x:')

    @commands.command("config")
    async def config(self, ctx: Context, module_name: str, action=None, config_name=None, *, arg=None):
        if module_name not in [e[8:] for e in self.bot.extensions]:
            await ctx.send(f'Module **{module_name}** invalide.')
        else:
            if action is None:
                await self.print_module_info(ctx, module_name)
            elif action == "reset" and config_name is not None:
                await self.reset_config(ctx, module_name, config_name)
            elif action == "set" and config_name is not None and arg is not None:
                await self.set_config(ctx, module_name, config_name, arg)

    async def print_module_info(self, ctx, module_name):
        description = ""
        configs = self.bot.config.get_module_configs(module_name)
        if len(configs) == 0:
            await ctx.send(f'Aucune configuration pour le module **{module_name}**')
        else:
            for config in configs:
                description += config_to_string(configs[config], ctx)
            embed = Embed(title=f'Configuration du module **{module_name}**:', colour=Colour(0xFABC20),
                          description=description)
            if any(configs[c].required for c in configs):
                embed.set_footer(text="* Paramètre requis")
            await ctx.send(embed=embed)

    async def reset_config(self, ctx, module_name, config_name):
        configs = self.bot.config.get_module_configs(module_name)
        if config_name not in configs:
            await ctx.send(f'Paramètre **{config_name}** invalide.')
        else:
            del configs[config_name][ctx.guild.id]
            await ctx.send(f'Paramètre **{config_name}** reinitialisé.')
            if self.bot.config.has_missing_required_config(ctx.guild.id, module_name):
                self.bot.config.set("_enabled", ctx.guild.id, False, module_name)

    async def set_config(self, ctx, module_name, config_name, arg):
        configs = self.bot.config.get_module_configs(module_name)
        if config_name not in configs:
            await ctx.send(f'Paramètre **{config_name}** invalide.')
        else:
            try:
                config = configs[config_name]
                value = arg
                if config.config_type == ConfigType.INT:
                    value = int(arg)
                if config.config_type == ConfigType.BOOL:
                    value = arg.lower() in ["true", "t", "vrai", "v", "oui", "o", "yes", "y"]
                if config.config_type == ConfigType.USER:
                    member = await MemberConverter().convert(ctx, arg)
                    value = member.id
                if config.config_type == ConfigType.CHANNEL:
                    channel = await TextChannelConverter().convert(ctx, arg)
                    value = channel.id
                config[ctx.guild.id] = value
                await ctx.send(f'Paramètre **{config_name}** modifié.')
            except (ValueError, ChannelNotFound, UserNotFound):
                await ctx.send(f'Valeur **{arg}** invalide.')
