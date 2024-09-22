import discord
import requests
import importlib
import traceback
import os
from colorama import Fore, Style, init


class Bot(discord.Bot):
    def __init__(self, token=None, error_handler_webhook=None, error_handler=False,intents=None, lang=None, *args, **kwargs):
        if token is None:
            return

        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
        super().__init__(intents=intents, *args, **kwargs)
        self.token = token
        self.error_handler_webhook = error_handler_webhook
        self._cogs = {}
        self.lang = lang
        self.error_handler=error_handler



    def run(self):
        super().run(self.token)

    def load_cogs(self,directory_name="cogs"):
        """
        Loads all cogs from the specified directory into the bot.

        Args:
            bot (discord.Bot): The bot object that should load the cogs.
            directory_name (str): The name of the directory where the cogs are located.
        """

        cogs_loaded = 0
        for filename in os.listdir(directory_name):
            if filename.endswith(".py"):
                try:
                    self.load_extension(f"{directory_name}.{filename[:-3]}")
                    cogs_loaded += 1
                    print(f"Loaded cog: {filename}")
                except Exception as e:
                    print(f"Error loading cog {filename}: {e}")
                    return

        print(f"Successfully loaded {cogs_loaded} cog(s).")

    async def on_ready(self):
        await self.register_cogs()



    async def status(self, activity=None, text=None,link=None):
        if activity is None and text is None:
         if self.lang is None or self.lang == "en":
          return print(
                Fore.BLUE + "[FREEZCORD] " + Fore.WHITE + "You need to provide a stream link for the bot status!" + Style.RESET_ALL)
         elif self.lang == "de":
            return print(
                    Fore.BLUE + "[FREEZCORD] " + Fore.WHITE + "Du musst einen Stream Link angeben für den Bot Status!" + Style.RESET_ALL)
         else:
             return print(
                    Fore.BLUE + "[FREEZCORD] " + Fore.WHITE + "You need to provide a stream link for the bot status!" + Style.RESET_ALL)
        if activity == "playing":
            activity_type = discord.Game(name=text)
        elif activity == "streaming":
            if link is None:
             if self.lang is None or self.lang=="en":
              return print(Fore.BLUE+"[FREEZCORD] "+Fore.WHITE+"You need to provide a stream link for the bot status!"+ Style.RESET_ALL)
             elif self.lang=="de":
                return print(Fore.BLUE + "[FREEZCORD] " + Fore.WHITE + "Du musst einen Stream Link angeben für den Bot Status!" + Style.RESET_ALL)
             else:
                 return print(Fore.BLUE + "[FREEZCORD] " + Fore.WHITE + "You need to provide a stream link for the bot status!" + Style.RESET_ALL)
            activity_type = discord.Streaming(name=text, url="https://www.twitch.tv/")
        elif activity == "listening":
            activity_type = discord.Activity(type=discord.ActivityType.listening, name=text)
        else:
            activity_type = None

        if activity_type:
            await self.change_presence(activity=activity_type)



    async def send_reply(self, interaction, error, guild=None, user=None, command_name=None):
        """
        Send an error message to the user who used the command, taking into account their Discord language setting,
        and prevent further command execution.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
            error (str): The error traceback as a string.
            guild (discord.Guild): The guild where the error occurred (or None).
            user (discord.User): The user who triggered the error (or None).
            command_name (str): The name of the command that caused the error (if applicable).
        """
        guild_name = guild.name if guild else 'None'
        guild_id = guild.id if guild else 'None'
        user_name = user.name if user else 'None'
        user_id = user.id if user else 'None'
        command_info = f"\n- Command: {command_name}" if command_name else ""

        if command_info is not None and self.error_handler==True:
         if user:
          user_locale = user.locale

          if user_locale == "de":
           error_message = f"Ein Fehler ist aufgetreten:"
          elif user_locale == "es":
             error_message = f"¡Se ha producido un error:"
          elif user_locale == "ru":
             error_message = f"Произошла ошибка:"
          else:
              error_message = f"An error occurred:"

          embed = discord.Embed(
          title="Error",
          description=f"{error_message}\n\n```py\n{error}\n```",
                color=discord.Color.red()
            )


         await interaction.response.send_message(embed=embed, ephemeral=True)

    async def send_error(self, error, guild=None, user=None, command_name=None):
        """
        Send an error report to the specified webhook. If `guild` or `user` is not available, 'None' will be used.

        Args:
            error (str): The error traceback as a string.
            guild (discord.Guild): The guild where the error occurred (or None).
            user (discord.User): The user who triggered the error (or None).
            command_name (str): The name of the command that caused the error (if applicable).
        """
        guild_name = guild.name if guild else 'None'
        guild_id = guild.id if guild else 'None'
        user_name = user.name if user else 'None'
        user_id = user.id if user else 'None'
        command_info = f"\n- Command: {command_name}" if command_name else ""

        if self.error_handler_webhook:
            embed = discord.Embed(
                title="Error Report",
                description=f"- Guild: {guild_name} ({guild_id})\n- User: {user_name} ({user_id}){command_info}\n\n```py\n{error}\n```",
                color=discord.Color.red()
            )

            requests.post(self.error_handler_webhook, json={"embeds": [embed.to_dict()]})

    async def on_error(self, event, *args, **kwargs):
        error_info = traceback.format_exc()
        print(error_info)

        interaction = None
        user = None
        guild = None
        command_name = None


        if event == "on_command_error":
            interaction = args[0].interaction if hasattr(args[0], 'interaction') else None
            user = args[0].author if hasattr(args[0], 'author') else None
            guild = args[0].guild if hasattr(args[0], 'guild') else None
            command_name = args[0].command.name if hasattr(args[0], 'command') else None
        elif hasattr(args[0], 'interaction'):
            interaction = args[0].interaction
            user = interaction.user if interaction else None
            guild = interaction.guild if interaction else None


        if interaction:

         await self.send_reply(interaction, error_info, user, command_name)


        await self.send_error(error_info, guild, user, command_name)