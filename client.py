import discord
from discord.ext import commands
from views import Confirm
from asyncio import sleep
from io import BytesIO

from deck import Deck, display_three_cards

description = """Will pull a number of tarot cards for you."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned, description=description, intents=intents)


async def respond(ctx, msg, *, file=None, view=None, timeout=1):
    async with ctx.typing():
        await sleep(timeout)
        await ctx.send(msg, view=view, file=file)


async def draw3(ctx):
    cards = deck.draw3()
    image = display_three_cards(cards)
    with BytesIO() as buf:
        image.save(buf, "PNG")
        buf.seek(0)
        file = discord.File(fp=buf, filename="tarot-draw.png")
    await respond(ctx, f"Here is your draw!", file=file)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(msg):
    if not msg.author.bot and bot.user.mentioned_in(msg):
        ctx = msg.channel
        if any(word in msg.content for word in ['card', 'cards', 'read', 'reading']):
            await respond(ctx, f'Good day {msg.author.mention}, I will gladly read your cards!')
            await sleep(1)
            await draw3(ctx)
        else:
            confirm = Confirm()
            await respond(ctx, f'Hello {msg.author.mention}, would you like me to read your cards?', view=confirm)
            await confirm.wait()
            if confirm.confirmed: await draw3(ctx)
            else: await respond(ctx, "Alright, maybe some other time.")


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    token = getenv('TOKEN')

    deck = Deck()

    bot.run(token)
