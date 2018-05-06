import json
import discord
from discord.ext import commands

class Admin:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def grant(self, context, member: discord.Member, scope: str = None):
        author_id = context.message.author.id
        server_id = context.message.server.id

        if scope == 'global':
            if not self.bot.is_admin(author_id):
                await self.bot.reply('error: Granting global priviledges requires global priviledges.')
                await self.bot.doubt(context.message)
                return
            self.bot.update_or_create_user(member.id, {'super_admin': True})
            self.bot.db.commit()
            # await self.bot.reply('successfully granted {} global priviledges.'.format(member))
            await self.bot.ok(context.message)
            return
        if not self.bot.is_admin(author_id, server_id) and not self.bot.is_admin(author_id):
            await self.bot.reply('error: Granting bot admins priviledges requires either bot admin priviledges or global priviledges.')
            await self.bot.doubt(context.message)
            return

        bot_admins = self.bot.get_or_create_server(server_id, 'bot_admins')['bot_admins']
        if bot_admins:
            bot_admins = json.loads(bot_admins)
        else:
            bot_admins = []
        if member.id in bot_admins:
            bot_admins.remove(member.id)
            await self.bot.reply('Demoting {}'.format(member))
        else:
            bot_admins.append(member.id)
            await self.bot.reply('Promoting {}'.format(member))
        self.bot.update_server(server_id, {'bot_admins': json.dumps(bot_admins)})
        self.bot.db.commit()
        await self.bot.ok(context.message)

    @commands.command(pass_context=True)
    async def admins(self, context):
        server = context.message.server
        global_admins = []
        server_admins = self.bot.get_server(context.message.server.id, 'bot_admins')
        if server_admins and server_admins['bot_admins']:
            server_admins = json.loads(server_admins['bot_admins'])
        else:
            server_admins = []
        for member in context.message.server.members:
            data = self.bot.get_user(member.id, 'super_admin')
            if data and data['super_admin']:
                global_admins.append(member.id)

        if len(global_admins) + len(server_admins) is 0:
            await self.bot.reply('there is no bot admin on this server.')
            return
        msg = ''
        if global_admins:
            msg += 'Global bot admins on this server:\n'
            msg += self.bot.users_id_to_server_list(global_admins, server)
        if server_admins:
            msg += 'Local bot admins on this server:\n'
            msg += self.bot.users_id_to_server_list(server_admins, server)
        await self.bot.say(msg)
        await self.bot.check(context.message)
