import discord
import requests
import importlib
import traceback
from colorama import Fore, Style, init


class Bot(discord.Bot):
    def __init__(self, token, error_handler_webhook=None, intents=None,lang=None, *args, **kwargs):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
        super().__init__(intents=intents, *args, **kwargs)
        self.token = token
        self.error_handler_webhook = error_handler_webhook
        self._cogs = {}
        self.lang = lang

    async def print_info(self):
        bot_name = str(Bot.user)
        bot_id = Bot.user.id
        pycord_version = discord.__version__
        commands_count = len(Bot.commands)
        guilds_count = len(Bot.guilds)
        latency = round(Bot.latency * 1000, 2)
        if self.lang is None or self.lang=="en":
         print(Fore.BLUE + "[FREEZCORD]" + Fore.WHITE + " Bot is "+ Fore.GREEN + "online.")
        elif self.lang=="de":
           print(Fore.BLUE + "[FREEZCORD]" + Fore.WHITE + " Bot ist " + Fore.GREEN + "online.")
        else:
            print(Fore.BLUE + "[FREEZCORD]" + Fore.WHITE + " Bot is "+ Fore.GREEN + "online.")
        print(Fore.WHITE + "╭────────────────┬─────────────────────┬────────┬──────────┬────────┬─────────╮")
        print(Fore.WHITE + "╭────────────────┬─────────────────────┬────────┬──────────┬────────┬─────────╮")
        print(
            Fore.WHITE + "│ " + Fore.WHITE + "Bot" + Fore.WHITE + "            │ " + Fore.WHITE + "ID" + Fore.WHITE + "                  │ " + Fore.WHITE + "Pycord" + Fore.WHITE + " │ " + Fore.WHITE + "Commands" + Fore.WHITE + " │ " + Fore.WHITE + "Guilds" + Fore.WHITE + " │ " + Fore.WHITE + "Latency" + Fore.WHITE + " │")
        print(Fore.WHITE + "│────────────────┼─────────────────────┼────────┼──────────┼────────┼─────────│")
        print(
            Fore.WHITE + f"│ {Fore.BLUE}{bot_name:<14}{Fore.CYAN} │ {Fore.BLUE}{bot_id:<19}{Fore.CYAN} │ {Fore.BLUE}{pycord_version:<6}{Fore.CYAN} │ {Fore.BLUE}{commands_count:<8}{Fore.CYAN} │ {Fore.BLUE}{guilds_count:<6}{Fore.CYAN} │ {Fore.BLUE}{latency}ms{Fore.CYAN} │"
        )
        print(Fore.WHITE + "╰────────────────┴─────────────────────┴────────┴──────────┴────────┴─────────╯")
        print(Fore.WHITE + "╰────────────────┴─────────────────────┴────────┴──────────┴────────┴─────────╯")

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        print(f'Bot ist bereit und angemeldet als {self.user}')
        await self.register_cogs()
        await self.print_info()

    async def register_cogs(self):
        for cog_name, cog in self._cogs.items():
            await cog.initialize(self)

    def load_cog(self, cog_name):
        module = importlib.import_module(f'cogs.{cog_name}')
        cog = module.Cog()
        self._cogs[cog_name] = cog
        return cog

    async def status(self, activity=None, text=None):
        if activity is None and text is None:
            return

        if activity == "playing":
            activity_type = discord.Game(name=text)
        elif activity == "watching":
            activity_type = discord.Streaming(name=text, url="https://www.twitch.tv/")
        elif activity == "listening":
            activity_type = discord.Activity(type=discord.ActivityType.listening, name=text)
        else:
            activity_type = None

        if activity_type:
            await self.change_presence(activity=activity_type)

    async def send_error(self, error, guild, user):
        if self.error_handler_webhook:
            embed = discord.Embed(
                title="Error Report",
                description=f"- Guild: {guild.name} ({guild.id})\n- User: {user.name} ({user.id})\n\n```py\n{error}\n```",
                color=discord.Color.red()
            )
            requests.post(self.error_handler_webhook, json={"embeds": [embed.to_dict()]})

    async def on_error(self, event, *args, **kwargs):
        error_info = traceback.format_exc()
        print(error_info)
        guild = args[0].guild if event == "on_message" and args else None
        user = args[0].author if event == "on_message" and args else None

        await self.send_error(error_info, guild, user)