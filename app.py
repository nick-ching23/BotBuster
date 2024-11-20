import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from google.auth.aio.transport import aiohttp

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

monitoring = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_guild_join(guild):
    if guild.system_channel:
        await guild.system_channel.send(
            f"Hello, {guild.name}! 🎉 Thanks for inviting me!\n"
            "I'm here to assist you. Mention me with `@Veritas` to interact.\n"
            "In order to use our service, please register and login with the "
            "guild Id as the orgId via Postman. \n Your guild id is: "
            f"{guild.id}"
        )
    else:
        print(f"Joined {guild.name}, but no system channel is available.")

@bot.event
async def on_message(message):
    global monitoring

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        content = message.content.lower()

        if "start monitoring" in content:
            monitoring = True
            await message.channel.send("Monitoring started!")
        elif "stop monitoring" in content:
            monitoring = False
            await message.channel.send("Monitoring stopped!")
        else:
            await message.channel.send("I don't recognize that command. \n"
                                       "I currently support 3 commands: \n"
                                       "- start monitoring:  I will start "
                                       "monitoring every message that's "
                                       "being sent in this channel, "
                                       "and I will add flagged text to my "
                                       "database. I will send a warning if a "
                                       "message has been flagged\n"
                                       "- stop monitoring: I will stop "
                                       "monitoring this channel. \n")
        return

    if monitoring:
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{os.getenv('VERITAS_URL')}/checkTextUser"
                params = {
                    "userId": str(message.author.id),
                    "orgId": message.guild.id
                }
                headers = {"Content-Type": "application/json"}
                payload = message.content

                async with session.post(url, params=params, data=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("flagged"):
                            await message.channel.send(
                                f"⚠️ Message from {message.author} has been "
                                f"flagged:"
                                f" {message.content}"
                            )
                    else:
                        print(f"API error: {response.status}")
                        await message.channel.send("⚠️ There was an issue processing the message.")
            except Exception as e:
                print(f"Error connecting to API: {e}")
                await message.channel.send("⚠️ Unable to connect to the API.")


bot.run(TOKEN)