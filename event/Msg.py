from discord.ext import commands

from core.classes import Cog_Extension
from core.config import get_settings
from core.loggee import Loggee


KEYWORD_REPLIES = {
    "早安": "早安! 祝你有個美好的一天!",
    "早": "早安! 祝你有個美好的一天!",
    "大家早安": "早安! 祝你有個美好的一天!",
    "午安": "午安!",
    "睡午覺": "午安!",
    "晚安": "晚安! 祝你有個好夢!",
    "我先睡了": "晚安! 祝你有個好夢!",
    "?": "https://tenor.com/view/nick-young-question-mark-huh-what-confused-gif-4995479",
    "wtf": "https://tenor.com/view/nick-young-question-mark-huh-what-confused-gif-4995479",
    "嗨起來": "有人提到嗨起來嗎!?\nhttps://tenor.com/view/high-gif-5005257",
}


def _normalise(content):
    return content.strip().rstrip("!！?？").lower()


def _indecent_words():
    words = get_settings().get("Indecent_words") or []
    if isinstance(words, str):
        words = [item.strip() for item in words.split(",")]
    return {word.lower() for word in words if word}


class Msg(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        normalised = _normalise(msg.content)
        for keyword, reply in KEYWORD_REPLIES.items():
            if normalised == _normalise(keyword):
                await msg.channel.send(reply)
                Loggee(f"『訊息觸發』[{msg.author}] 觸發關鍵字 [{keyword}]")
                return

        if normalised in _indecent_words():
            try:
                await msg.delete()
            except Exception:
                pass
            await msg.channel.send(f"{msg.author.mention} 請勿輸入不雅詞語。", delete_after=8)
            Loggee(f"『訊息觸發』[{msg.author}] 觸發不雅詞語過濾")


async def setup(bot):
    await bot.add_cog(Msg(bot))
