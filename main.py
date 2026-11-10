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
    "Streaming on Twitch"
]

class SelfBotClient(discord.Client):
    def __init__(self, intents):
        # Kita override user_agent agar tidak terdeteksi sebagai bot standar
        super().__init__(intents=intents)
        self.loop_task = None

    async def on_ready(self):
        print(f'Logged in as: {self.user} ({self.user.id})')
        print(f'Type: {"User" if not self.user.bot else "Bot"}')
        
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

# SETUP INTENTS MINIMAL UNTUK SELF-BOT
# Hanya ambil yang paling dasar agar tidak kena rate limit atau error autentikasi
intents = discord.Intents.default()
# Jangan set intents besar seperti members atau guilds jika tidak perlu, 
# karena self-bot biasanya hanya butuh akses ke diri sendiri.
# Namun, kita biarkan default agar kompatibel dengan kebanyakan kasus.
intents.message_content = True 

client = SelfBotClient(intents=intents)

try:
    # Jalankan token
    client.run(TOKEN)
except discord.LoginFailure:
    print("Gagal login! Coba refresh token atau cek apakah akunmu dibatasi.")
except KeyboardInterrupt:
    print("Bot dihentikan oleh pengguna.")
