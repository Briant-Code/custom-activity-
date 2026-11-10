import discord
import asyncio
import os
import random

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("Token Discord belum dimasukkan!")

ACTIVITIES = [
    "Playing Minecraft",
    "Watching YouTube",
    "Listening to Spotify",
    "Streaming on Twitch"
]

class MyBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.loop_task = None

    async def on_ready(self):
        print(f'Logged in as: {self.user}')
        self.loop_task = asyncio.create_task(change_activity_loop())

    async def change_activity_loop(self):
        while True:
            try:
                activity_name = random.choice(ACTIVITIES)
                await self.change_presence(activity=discord.Game(name=activity_name))
                print(f"Status changed to: {activity_name}")
                await asyncio.sleep(300)
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(60)

# Intent minimal agar ringan dan kompatibel
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True
intents.members = True

client = MyBot(intents=intents)

try:
    client.run(TOKEN)
except discord.LoginFailure:
    print("Gagal login! Pastikan token valid.")
except KeyboardInterrupt:
    print("Stopped.")
