def avatar_url(user):
    return str(user.display_avatar.url)


def guild_icon_url(guild):
    if guild.icon is None:
        return ""
    return str(guild.icon.url)
