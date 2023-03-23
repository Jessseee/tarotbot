import discord
from asyncio import sleep
from io import BytesIO
from deck import Deck, display_three_cards
from views import Confirm


class Conversation:
    def __init__(self, init_message):
        self.init_message = init_message
        self.user = init_message.author
        self.channel = init_message.channel

    async def respond(self, msg, *, file=None, view=None, timeout=1):
        async with self.channel.typing():
            await sleep(timeout)
            await self.channel.send(msg, view=view, file=file)

    async def start(self):
        if any(word in self.init_message.content for word in ['card', 'cards', 'read', 'reading']):
            await self.respond(f'Good day {self.user.mention}, I will gladly read your cards!')
            await sleep(1)
        else:
            confirm = Confirm()
            await self.respond(f'Hello {self.user.mention}, would you like me to read your cards?', view=confirm)
            await confirm.wait()
            if confirm.confirmed:
                await self.draw3()
            else:
                await self.respond("Alright, maybe some other time.")

    async def draw3(self):
        deck = Deck()
        cards = deck.draw3()
        image = display_three_cards(cards)
        with BytesIO() as buf:
            image.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename="tarot-draw.png")
        await self.respond(f"Here is your draw!", file=file)
