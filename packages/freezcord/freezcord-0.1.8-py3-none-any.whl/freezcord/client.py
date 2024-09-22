import discord

class Client(discord.Client):
    def __init__(self, intents, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)



    def run(self, token):
        super().run(token)
