import random

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
        self.intro = ['Good day ', 'How are you doing ', 'Feeling fortunate today ','Hello']
        self.reading_invite = ["I would like to invite you to a tarot card draw session with me. It's an opportunity for you to gain insight and guidance about your life, and I believe it could be a transformative experience.",
                               "I've noticed that you've been going through a difficult time lately, and I think a tarot card draw session could help you find clarity and direction. Would you be interested in scheduling a session with me?",
                               "I've been honing my skills as a tarot reader for many years now, and I would love to share my knowledge and expertise with you. Would you be open to having a session with me?",
                               "I believe that tarot card readings are a powerful tool for self-discovery and personal growth. I would be honored to guide you through a session and help you uncover new insights about your life.",
                               "I know that some people are skeptical about tarot card readings, but I believe that if you approach it with an open mind, it can be an incredibly rewarding experience. Would you be willing to give it a try with me?"]
        self.drawtext = ['I have drawn the following cards for you',
                         'Perfectly! I have drawn the following',
                         'Here is your draw!',
                         'With all my might I present you the following cards!']
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
        draw_before_number = ["Yes I see your ", "let me say", "Certainly interesting! Your ", "It appears that" ]
        card_number = ["past card", 'present card', 'future card ']
        with BytesIO() as buf:
            image.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename="tarot-draw.png")

        await self.respond(f"Here is your draw!", file=file)
        for index, card in enumerate(cards):
            await self.respond(f' {random.choice(draw_before_number),card_number[index]} is {card.name.replace("_"," ")}, {random.choice(draw_middle)} {" & ".join([", ".join(card.desc[:-1]),card.desc[-1]])} ')
