import os
import discord
from discord.ext import commands
import wavelink

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await wavelink.NodePool.create_node(
        bot=bot,
        host=os.getenv("LAVALINK_HOST"),
        port=int(os.getenv("LAVALINK_PORT")),
        password=os.getenv("LAVALINK_PASS"),
        https=os.getenv("LAVALINK_SSL", "false").lower() == "true"
    )

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        return await ctx.send("You're not in a voice channel.")
    channel = ctx.author.voice.channel
    await channel.connect(cls=wavelink.Player)

@bot.command()
async def play(ctx, *, search: str):
    vc = ctx.voice_client

    if not vc:
        if not ctx.author.voice:
            return await ctx.send("You're not in a voice channel.")
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)

    query = f'ytsearch:{search}'
    tracks = await wavelink.YouTubeTrack.search(query)
    if not tracks:
        return await ctx.send("No results found.")
    
    track = tracks[0]
    await vc.play(track)
    await ctx.send(f'Now playing: `{track.title}`')

@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    if not vc or not vc.is_playing():
        return await ctx.send("Nothing is playing.")
    await vc.pause()
    await ctx.send("Paused!")

@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if not vc or not vc.is_paused():
        return await ctx.send("Nothing is paused.")
    await vc.resume()
    await ctx.send("Resumed!")

@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if not vc or not vc.is_connected():
        return await ctx.send("I'm not connected.")
    await vc.disconnect()
    await ctx.send("Disconnected!")

bot.run(os.getenv("BOT_TOKEN"))
