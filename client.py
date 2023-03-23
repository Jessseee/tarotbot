import discord
from discord.ext import commands
from conversation import Conversation


class TarotBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.conversations = []

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, msg):
        if not msg.author.bot and bot.user.mentioned_in(msg) and msg.author not in self.conversations:
            self.conversations.append(msg.author)
            print(self.conversations)
            conv = Conversation(msg)
            await conv.start()
            self.conversations.remove(msg.author)


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
