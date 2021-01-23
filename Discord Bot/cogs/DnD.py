import discord
import random as rd
from discord.ext import commands
from .consts import classes

class DnD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['randClass', 'class', 'gimme class'])
    async def randomClass(self, ctx):
        """Returns one random class."""
        rd.shuffle(classes)
        await ctx.send("Your random class is " + classes[0])


    @commands.command(aliases=['randRace', 'race', 'gimmeRace'])
    async def randomRace(self, ctx):
        """Returns one random race."""
        racesfile = open("01TrainingCode/Discord Bot/races.txt", "r")
        races = racesfile.readlines()
        rd.shuffle(races)
        await ctx.send(f"Your random race is:\n```{races[0]}```Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
        racesfile.close()


    @commands.command(aliases=['randFeat', 'feat', 'gimmeFeat'])
    async def randomFeat(self, ctx):
        """Returns one random feat."""
        featsfile = open("01TrainingCode/Discord Bot/feats.txt", "r")
        feats = featsfile.readlines()
        rd.shuffle(feats)
        await ctx.send(f"Your random feat is:\n```{feats[0]}```Visit http://www.jsigvard.com/dnd/Feats.html for more information on this feat.")
        featsfile.close()


    @commands.command(aliases=['character', 'gimmeCharacter', 'randCharacter', 'char', 'randChar'])
    async def randomCharacter(self, ctx):
        """Generates a random Character with race, class and stats."""
        racesfile = open("01TrainingCode/Discord Bot/races.txt",
                        "r", encoding='utf-8')
        races = racesfile.readlines()
        rd.shuffle(races)
        rd.shuffle(classes)
        await ctx.send(f"Your random Character is of the race:\n```{races[0]}```They are a {classes[0]}, and their stats (without race modifiers) look as such:")
        await rollStats.__call__(self, ctx)
        await ctx.send("Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
        racesfile.close()
    
    @commands.command(aliases=['d', 'dice'])
    async def roll(self, ctx, die=20, amount=1):
        """Rolls some dice."""
        total = 0
        rolls = []
        await ctx.send(":arrow_down: Contacting fate:")
        for i in range(int(amount)):
            curr = rd.randint(1, int(die))
            rolls.append(curr)
            total += curr
        await ctx.send(rolls)
        await ctx.send(f'The total is {total}.')


    @commands.command()
    async def check(self, ctx, die=20, mod=0, operator='plus'):
        """Rolls one dice with a modifier on it."""
        if(operator == 'plus'):
            await ctx.send(rd.randint(1, int(die)) + int(mod))
        elif(operator == 'minus'):
            await ctx.send(rd.randint(1, int(die)) - int(mod))
        else:
            await ctx.send("I don't understand, please try again.")


    @commands.command(aliases=['adv'])
    async def advantage(self, ctx, die=20):
        """Rolls with advantage"""
        await ctx.send(":arrow_down: Contacting fate, with advantage:")
        curr1 = rd.randint(1, int(die))
        curr2 = rd.randint(1, int(die))
        await ctx.send(str(curr1) + ', ' + str(curr2))
        if(curr1 < curr2):
            await ctx.send('Final: ' + str(curr2))
        else:
            await ctx.send('Final: ' + str(curr1))


    @commands.command(aliases=['disadv'])
    async def disadvantage(self, ctx, die=20):
        """Rolls with disadvantage."""
        await ctx.send(":arrow_down: Contacting fate, with disadvantage:")
        curr1 = rd.randint(1, int(die))
        curr2 = rd.randint(1, int(die))
        await ctx.send(str(curr1) + ', ' + str(curr2))
        if(curr1 > curr2):
            await ctx.send('Final: ' + str(curr2))
        else:
            await ctx.send('Final: ' + str(curr1))


    @commands.command(aliases=['stats', 'rollstats', 'randomstats', 'randstats'])
    async def rollStats(self, ctx):
        """Rolls an array of 6 4d6 drop lowest stats."""
        await ctx.send(":arrow_down: Contacting fate:")
        rolls = []
        stats = []
        for i in range(6):
            for j in range(4):
                rolls.append(rd.randint(1, 6))
            rolls.sort()
            rolls.pop(0)
            stats.append(rolls[0] + rolls[1] + rolls[2])
            rolls.clear()
        stats.sort()
        await ctx.send(f'Your stats, in ascending order, are: {stats}')


    @commands.command()
    async def rollHP(self, ctx, lvl, dice, conmod):
        """Rolls the maximum HP for your character."""
        sum = int(dice) + int(conmod)
        for i in range(int(lvl) - 1):
            sum += rd.randint(1, int(dice)) + int(conmod)
        await ctx.send("Your maximum HP is: " + str(sum))

    @commands.command()
    async def map(self, ctx):
        """Returns the current map for the campaign."""
        await ctx.channel.send(file=discord.File('01TrainingCode\Discord Bot\map.png'))

def setup(bot):
    bot.add_cog(DnD(bot))