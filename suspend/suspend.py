from discord.ext import commands
from discord import PermissionOverwrite

class SuspendPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dictionary to store suspended threads (thread_id: bool)
        self.suspended_threads = {}

    @commands.command(name="suspend")
    @commands.has_permissions(manage_channels=True)
    async def suspend(self, ctx):
        """Suspends a thread, making it read-only and disabling commands."""
        if ctx.channel.id in self.suspended_threads:
            await ctx.send("This thread is already suspended.")
            return

        # Mark the thread as suspended
        self.suspended_threads[ctx.channel.id] = True

        # Remove the ability for users to send messages in this channel
        overwrite = PermissionOverwrite()
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        # You can add a "closed" tag or change the channel's name to indicate suspension
        await ctx.channel.edit(name=f"{ctx.channel.name}-suspended")

        await ctx.send(f"Thread '{ctx.channel.name}' has been suspended.")

    @commands.command(name="unsuspend")
    @commands.has_permissions(manage_channels=True)
    async def unsuspend(self, ctx):
        """Unsuspends a thread, making it writable again."""
        if ctx.channel.id not in self.suspended_threads:
            await ctx.send("This thread is not suspended.")
            return

        # Remove the suspended state
        del self.suspended_threads[ctx.channel.id]

        # Restore the ability for users to send messages in this channel
        overwrite = PermissionOverwrite()
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        # Restore the original thread name (optional)
        await ctx.channel.edit(name=ctx.channel.name.replace("-suspended", ""))

        await ctx.send(f"Thread '{ctx.channel.name}' has been unsuspended.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Prevent users from sending messages in suspended threads."""
        if message.channel.id in self.suspended_threads:
            # Delete the message if the thread is suspended
            await message.delete()
            await message.channel.send(f"Thread is suspended. No messages allowed.", delete_after=5)

def setup(bot):
    bot.add_cog(SuspendPlugin(bot))
