import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.discord_helpers import delete_invocation
from core.loggee import Loggee


class Status(Cog_Extension):
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await delete_invocation(ctx)
        Loggee(f"『指令』〔{ctx.author}〕 輸入 [shutdown - 機器人關機] 指令")
        await ctx.send("【狀態】掰掰 我已關機")
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def online(self, ctx):
        await delete_invocation(ctx)
        await ctx.send("【狀態】你好 我已經啟動!")
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name="我現在不知道要幹嘛...."),
        )

    @commands.command()
    @commands.is_owner()
    async def idle(self, ctx):
        await delete_invocation(ctx)
        await ctx.send("【狀態】我太懶了 不想做事!")
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name="ψ(｀∇´)ψ"),
        )

    @commands.command()
    @commands.is_owner()
    async def dnd(self, ctx):
        await delete_invocation(ctx)
        await ctx.send("【狀態】不要打擾我")
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name="不要吵我"),
        )

    @commands.command()
    @commands.is_owner()
    async def inv(self, ctx):
        await delete_invocation(ctx)
        await self.bot.change_presence(status=discord.Status.invisible)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        await delete_invocation(ctx)
        await ctx.send("【狀態】機器人測試中 請勿打擾")
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name="機器人測試中"),
        )

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, state, *, name=None):
        await delete_invocation(ctx)
        name = name or "ヾ(•ω•`)o"
        states = {
            "online": (discord.Status.online, "線上"),
            "線上": (discord.Status.online, "線上"),
            "idle": (discord.Status.idle, "閒置"),
            "dnd": (discord.Status.dnd, "請勿打擾"),
        }
        selected = states.get(state)
        if selected is None:
            await ctx.send("『ERROR』狀態可用: online, idle, dnd")
            return

        discord_status, label = selected
        await self.bot.change_presence(
            status=discord_status,
            activity=discord.Activity(type=discord.ActivityType.watching, name=name),
        )
        await ctx.send(f"【狀態】目前狀態:{label} 目前狀態消息:{name}")


async def setup(bot):
    await bot.add_cog(Status(bot))
