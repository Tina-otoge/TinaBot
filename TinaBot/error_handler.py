import traceback
from discord.ext import commands

class CommandErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, context):

        ignored = (commands.CommandNotFound)

        if hasattr(context.command, 'on_error') or isinstance(error, ignored):
            return

        # await self.bot.send_message(context.message.channel, '{0.mention}, {1}\n{2}'.format(context.message.author, error, traceback.format_tb(error.__traceback__)))
        await self.bot.send_message(context.message.channel, '{0.mention}, {1}'.format(context.message.author, error))
        await self.bot.doubt(context.message)
