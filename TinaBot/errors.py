from discord.ext import commands

class PriviledgeException(commands.CommandError):
    def __init__(self, message=None, *args):
        if message is None:
            message = 'insufficient priviledge.'
        super().__init__(message, *args)
