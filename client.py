import discord
from discord.ext import commands
from conversation import Conversation


class TarotBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.conversations = {}

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, msg):
        if not msg.author.bot and not msg.author == self.user and bot.user.mentioned_in(msg):
            if msg.author not in self.conversations.keys():
                conversation = Conversation(msg.channel, msg.author, self)
                self.conversations[msg.author] = conversation
            conversation = self.conversations[msg.author]
            await conversation.on_message(msg)
            if conversation.ended():
                del self.conversations[msg.author]


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    description = """Will pull a number of tarot cards for you."""

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    load_dotenv()
    token = getenv('TOKEN')

    bot = TarotBot(command_prefix=commands.when_mentioned, description=description, intents=intents)
    bot.run(token)
