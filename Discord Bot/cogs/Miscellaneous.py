import discord
import random as rd
from discord.ext import commands
from .Karma import Karma

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.karma = Karma(bot)
    
    @commands.command()
    async def guess(self, ctx, theguess):
        """Guess a random number between 1 and 10."""
        temp = rd.randint(1, 10)
        try:
            int(theguess)
        except:
            await ctx.send('The stars didn\'t align, or you were just stupid. Try again, but with a number this time :angry:.')
            return

        if(int(theguess) == temp):
            await ctx.send('Correct! Are you a divination wizard by chance?')
            await self.karma.add_karma(ctx, 200)
        else:
            await ctx.send(f'Gotta work on those divination spells, huh?\nThe true value was {temp}.')

def setup(bot):
    bot.add_cog(Miscellaneous(bot))