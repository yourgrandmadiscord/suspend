import discord
from discord.ext import commands

from core import checks
from core.checks import PermissionLevel


class SuspendThread(commands.Cog):
    """Allows supporters to suspend a thread."""
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)


    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    @commands.command()
    async def suspend(self, ctx):
        thread = await self.db.find_one({'thread_id': str(ctx.thread.channel.id)})
        await self.db.delete_one(thread)
        await ctx.send('lmao tom is an L.')
        await ctx.send('fr')


async def setup(bot):
    await bot.add_cog(SuspendThread(bot))
