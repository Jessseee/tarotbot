import discord
from discord.ext import commands
from conversation import Conversation

description = """Will pull a number of tarot cards for you."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned, description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(msg):
    if not msg.author.bot and bot.user.mentioned_in(msg):
        conv = Conversation(msg)
        await conv.start()


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    token = getenv('TOKEN')

    bot.run(token)
