import discord
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

class FlexibleBot(discord.Client):
    def __init__(self, intents):
        # Kita inisialisasi Client biasa, bukan AutoShardedClient agar lebih ringan
        super().__init__(intents=intents)
        self.loop_task = None

    async def on_ready(self):
        print(f'Logged in as: {self.user} (ID: {self.user.id})')
        print(f'Type: {"User" if self.user.bot == False else "Bot"}')
        
        # Mulai task pengubah status otomatis
        self.loop_task = asyncio.create_task(change_activity_loop())

    async def change_activity_loop(self):
        while True:
            try:
                activity_name = random.choice(ACTIVITIES)
                
                # Ubah status menjadi "Playing" dengan nama activity
                await self.change_presence(activity=discord.Game(name=activity_name))
                
                print(f"Status changed to: {activity_name}")
                
                # Tunggu 5 menit (300 detik) sebelum ganti lagi
                await asyncio.sleep(300)
                
            except Exception as e:
                print(f"Error changing activity: {e}")
                await asyncio.sleep(60)

# SETUP INTENTS YANG AMAN UNTUK SEMUA JENIS TOKEN
# Ini adalah kunci agar tidak error 'AttributeError' dan kompatibel dengan Self-Bot & Bot Biasa
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True
intents.members = True
# Penting: Jangan set intents lain yang tidak perlu agar tidak kena rate limit atau error

client = FlexibleBot(intents=intents)

try:
    # Jalankan token. Tidak ada parameter bot=False atau bot=True yang dipaksa.
    # discord.py akan mendeteksi sendiri berdasarkan token.
    client.run(TOKEN)
except discord.LoginFailure:
    print("Gagal login! Pastikan token masih aktif.")
except KeyboardInterrupt:
    print("Bot dihentikan oleh pengguna.")
