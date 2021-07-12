from discord.ext import commands

from core.Config import ConfigDatabase
from core.ConfigModule import ConfigModule


class IAMBOT(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.config = ConfigDatabase()
        self.prefix = self.config.add("prefix", default='?')
        self.add_cog(ConfigModule(self))

        @self.event
        async def on_ready():
            for guild in self.guilds:
                self.config.loads(guild.id)

            # Auto disable module if required config is missing
            for module in [e[8:] for e in self.extensions]:
                for guild in self.guilds:
                    if self.config.has_missing_required_config(guild.id, module):
                        self.config.set("_enabled", guild.id, False, module)

            print(f'Connecté en tant que {self.user} sur {len(self.guilds)} serveurs.')
