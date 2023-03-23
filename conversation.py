import random
import discord
from asyncio import sleep
from io import BytesIO
from deck import Deck, display_three_cards
from enum import IntEnum

from views import Confirm

text = {
    'description': "I am the mystical Lorelei, I will draw you three Tarot cards that will give you insight into your "
                   "past, present and future.",
    'start': {
        'intro': ['Good day ', 'How are you doing ', 'Feeling fortunate today ', 'Hello'],
        'invite': [
            "I would like to invite you to a tarot card session with me. It's an opportunity for you to gain "
            "insight and guidance about your life, and I believe it could be a transformative experience.",
            "I've noticed that you've been going through a difficult time lately, and I think a tarot card draw "
            "session could help you find clarity and direction. Would you be interested in scheduling a session with "
            "me?",
            "I've been honing my skills as a tarot reader for many years now, and I would love to share my knowledge "
            "and expertise with you. Would you be open to having a session with me?",
            "I believe that tarot card readings are a powerful tool for self-discovery and personal growth. I would "
            "be honored to guide you through a session and help you uncover new insights about your life.",
            "I know that some people are skeptical about tarot card readings, but I believe that if you approach it "
            "with an open mind, it can be an incredibly rewarding experience. Would you be willing to give it a try "
            "with me?"
        ],
        'cancel': [
            "Alright, maybe some other time.",
            "That's perfectly okay. My services are only for those who seek them, and I respect your decision not to "
            "have a reading today.",
            "I understand that not everyone believes in the power of tarot. If you ever change your mind, I will be "
            "here to offer my guidance.",
            "I appreciate your honesty. Tarot readings are a personal choice, and I'm always here to help those who "
            "are open to receiving my insights.",
            "No problem at all. Tarot readings can be a bit intimidating, and I understand that not everyone is ready "
            "for that kind of experience.",
            "Of course, I completely respect your decision. If you ever have any questions or concerns, feel free to "
            "reach out to me at any time."
        ],
        'question': [
            "Before we begin, I'd like to invite you to share an concerns that you would like to address "
            "during our session.",
            "In order to make the most of our time together, I'd like to ask you to take a few moments to reflect on "
            "any areas of your life that you would like to explore through the tarot cards.",
            "I find that the most meaningful tarot readings come when we start with a clear intention.",
            "I believe that tarot readings work best when we are able to delve deeply into the areas of your life "
            "that are most important to you.",
            "Tarot readings can be incredibly illuminating, but they work best when we start with a clear sense of "
            "what you would like to know or explore.",
        ],
        'focus': [
            "This will help me to focus my insights and provide you with the most helpful guidance possible.",
            "When you're ready, please let me know what's on your mind.",
            "I would like you to take a moment to think about what you would like to focus on today, and then we can "
            "get started.",
            "Is there anything specific that you would like to focus on today?"
        ]
    },
    'question': {
        'response': [
            "I appreciate you sharing your question with me. Just to let you know, we will be using this question as "
            "the basis for our tarot reading today. I believe that the cards have the ability to provide valuable "
            "insights and guidance on your situation.",
            "Your question is an important one, and we will be using it as the focus of our tarot reading today. The "
            "tarot cards can offer a unique perspective and bring clarity to your situation, helping you to move "
            "forward with confidence.",
            "By sharing your question with me, you have taken the first step in seeking guidance and understanding. I "
            "would like to let you know that we will be using this question as the center of our tarot reading, "
            "and I believe that the cards will be able to offer meaningful insights that can help you find your way.",
            "Thank you for trusting me with your question. Just to let you know, we will be using this question as "
            "the anchor for our tarot reading. The cards have a way of revealing hidden truths and offering a fresh "
            "perspective, and I believe that they will be able to provide you with valuable insights.",
            "Thank you for sharing your question with me. I'd like to let you know that we will be using this "
            "question as the focus of our tarot reading today. The tarot cards can offer insights and guidance that "
            "can help shed light on the situation and provide clarity and direction."
        ],
        'start': [
            "Let us begin.",
            "Let me shuffle my deck",
            "The starts are well aligned, so let us get started.",
            "Let me draw three cards for you."
        ],
        'will i':
            "Try to avoid questions starting with 'Will I...' as they will lock you into a passive role in your own "
            "future. Is there something else you would like to focus on?",
        'example': [
            "What do I need to know about...?",
            "How can I understand...?",
            "Why am I feeling anxious about...?",
            "Where is the hidden opportunity in...?",
            "What should I focus on in my relationship with...?",
            "How can I move past...?"
        ]
    },
    'draw': {
        'show': [
            'I have drawn the following cards for you:',
            'Perfect! I have drawn the following:',
            'Here is your draw!',
            'With all my might I present you the following cards!'
        ],
        'your card': ["Yes I see, your", "let me see, your", "Certainly interesting! Your", "It appears that your"],
        'time': ['past', 'present', 'future'],
        'meaning': ["which means", "that entails", "corresponds to", "which describes"],
        'reflection': [
            "Now that we have your cards in front of us, I'd like to ask you to take a moment to reflect on your "
            "question. Does it still feel relevant and important to you? Is there anything that you would like to add "
            "or clarify?",
            "Before we begin interpreting the cards, I would like to invite you to revisit your question. Take a deep "
            "breath, and ask yourself again: what is it that you really want to know? Are you ready to receive the "
            "guidance that the tarot has to offer?",
            "As we begin to explore your cards, I'd like to encourage you to stay connected to your question. Take a "
            "moment to center yourself, and consider what it is that you're hoping to gain from this reading. How can "
            "the cards help you on your path?",
            "Your question has brought us here today, and I'd like to invite you to take a moment to reconnect with "
            "it before we begin. Is there anything that you would like to ask for guidance on specifically? Are you "
            "open and ready to receive the insights that the tarot has to offer?",
            "The question that you brought to this reading is the foundation upon which our insights will be built. "
            "Take a moment to reflect on it again, and consider what it is that you really want to know. Are you "
            "ready to explore the hidden truths and messages that the cards have to offer?"
        ]
    }
}


