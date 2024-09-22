import discord

class Client(discord.Client):
    def __init__(self, intents, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)

    async def on_ready(self):
        print(f'Angemeldet als {self.user}')

    def run(self, token):
        super().run(token)
