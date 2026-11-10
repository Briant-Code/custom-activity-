import discord
import asyncio
import os
import random

# Konfigurasi Token
# Kita ambil dari Environment Variable 'TOKEN' yang akan kita set di Railway
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("Token Discord belum dimasukkan di Environment Variables!")

# Daftar Activity/Kegiatan
# Kamu bisa ganti teks di dalam tanda kutip sesuai keinginan
ACTIVITIES = [
    "Playing Minecraft",
    "Watching YouTube",
    "Listening to Spotify",
    "Streaming on Twitch",
    "Reading a Book"
]

class SelfBotClient(discord.Client):
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
                # Pilih aktivitas acak
                activity_name = random.choice(ACTIVITIES)
                
                # Ubah status menjadi "Playing" dengan nama activity
                await self.change_presence(activity=discord.Game(name=activity_name))
                
                print(f"Status changed to: {activity_name}")
                
                # Tunggu 5 menit (300 detik) sebelum ganti lagi
                # Jika ingin lebih lama, ubah angka 300 menjadi lebih besar (misal 600 untuk 10 menit)
                await asyncio.sleep(300)
                
            except Exception as e:
                print(f"Error changing activity: {e}")
                # Jika error (misal internet putus), tunggu sebentar lalu coba lagi
                await asyncio.sleep(60)

# Setup Intents
intents = discord.Intents.default()
# Untuk self-bot, kita biasanya hanya butuh default intents
client = SelfBotClient(intents=intents)

try:
    # Jalankan bot dengan user token (bot=False penting untuk self-bot)
    client.run(TOKEN, bot=False)
except discord.LoginFailure:
    print("Gagal login! Pastikan token yang digunakan adalah User Token (Self-Bot Token), bukan Bot Token.")
except KeyboardInterrupt:
    print("Bot dihentikan oleh pengguna.")
