from json import loads
import sqlite3
from discord.ext import commands
from . import cogs
from .error_handler import CommandErrorHandler

async def _react(bot, message, emoji):
    try:
        await bot.add_reaction(message, emoji)
    except discord.errors.NotFound:
        pass

def _dict_factory(cursor, row):
    result = {}
    for index, column in enumerate(cursor.description):
        result[column[0]] = row[index]
    return result

def _insert(bot, table, id):
    bot.db_cur.execute('INSERT INTO {}(`id`) VALUES (?)'.format(table), (id,))

def _get(bot, table, id, rows):
    bot.db_cur.execute('SELECT {} FROM {} WHERE `id`=?'.format(rows, table), (id,))
    return bot.db_cur.fetchone()

def _get_or_create(bot, table, id, rows):
    result = _get(bot, table, id, rows)
    if result is None:
        _insert(bot, table, id)
        bot.db.commit()
        result = _get(bot, table, id, rows)
    return result

def _update(bot, table, id, data):
    values = []
    sql = 'UPDATE {} SET '.format(table)
    for key, value in data.items():
        sql += '`{}` = ?, '.format(key)
        values.append(value)
    sql = sql[:-2] + ' WHERE `id`=?'
    values.append(id)
    bot.db_cur.execute(sql, tuple(values))

def _update_or_create(bot, table, id, data):
    if _get(bot, table, id, 'id') is None:
        _insert(bot, table, id)
    _update(bot, table, id, data)

class Bot (commands.Bot):

    def __init__(self, token, prefix='!', *args, **kwargs):
        super().__init__(*args, command_prefix=commands.when_mentioned_or('!'), **kwargs)
        self.token = token
        self.add_cog(cogs.Bday(self))
        self.add_cog(cogs.Admin(self))
        self.add_cog(CommandErrorHandler(self))

    def run(self):
        self.db = sqlite3.connect('TinaBot.db')
        self.db.row_factory = _dict_factory
        self.db_cur = self.db.cursor()
        with open('init.sql') as f:
            self.db_cur.executescript(f.read())
        super().run(self.token)
        self.db.close()

    async def on_ready(self):
        print('Online as {} ({})'.format(self.user, self.user.id))

    async def doubt(self, message):
        await _react(self, message, '\N{THINKING FACE}')

    async def ok(self, message):
        await _react(self, message, '\N{OK HAND SIGN}')

    async def check(self, message):
        await _react(self, message, '\N{RIGHTWARDS ARROW WITH HOOK}')

    def get_user(self, user_id, rows='*'):
        return _get(self, '`users`', user_id, rows)

    def get_server(self, server_id, rows='*'):
        return _get(self, '`servers`', server_id, rows)

    def get_or_create_user(self, user_id, rows='*'):
        return _get_or_create(self, '`users`', user_id, rows)

    def get_or_create_server(self, server_id, rows='*'):
        return _get_or_create(self, '`servers`', server_id, rows)

    def update_user(self, user_id, data):
        return _update(self, '`users`', user_id, data)

    def update_server(self, server_id, data):
        return _update(self, '`servers`', server_id, data)

    def update_or_create_user(self, user_id, data):
        return _update_or_create(self, '`users`', user_id, data)

    def update_or_create_server(self, server_id, data):
        return _update_or_create(self, '`servers`', server_id, data)

    def users_id_to_server_list(self, user_ids, server, extra = {}):
        result = ''
        for user_id in user_ids:
            member = server.get_member(user_id)
            result += '- {}'.format(member)
            if member.nick:
                result += ' ({})'.format(member.nick)
            if extra[user_id]:
                result += ' {}'.format(extra[user_id])
            result += '\n'

    def is_admin(self, user_id, server_id = None):
        if server_id is None:
            return self.get_user(user_id, 'super_admin')['super_admin'] == True
        server_data = self.get_server(server_id, 'bot_admins')
        return server_data and server_data['bot_admins'] is not None and user_id in loads(server_data['bot_admins'])
