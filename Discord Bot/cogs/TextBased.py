import discord
from discord.ext import commands
from .Karma import Karma

class TextBased(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
    
    @commands.command()
    async def clapify(self, ctx, *, text):
        """Replaces spaces with :clap:"""
        newtext = text.replace(' ', ':clap:')
        await ctx.channel.purge(limit=1)
        await ctx.send(newtext)
        await self.Karma.add_karma(ctx, 1)
    
    
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
        # await ctx.channel.purge(limit=1)
        if(abs(lvl) == 0):
            await ctx.send("Wait! Let me cast guidance, cause y'all need Jesus.")
        elif(abs(lvl) == 1):
            await ctx.send(f"Woaah there, I need to drop concentration on Comprehend Languages.")
        elif(abs(lvl) == 2):
            await ctx.send(f"I'm getting a restraining order, I need you out of Misty Step range!")
        elif(abs(lvl) == 3):
            await ctx.send(f"KILL IT WITH FIREBALL! QUICKEN THE SPELL YOU USELESS SORCERER I NEED IT ***NOW***.")
        elif(abs(lvl) == 4):
            await ctx.send(f"Yeah, this definitely deserves Banishment.")
        elif(abs(lvl) == 5):
            await ctx.send(f"Oh lord, I'm unseeing this. MODIFY MEMORY *wooshes wand*")
        elif(abs(lvl) == 6):
            await ctx.send(f"Did someone cast Eyebite? I feel sickened!")
        elif(abs(lvl) == 7):
            await ctx.send(f"That's it. I'm summoning Jesus. CONJURE CELESTIAL *wooshes wand*")
        elif(abs(lvl) == 8):
            await ctx.send(f"I'm casting Mind Blank, I need immunity to the psychic damage you just caused with... that...")
        if(lvl > 8):
            await ctx.send("Good Lord, I'll need a wish spell to unsee this! Anyone have spare GP?")
        await self.Karma.add_karma(ctx, 1)
    

    @commands.command()
    async def spam(self, ctx, person, amount=1):
        """Spams the message you input. Currently Disabled."""
        await ctx.send("Hugo made me diable this. Bad Hugo.")
        # for i in range(int(amount)):
        #     await ctx.send(person)
    
    @commands.command(aliases=['69', 'funny number'])
    async def nice(self, ctx):
        """nice"""
        await ctx.send('Nice')
        await self.Karma.add_karma(ctx, 1)



    @commands.command(aliaes=['love', 'live', 'laugh', 'lovelivelaugh', 'lickmyass'])
    async def livelaughlove(self, ctx):
        """just no"""
        await ctx.send("Watch out there! We got a white girl in our hands! I'll cast mold earth to make some 'magic' crystals as a distraction while you get her!")
        await self.Karma.add_karma(ctx, 1)


    @commands.command()
    async def uwufy(self, ctx, *, text):
        """UwU nyaa~~ rawr XD"""
        await ctx.channel.purge(limit=1)
        text = text.replace("r", "w")
        text = text.replace("l", "w")
        text = text.replace('ove', 'uv')
        await ctx.send(text)
        await self.Karma.add_karma(ctx, 1)



def setup(bot):
    bot.add_cog(TextBased(bot))