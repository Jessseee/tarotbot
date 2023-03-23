import random

import discord
from asyncio import sleep
from io import BytesIO
from deck import Deck, display_three_cards, three_cards_sentiment

from views import Confirm


class Conversation:
    def __init__(self, init_message):
        self.init_message = init_message
        self.user = init_message.author
        self.channel = init_message.channel
        self.intro = ['Good day ', 'How are you doing ', 'Feeling fortunate today ','Have you ever considered your dreams ']
        self.drawtext = ['Aaah hmm I see']
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
            await self.respond(f'{random.choice(self.intro)} {self.user.mention}, would you like me to read your cards?', view=confirm)
            await confirm.wait()
            if confirm.confirmed:
                await self.draw3()
            else:
                await self.respond(random.choice(["Alright, maybe some other time.", "That's perfectly okay. My services are only for those who seek them, and I respect your decision not to have a reading today.",
                                                  "I understand that not everyone believes in the power of tarot. If you ever change your mind, I will be here to offer my guidance.",
                                                  "I appreciate your honesty. Tarot readings are a personal choice, and I'm always here to help those who are open to receiving my insights.",
                                                  "No problem at all. Tarot readings can be a bit intimidating, and I understand that not everyone is ready for that kind of experience.",
                                                  "Of course, I completely respect your decision. If you ever have any questions or concerns, feel free to reach out to me at any time."]))

    async def draw3(self):
        deck = Deck()
        cards = deck.draw3()
        image = display_three_cards(cards)
        draw_middle = ["which means", "that entails", "corresponds to", "which describes"]
        card_number = {
            0: "Yes I see, your past card",
            1: 'let met say, your present card',
            2: 'certainly interesting! Your future card '
        }
        with BytesIO() as buf:
            image.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename="tarot-draw.png")

        await self.respond(f"Here is your draw!", file=file)
        for index, card in enumerate(cards) :
            await self.respond(f' {card_number.get(index)} is {card.name.replace("_"," ")}, {random.choice(draw_middle)} {" & ".join([", ".join(card.desc[:-1]),card.desc[-1]])} ')
