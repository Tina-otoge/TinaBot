#!/usr/bin/env python3

from config import token
import TinaBot.bot

if __name__ == '__main__':
    bot = TinaBot.Bot(token)
    bot.run()
