from discord.ext import commands


class IAMBOT(commands.Bot):
    def __init__(self, **options):
        super().__init__(options)

        @self.event
        async def on_ready():
            print(f'Connecté en tant que {self.user} sur {len(self.guilds)} serveurs.')
