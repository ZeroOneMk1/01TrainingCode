import discord
from discord.ext import commands

class TextBased(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def clapify(self, ctx, *, text):
        """Replaces spaces with :clap:"""
        newtext = text.replace(' ', ':clap:')
        await ctx.channel.purge(limit=1)
        await ctx.send(newtext)
    
    
    @commands.command(aliases=['say'])
    async def repeat(self, ctx, *, message):
        """Repeats a message."""
        if(message == "I'm gay"):
            await ctx.send('I know')
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send(message)
    
    @commands.command(aliases=['curse'])
    async def cursed(self, ctx, lvl=0):
        """Immortalizes the cursedness of thy post above."""
        await ctx.channel.purge(limit=1)
        if(abs(lvl) == 0):
            await ctx.send("This is cursed.")
        elif(abs(lvl) % 10 == 1):
            await ctx.send(f"Woaah there, this is cursed to the {lvl}st level!")
        elif(abs(lvl) % 10 == 2):
            await ctx.send(f"Woaah there, this is cursed to the {lvl}nd level!")
        elif(abs(lvl) % 10 == 3):
            await ctx.send(f"Woaah there, this is cursed to the {lvl}rd level!")
        else:
            await ctx.send(f"Woaah there, this is cursed to the {lvl}th level!")
        if(lvl > 8):
            await ctx.send("I'll need a wish spell to unsee this! Anyone have spare GP?")
    

    @commands.command()
    async def spam(self, ctx, person, amount=1):
        """Spams the message you input."""
        for i in range(int(amount)):
            await ctx.send(person)
    
    @commands.command(aliases=['69', 'funny number'])
    async def nice(self, ctx):
        """nice"""
        await ctx.send('Nice')


    @commands.command(aliaes=['love', 'live', 'laugh', 'lovelivelaugh', 'lickmyass'])
    async def livelaughlove(self, ctx):
        """just no"""
        await ctx.send("Watch out there! We got a white girl in our hands! I'll cast mold earth to make some 'magic' crystals as a distraction while you get her!")

def setup(bot):
    bot.add_cog(TextBased(bot))