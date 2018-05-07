import traceback
from discord.ext import commands
class CommandErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, context):

        ignored = (commands.CommandNotFound)
        public = (commands.BadArgument, commands.MissingRequiredArgument)

        if hasattr(context.command, 'on_error') or isinstance(error, ignored):
            return

        # await self.bot.send_message(context.message.channel, '{0.mention}, {1}\n{2}'.format(context.message.author, error, traceback.format_tb(error.__traceback__)))
        if isinstance(error, public):
            await self.bot.send_message(context.message.channel, '{0.mention}, {1}'.format(context.message.author, error))
        else:
            msg = ''
            for tb in traceback.format_tb(error.__traceback__):
                msg += tb
            await self.bot.send_message(self.bot.get_channel(self.bot.warnings), '{0} provoked an error on {1} :warning:\n{2}\n```\n{3}```'.format(context.message.author, context.message.server, error, msg))
        await self.bot.doubt(context.message)
