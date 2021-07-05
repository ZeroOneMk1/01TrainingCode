import discord
import json
from discord.ext import commands
from .Karma import Karma

class BitD(commands.Cog):
    """Blades in the Dard Commands!"""
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)

    async def clock(self, ctx, description):
        """Makes a new clock according to your specifications."""
        parts = description.split('"')
        parts.pop(0)

        name = parts[0]

        try:
            clock = Clock(int(parts[1][1:]), 0)
        except:
            await ctx.send('Please give me the clock in this format: ("Name" x) where Name is the name of the clock, and x is the size.')

        jsclock = json.dumps(clock.__dict__)

        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        if clocks[name] is None:
            clocks[name] = jsclock
        else:
            await ctx.send("Clock not created, as a clock in this channel with this name already exists. To check all clocks on this channel, write 'wiz clocks'")
    
    async def tick(self, ctx, description):
        """Chages a specific Clock's phase by a specified value"""
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        parts = description.split('"')
        parts.pop(0)

        name = parts[0]

        operation = parts[1][1:]

        if '+' in operation:
            newvalue = clocks[str(ctx.channel.id)][name]["phase"] + operation[1:]
        elif '-' in operation:
            newvalue = clocks[str(ctx.channel.id)][name]["phase"] - operation[1:]
        else:
            await ctx.send("I'm sorry, but you seem to not have added or subtracted anything.")

        clocks[str(ctx.channel.id)][name]["phase"] = newvalue

    async def clocks(self, ctx):
        """Returns all clocks in the channel in a dictionary format. May be hard to read."""
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        await ctx.send(clocks[str(ctx.channel.id)])
    
    async def kill(self, ctx, name):
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        clocks[str(ctx.channel.id)].pop(name)

        await ctx.send(f"Killed the clock: {name}")

    async def get_clocks_data(self):
        with open("Party Wizard/clocks.json", 'r') as f:
            clocks = json.load(f)
        return clocks
    
    async def open_channel_by_id(self, ID):

        clocks = await self.get_clocks_data()

        if str(ID) in clocks:
            return
        else:
            clocks[str(ID)] = {}

        with open("Party Wizard/main.json", 'w') as f:
            json.dump(clocks, f)
    

        

class Clock():
    def __init__(self, size, phase):
        self.size = size
        self.phase = phase

def setup(bot):
    bot.add_cog(BitD(bot))