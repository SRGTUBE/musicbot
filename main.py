import discord
from discord.ext import commands
import wavelink
import os

# Get the bot token from Railway secrets
TOKEN = os.getenv('BOT_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to Lavalink server
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # Connect to Lavalink
    node = await wavelink.NodePool.create_node(
        bot=bot,
        host='localhost',  # Use your Lavalink server host or IP
        port=2333,  # Lavalink default port
        password='youshallnotpass',  # Default password, replace if needed
        identifier='MAIN',  # Name of the node
        region='us_east'  # Your region, change it if needed
    )
    print(f'Connected to Lavalink node {node.identifier}')

# Command to join the voice channel and play music
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("You need to join a voice channel first!")
        return

    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    # Get a song URL from YouTube
    song = await wavelink.YouTubeTrack.search('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  # Change URL as needed
    await voice_client.play(song[0])
    await ctx.send(f"Now playing: {song[0].title}")

# Command to pause the music
@bot.command()
async def pause(ctx):
    if ctx.voice_client:
        ctx.voice_client.pause()
        await ctx.send("Paused the music.")
    else:
        await ctx.send("I'm not playing anything.")

# Command to resume the music
@bot.command()
async def resume(ctx):
    if ctx.voice_client:
        ctx.voice_client.resume()
        await ctx.send("Resumed the music.")
    else:
        await ctx.send("I'm not playing anything.")

# Command to stop the music and disconnect
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped the music and disconnected.")
    else:
        await ctx.send("I'm not playing anything.")

# Run the bot using the token from Railway secrets
bot.run(TOKEN)
