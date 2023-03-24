<h1 align="center">
<img src="profile.webp" width="200px" alt="Tarot bot profile picture">

<br>
Lorelei 
</h1>
<p align="center">
The mystical Lorelei is a Discord Tarot reading bot.
</p>

## Install
Lorelei is created using the Python Discord API. To get Lorelei up and running you need to create a Python [virtual environment](https://docs.python.org/3/library/venv.html). Activate the virtual environment and install the required modules using the Python package manager `pip`.

```Shell
python -m pip install -r requirements.txt
```

You will also need to create a Discord bot account. Check the [Discord documentation](https://discordpy.readthedocs.io/en/stable/discord.html) for instructions.

To make the bot log in to the bot account, copy the `.env.default` file to `.env` and add the application token found on the bot page of the application dashboard.

```Shell
cp .env.default .env
```

## Usage
To start the bot run the `client.py` file. You should see the bot account come online.
```Shell
python client.py
```

To interact with the bot **@mention** the bot in a channel that the bot account has access to. It will ask you whether you would like to have a tarot reading and ask you some questions. Make sure to **@mention** the bot in your responses.
