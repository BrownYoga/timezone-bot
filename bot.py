import discord
from discord.ext import tasks
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # ✅ Gets token from Railway secrets
GUILD_ID = 1328810752877793401  # Replace with your actual Server ID
CHANNEL_ID = 1333862823935217685  # Replace with your Voice Channel ID

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(minutes=30)  # ✅ Updates every 30 minute
async def update_time():
    try:
        guild = client.get_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            # ✅ Format time with dashes (20-08 instead of 20:08)
            cet_time = datetime.now(pytz.timezone('CET')).strftime('%H-%M CET (UTC+1)')
            await channel.edit(name=f"🕒 {cet_time}")
            print(f"Updated channel name to {cet_time}")
    except discord.errors.HTTPException as e:
        if e.status == 429:  # Handle rate limiting
            retry_after = int(e.response.headers.get("Retry-After", 1800))  # Default to 30 mins
            print(f"Rate limited! Retrying in {retry_after} seconds...")
            await asyncio.sleep(retry_after)
            await update_time()  # Retry

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    update_time.start()

client.run(TOKEN)
