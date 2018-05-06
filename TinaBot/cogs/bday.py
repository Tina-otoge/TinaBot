import discord
from discord.ext import commands
from time import strftime, strptime
from config import null_words, bday_print_format, bday_get_formats

class Bday:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bdays(self, context, n : int = 5):
        users_with_bday = []
        for member in context.server.members:
            user_data = self.bot.get_user(member.id, 'id, birthday')
            if user_data and user_data['birthday']:
                users_with_bday.append(user_data)
        await self.bot.reply('TODO')

    @commands.command(pass_context=True)
    async def bday(self, context, date = None):
        user_id = context.message.author.id
        time = None

        if date is None:
            user_data = self.bot.get_user(user_id, 'birthday')
            if user_data and user_data['birthday']:
                await self.bot.reply('your birthday is set to {}.'.format(strftime(bday_print_format, strptime(user_data['birthday'], '%Y-%m-%d'))))
            else:
                msg = 'you do not have a birthday date set yet.\n'
                msg += 'You can set one with !bday <your birthday>\n'
                msg += 'Supported formats:\n'
                for bday_format in bday_get_formats:
                    msg += '- {}\n'.format(bday_format)
                await self.bot.reply(msg)
            return
        if date in null_words and self.bot.get_user(user_id) is not None:
            self.bot.update_user(user_id, {"birthday": None})
            self.bot.db.commit()
            await self.bot.reply('successfully deleted your birthday.')
            return
        for get_format in bday_get_formats:
            try:
                time = strptime(date, get_format)
                break
            except ValueError as e:
                pass
        if time is not None:
            self.bot.update_or_create_user(user_id, {"birthday": strftime("%Y-%m-%d", time)})
            self.bot.db.commit()
            await self.bot.reply('your birthday is now set to {}. :birthday:'.format(strftime(bday_print_format, time)))
        else:
            await self.bot.reply('error: Invalid date.')

    @commands.command(pass_context=True)
    async def setbdaychan(self, context, channel: discord.Channel = None):
        await self.bot.reply('TODO')
