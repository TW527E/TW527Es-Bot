import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.config import get_guild_configs, int_or_none
from core.discord_helpers import avatar_url
from core.loggee import Loggee


def _find_config(guild_id):
    for config in get_guild_configs():
        if config.get("guild_id") == guild_id:
            return config
    return None


async def _send_member_notice(bot, channel_id, title, member):
    channel_id = int_or_none(channel_id)
    channel = bot.get_channel(channel_id) if channel_id else None
    if channel is None:
        return

    embed = discord.Embed(title=title, color=0xD08A2B)
    embed.set_thumbnail(url=avatar_url(member))
    await channel.send(embed=embed)


class Member(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = _find_config(member.guild.id)
        if config is None:
            return

        Loggee(f"『{member}』 加入了《{member.guild.name}》伺服器")
        await _send_member_notice(
            self.bot,
            config.get("member_join_channel"),
            f"『{member}』 加入了伺服器",
            member,
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        config = _find_config(member.guild.id)
        if config is None:
            return

        Loggee(f"『{member}』 退出了《{member.guild.name}》伺服器")
        await _send_member_notice(
            self.bot,
            config.get("member_leave_channel"),
            f"『{member}』 退出了伺服器",
            member,
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None or payload.member is None:
            return

        config = _find_config(payload.guild_id)
        if config is None:
            return

        reaction_message_id = int_or_none(config.get("Reaction_Msg"))
        reaction_role_id = int_or_none(config.get("Reaction_Role"))
        reaction_emoji = str(config.get("Reaction_Emoji") or "")
        if payload.message_id != reaction_message_id or str(payload.emoji) != reaction_emoji:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(reaction_role_id) if guild and reaction_role_id else None
        if role is None:
            return

        await payload.member.add_roles(role, reason="Reaction role")
        Loggee(f"《{guild.name}》『{payload.member}』透過反應獲得《{role.name}》")
        try:
            await payload.member.send(f"《恭喜》你已獲得了《{role.name}》")
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return

        config = _find_config(payload.guild_id)
        if config is None:
            return

        reaction_message_id = int_or_none(config.get("Reaction_Msg"))
        reaction_role_id = int_or_none(config.get("Reaction_Role"))
        reaction_emoji = str(config.get("Reaction_Emoji") or "")
        if payload.message_id != reaction_message_id or str(payload.emoji) != reaction_emoji:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role = guild.get_role(reaction_role_id) if reaction_role_id else None
        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                return

        if role is None:
            return

        await member.remove_roles(role, reason="Reaction role removed")
        Loggee(f"《{guild.name}》『{member}』移除反應並失去《{role.name}》")


async def setup(bot):
    await bot.add_cog(Member(bot))