class ConvState(IntEnum):
    END = -1
    START = 0
    QUESTION = 1
    DRAW = 2


class Conversation:
    def __init__(self, channel, user, bot):
        self.channel = channel
        self.user = user
        self.bot = bot
        self.state = ConvState.START

    def ended(self):
        return self.state == ConvState.END

    async def respond(self, msg, *, file=None, view=None):
        async with self.channel.typing():
            await sleep(len(msg.split(' ')) / 4)  # Typing speed = 240 wpm
            await self.channel.send(msg, view=view, file=file)

    async def on_message(self, msg):
        if any(word in msg.content.lower() for word in ['who', 'are' 'you']):
            await self.respond(text['description'])
        elif self.state == ConvState.START:
            await self.start_reading(msg)
        elif self.state == ConvState.QUESTION:
            await self.prompt_question(msg)

    async def start_reading(self, msg):
        if any(word in msg.content.lower() for word in ['card', 'cards', 'read', 'reading']):
            await self.respond(f"{random.choice(text['start']['intro'])} {self.user.mention}, "
                               f'I will gladly draw you some tarot cards!')
            await sleep(1)
            await self.respond(f"{random.choice(text['start']['question'])} We can start by asking the deck an "
                               f"_open-ended question_. {random.choice(text['start']['focus'])} "
                               f"(Please **@mention** me in your response)")
            self.state = ConvState.QUESTION
        else:
            confirm = Confirm()
            await self.respond(f"{random.choice(text['start']['intro'])} {self.user.mention}, {random.choice(text['start']['invite'])}",
                               view=confirm)
            await confirm.wait()
            if confirm.confirmed:
                await self.respond(f"{random.choice(text['start']['question'])} We can start by asking the deck an "
                                   f"_open-ended question_. {random.choice(text['start']['focus'])} "
                                   f"(Please **@mention** me in your response)")
                self.state = ConvState.QUESTION
            else:
                await self.respond(random.choice(text['start']['cancel']))
                self.state = ConvState.END

    async def prompt_question(self, msg):
        if msg.content.lower().split(' ')[1] == "will":
            await self.respond(f"{text['question']['will i']} Maybe try a question such as: _{random.choice(text['question']['example'])}_")
        else:
            await self.respond(f"{random.choice(text['question']['response'])} {random.choice(text['question']['start'])}")
            self.state = ConvState.DRAW
            await self.draw3()

    async def draw3(self):
        deck = Deck()
        cards = deck.draw3()
        image = display_three_cards(cards)

        with BytesIO() as buf:
            image.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename="tarot-draw.png")

        await self.respond(random.choice(text['draw']['show']), file=file)
        for index, card in enumerate(cards):
            await self.respond(
                f"{random.choice(text['draw']['your card'])} {text['draw']['time'][index]} card is **{card.readable_name}**, "
                f"{random.choice(text['draw']['meaning'])} _{' & '.join([', '.join(card.desc[:-1]), card.desc[-1]])}_."
            )
        await self.respond(random.choice(text['draw']['reflection']))
        self.state = ConvState.END
