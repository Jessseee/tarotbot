import discord
from discord.ext import commands
from views import Confirm
from asyncio import sleep
from deck import Deck

description = """Will pull a number of tarot cards for you."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned, description=description, intents=intents)


async def wait_typing(channel, timeout):
    async with channel.typing(): await sleep(timeout)


async def respond(channel, msg, view=None, timeout=1):
    await wait_typing(channel, timeout)
    await channel.send(msg, view=view)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(msg):
    if msg.author.bot or bot.user.mentioned_in(msg):
        pass
    elif any(word in msg.content for word in ['card', 'cards', 'read', 'reading']):
        await respond(msg.channel, f'Good day {msg.author.mention}, I will gladly read your cards!')
    else:
        await respond(msg.channel, f'Hello {msg.author.mention}, would you like me to read your cards?', view=Confirm())


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    token = getenv('TOKEN')

    deck = Deck()

    bot.run(token)
