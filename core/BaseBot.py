from discord.ext import commands

from core.Config import ConfigDatabase


class IAMBOT(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.config = ConfigDatabase()
        self.prefix = self.config.add("prefix", default='?')

        @self.event
        async def on_ready():
            for guild in self.guilds:
                self.config.loads(guild.id)

            print(f'Connecté en tant que {self.user} sur {len(self.guilds)} serveurs.')
