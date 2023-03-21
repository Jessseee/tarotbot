import discord
from discord.ext import commands
from views import Confirm
from asyncio import sleep

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
    if msg.author.bot is False and bot.user.mentioned_in(msg):
        if any(word in msg.content for word in ['card', 'cards', 'read', 'reading']):
            async with msg.channel.typing():
                await sleep(1)
                await msg.channel.send(f'Good day {msg.author.mention}, I will gladly read your cards!')
        else:
            async with msg.channel.typing():
                await sleep(1)
                await msg.channel.send(f'Hello {msg.author.mention}, would you like me to read your cards?', view=Confirm())


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    token = getenv('TOKEN')

    bot.run(token)
