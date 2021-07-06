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

        name = description[0].lower()
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
        
        await self.Karma.add_karma(ctx, 2)


    @commands.command()    
    async def tick(self, ctx, *description):
        """Chages a specific Clock's phase by a specified value"""
        await self.open_channel_by_id(ctx.channel.id)

        name = description[0].lower()

        clocks = await self.get_clocks_data()
        
        size = clocks[str(ctx.channel.id)][name]['size']
        
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
            try:
                await ctx.send(file=discord.File(f"Party Wizard/PClocks/Progress Clock {size}-{size}.png"))
            except:
                pass
            
            clocks[str(ctx.channel.id)].pop(name)
        else:
            clocks[str(ctx.channel.id)][name]["phase"] = newvalue


            if size == 4 or size == 6 or size == 8:

                if newvalue >=0 and newvalue <= size:
                    await ctx.send(file=discord.File(f"Party Wizard/PClocks/Progress Clock {size}-{newvalue}.png"))
                elif newvalue < 0:
                    await ctx.send(file=discord.File(f"Party Wizard/PClocks/Progress Clock {size}-0.png"))
                else:
                    await ctx.send(file=discord.File(f"Party Wizard/PClocks/Progress Clock {size}-{size}.png"))
            elif size > 0:
                sendstring = ''
                for _ in range(newvalue):
                    sendstring += ":black_large_square:"
                for _ in range(size - newvalue):
                    sendstring += ":white_large_square:"
                await ctx.send(sendstring)
            else:
                await ctx.send("I'm sorry, but the clock has a negative size, so I can't show it.")

            await ctx.send(f"The new phase value for this clock is {newvalue}")

        with open("Party Wizard/clocks.json", 'w') as f:
            json.dump(clocks, f)
        
        await self.Karma.add_karma(ctx, 1)

    @commands.command()
    async def clocks(self, ctx):
        """Returns all clocks in the channel in a dictionary format. May be hard to read."""
        await self.open_channel_by_id(ctx.channel.id)

        clocks = await self.get_clocks_data()

        sendstring = ''

        if clocks[str(ctx.channel.id)] == {}:
            await ctx.send("Couldn't find any clocks in this channel.")
        else:
            for clock in clocks[str(ctx.channel.id)]:
                sendstring += f"Clock '{clock}':\n   Size: {clocks[str(ctx.channel.id)][clock]['size']}\n    Phase: {clocks[str(ctx.channel.id)][clock]['phase']}\n"

            await ctx.send(sendstring)
        
        await self.Karma.add_karma(ctx, 1)

    @commands.command()    
    async def kill(self, ctx, name):
        """Deletes the specified clock."""
        await self.open_channel_by_id(ctx.channel.id)

        name = name.lower()

        clocks = await self.get_clocks_data()

        if name not in clocks[str(ctx.channel.id)]:
            await ctx.send("I'm sorry, but this clock doesn't exist. Maybe you mispronounced it?")
            return

        clocks[str(ctx.channel.id)].pop(name)

        await ctx.send(f"Killed the clock: {name}")

        with open("Party Wizard/clocks.json", 'w') as f:
            json.dump(clocks, f)
    
        await self.Karma.add_karma(ctx, 2)


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