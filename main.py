import disnake
import asyncio
import os
import random

# Konfigurasi Token dari Environment Variable
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("Token Discord belum dimasukkan di Environment Variables!")

# Daftar Activity/Kegiatan
ACTIVITIES = [
    "Playing Minecraft",
    "Watching YouTube",
    "Listening to Spotify",
    "Streaming on Twitch",
    "Reading a Book"
]

class SelfBotClient(disnake.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.loop_task = None

    async def on_ready(self):
        print(f'Successfully logged in as: {self.user}')
        # Mulai task pengubah status otomatis
        self.loop_task = asyncio.create_task(change_activity_loop())

    async def change_activity_loop(self):
        while True:
            try:
                activity_name = random.choice(ACTIVITIES)
                
                # Ubah status menjadi "Playing" dengan nama activity
                await self.change_presence(activity=disnake.Game(name=activity_name))
                
                print(f"Status changed to: {activity_name}")
                
                # Tunggu 5 menit (300 detik) sebelum ganti lagi
                await asyncio.sleep(300)
                
            except Exception as e:
                print(f"Error changing activity: {e}")
                await asyncio.sleep(60)

# SETUP INTENTS UNTUK DISNAKE
intents = disnake.Intents.default()
intents.message_content = True 
intents.guilds = True
intents.members = True

client = SelfBotClient(intents=intents)

try:
    # Jalankan sebagai User Client (Self-Bot)
    client.run(TOKEN, bot=False)
except disnake.LoginFailure:
    print("Gagal login! Pastikan token yang digunakan adalah User Token.")
except KeyboardInterrupt:
    print("Bot dihentikan oleh pengguna.")
