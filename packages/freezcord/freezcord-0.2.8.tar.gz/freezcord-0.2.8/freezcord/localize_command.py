import discord


def localize_commands(
        commands: list[discord.ApplicationCommand | discord.SlashCommandGroup],
        lang: str,
        translations: dict,
        default_lang: str
):
    """Localize a list of slash commands or command groups."""
    for command in commands:
        localize_command(command, lang, translations.get(command.name, {}), default_lang)


def localize_command(
        cmd: discord.ApplicationCommand | discord.SlashCommandGroup,
        lang: str,
        translations: dict,
        default_lang: str
):
    """Apply localization to a single slash command or a command group."""

    if isinstance(cmd, discord.SlashCommandGroup):
        for sub_cmd in cmd.walk_commands():
            localize_command(sub_cmd, lang, translations.get(sub_cmd.name, {}), default_lang)

    localized_name = translations.get("name")
    if localized_name:
        if lang == default_lang:
            cmd.name = localized_name

        if cmd.name_localizations is discord.MISSING:
            cmd.name_localizations = {lang: localized_name}
        else:
            cmd.name_localizations[lang] = localized_name

    if not isinstance(cmd, discord.SlashCommand):
        return

    localized_desc = translations.get("description")
    if localized_desc:
        if lang == default_lang:
            cmd.description = localized_desc

        if cmd.description_localizations is discord.MISSING:
            cmd.description_localizations = {lang: localized_desc}
        else:
            cmd.description_localizations[lang] = localized_desc

    options_data = translations.get("options", {})
    for opt_name, opt_translation in options_data.items():
        opt = discord.utils.get(cmd.options, name=opt_name)
        if opt:
            opt_localized_name = opt_translation.get("name")
            if opt_localized_name:
                if lang == default_lang:
                    opt.name = opt_localized_name

                if opt.name_localizations is discord.MISSING:
                    opt.name_localizations = {lang: opt_localized_name}
                else:
                    opt.name_localizations[lang] = opt_localized_name

            opt_localized_desc = opt_translation.get("description")
            if opt_localized_desc:
                if lang == default_lang:
                    opt.description = opt_localized_desc

                if opt.description_localizations is discord.MISSING:
                    opt.description_localizations = {lang: opt_localized_desc}
                else:
                    opt.description_localizations[lang] = opt_localized_desc

            opt_choices_data = opt_translation.get("choices", {})
            for choice in opt.choices:
                if isinstance(choice, str):
                    choice = discord.OptionChoice(name=choice)

                localized_choice_name = opt_choices_data.get(choice.name)
                if localized_choice_name:
                    if lang == default_lang:
                        choice.name = localized_choice_name

                    if choice.name_localizations is discord.MISSING:
                        choice.name_localizations = {lang: localized_choice_name}
                    else:
                        choice.name_localizations[lang] = localized_choice_name
