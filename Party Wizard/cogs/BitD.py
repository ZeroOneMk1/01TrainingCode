import discord
import json
from discord.ext import commands
from .Karma import Karma

class BitD(commands.Cog):
    """Blades in the Dard Commands!"""
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
    
    @commands.command()
    async def clock(self, ctx, *description):
        """Makes a new clock according to your specifications."""

        name = description[0]
        size = int(description[1])

        try:
            clock = Clock(size, 0)
        except:
            await ctx.send('Please give me the clock in this format: ("Name" x) where Name is the name of the clock, and x is the size.')

        jsclock = clock.__dict__

        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        if name not in clocks[str(ctx.channel.id)]:
            clocks[str(ctx.channel.id)][name] = jsclock
            await ctx.send(f"Created clock named {name} with size {size}")
        else:
            await ctx.send("Clock not created, as a clock in this channel with this name already exists. To check all clocks on this channel, write 'wiz clocks'")

        with open("Party Wizard/clocks.json", 'w') as f:
            json.dump(clocks, f)

    @commands.command()    
    async def tick(self, ctx, *description):
        """Chages a specific Clock's phase by a specified value"""
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        name = description[0]
        
        if name not in clocks[str(ctx.channel.id)]:
            await ctx.send("I'm sorry, but this clock doesn't exist. Maybe you mispronounced it?")
            return

        try:
            operation = description[1]
        except:
            operation = '+1'

        if '+' in operation:
            newvalue = clocks[str(ctx.channel.id)][name]["phase"] + int(operation[1:])
        elif '-' in operation:
            newvalue = clocks[str(ctx.channel.id)][name]["phase"] - int(operation[1:])
        else:
            await ctx.send("I'm sorry, but you seem to not have added or subtracted anything.")

        if newvalue >= clocks[str(ctx.channel.id)][name]["size"]:
            await ctx.send("Ding Ding Ding! This clock has reached its end!")
            clocks[str(ctx.channel.id)].pop(name)
        else:
            clocks[str(ctx.channel.id)][name]["phase"] = newvalue

            await ctx.send(f"The new phase value for this clock is {newvalue}")

        with open("Party Wizard/clocks.json", 'w') as f:
            json.dump(clocks, f)

    @commands.command()
    async def clocks(self, ctx):
        """Returns all clocks in the channel in a dictionary format. May be hard to read."""
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        await ctx.send(clocks[str(ctx.channel.id)])

    @commands.command()    
    async def kill(self, ctx, name):
        """Deletes the specified clock."""
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        if name not in clocks[str(ctx.channel.id)]:
            await ctx.send("I'm sorry, but this clock doesn't exist. Maybe you mispronounced it?")
            return

        clocks[str(ctx.channel.id)].pop(name)

        await ctx.send(f"Killed the clock: {name}")

        with open("Party Wizard/clocks.json", 'w') as f:
            json.dump(clocks, f)

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

        with open("Party Wizard/clocks.json", 'w') as f:
            json.dump(clocks, f)
    

        

class Clock():
    def __init__(self, size, phase):
        self.size = size
        self.phase = phase

def setup(bot):
    bot.add_cog(BitD(bot))