def avatar_url(user):
    return str(user.display_avatar.url)


def guild_icon_url(guild):
    if guild.icon is None:
        return ""
    return str(guild.icon.url)


def moderation_problem(interaction, permission, *, member=None, role=None):
    """Why the caller may not do this to `member` / with `role`, or None when allowed.

    The bot acts with its own, usually higher, permissions. Without these checks
    a low-ranked moderator could use it to act on people and roles above them.
    """
    guild = interaction.guild
    actor = interaction.user
    if guild is None:
        return "這個指令只能在伺服器內使用。"
    if not getattr(interaction.permissions, permission, False):
        return "你沒有執行這個指令所需的權限。"
    is_owner = actor.id == guild.owner_id
    me = guild.me

    if member is not None:
        if member.id == guild.owner_id:
            return "不能對伺服器擁有者執行這個操作。"
        if member.id != actor.id and not is_owner and member.top_role >= actor.top_role:
            return "你不能對身分組與你相同或更高的成員執行這個操作。"
        if me is not None and member.id != me.id and member.top_role >= me.top_role:
            return "機器人的身分組不夠高，無法對這位成員執行這個操作。"

    if role is not None:
        if role.is_default() or role.managed:
            return "這個身分組由 Discord 或整合服務管理，無法手動指派。"
        if not is_owner and role >= actor.top_role:
            return "你不能操作與你最高身分組相同或更高的身分組。"
        if me is not None and role >= me.top_role:
            return "機器人的身分組不夠高，無法操作這個身分組。"

    return None
