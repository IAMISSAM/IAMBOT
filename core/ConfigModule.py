from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import Context, MemberConverter, TextChannelConverter, ChannelNotFound, UserNotFound

from core.Config import config_to_string, ConfigType


class ConfigModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: Context):
        return ctx.guild is not None and getattr(ctx.author.guild_permissions, 'administrator')

    @commands.group(invoke_without_command=True)
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

    @modules.command()
    async def enable(self, ctx: Context, module_name):
        module = get_real_module_name(self.bot, module_name)
        if module is None:
            await ctx.send(f'Module **{module_name}** invalide.')
            return
        if self.bot.config.has_missing_required_config(ctx.guild.id, module):
            await ctx.send(f'Des paramètres requis sont manquants pour activer le module **{module}**.')
        else:
            self.bot.config.set("_enabled", ctx.guild.id, True, module)
            await ctx.send(f'Module **{module}** activé :white_check_mark:')

    @modules.command()
    async def disable(self, ctx: Context, module_name):
        module = get_real_module_name(self.bot, module_name)
        if module is None:
            await ctx.send(f'Module **{module_name}** invalide.')
            return
        self.bot.config.set("_enabled", ctx.guild.id, False, module)
        await ctx.send(f'Module **{module}** désactivé :x:')

    @commands.group(invoke_without_command=True)
    async def config(self, ctx: Context, module_name: str):
        module = next((e[8:] for e in self.bot.extensions if e[8:].lower() == module_name.lower()), None)
        if module is None:
            await ctx.send(f'Module **{module_name}** invalide.')
            return
        description = ""
        configs = self.bot.config.get_module_configs(module)
        if len(configs) == 0:
            await ctx.send(f'Aucune configuration pour le module **{module}**')
        else:
            for config in configs:
                description += config_to_string(configs[config], ctx)
            embed = Embed(title=f'Configuration du module **{module}**:', colour=Colour(0xFABC20),
                          description=description)
            if any(configs[c].required for c in configs):
                embed.set_footer(text="* Paramètre requis")
            await ctx.send(embed=embed)

    @config.command("reset")
    async def reset_config(self, ctx, module_name, config_name):
        module = get_real_module_name(self.bot, module_name)
        if module is None:
            await ctx.send(f'Module **{module_name}** invalide.')
            return
        configs = self.bot.config.get_module_configs(module)
        if config_name not in configs:
            await ctx.send(f'Paramètre **{config_name}** invalide.')
            return
        del configs[config_name][ctx.guild.id]
        await ctx.send(f'Paramètre **{config_name}** reinitialisé.')
        if self.bot.config.has_missing_required_config(ctx.guild.id, module):
            self.bot.config.set("_enabled", ctx.guild.id, False, module)

    @config.command("set")
    async def set_config(self, ctx, module_name, config_name, arg):
        module = get_real_module_name(self.bot, module_name)
        if module is None:
            await ctx.send(f'Module **{module_name}** invalide.')
            return
        configs = self.bot.config.get_module_configs(module)
        if config_name not in configs:
            await ctx.send(f'Paramètre **{config_name}** invalide.')
            return
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

    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx: Context):
        await ctx.send(f'Le préfixe actuel est : **{self.bot.prefix[ctx.guild.id]}**')

    @prefix.command("reset")
    async def prefix_reset(self, ctx: Context):
        del self.bot.prefix[ctx.guild.id]
        await ctx.send(f'Le préfixe a été reinitialisé.')

    @prefix.command("set")
    async def prefix_set(self, ctx: Context, value):
        self.bot.prefix[ctx.guild.id] = value
        await ctx.send(f'Le préfixe a été modifié pour **{value}**.')


def get_real_module_name(bot, module_name):
    return next((e[8:] for e in bot.extensions if e[8:].lower() == module_name.lower()), None)
