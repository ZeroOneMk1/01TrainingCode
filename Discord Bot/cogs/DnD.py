import discord
import random as rd
from discord.ext import commands
from .consts import classes
from .Karma import Karma
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = False

class DnD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
    
    @commands.command(aliases=['randClass', 'class', 'gimme class'])
    async def randomClass(self, ctx):
        """Returns one random class."""
        rd.shuffle(classes)
        await ctx.send("Your random class is " + classes[0])
        await self.Karma.add_karma(ctx, 1)


    @commands.command(aliases=['randRace', 'race', 'gimmeRace'])
    async def randomRace(self, ctx):
        """Returns one random race."""
        racesfile = open("Discord Bot/races.txt", "r")
        races = racesfile.readlines()
        rd.shuffle(races)
        await ctx.send(f"Your random race is:\n```{races[0]}```Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
        racesfile.close()
        await self.Karma.add_karma(ctx, 1)


    @commands.command(aliases=['randFeat', 'feat', 'gimmeFeat'])
    async def randomFeat(self, ctx):
        """Returns one random feat."""
        featsfile = open("Discord Bot/feats.txt", "r")
        feats = featsfile.readlines()
        rd.shuffle(feats)
        await ctx.send(f"Your random feat is:\n```{feats[0]}```Visit http://www.jsigvard.com/dnd/Feats.html for more information on this feat.")
        featsfile.close()
        await self.Karma.add_karma(ctx, 1)

    
    @commands.command(aliases=['d', 'dice', 'r'])
    async def roll(self, ctx, rollstr):
        """Rolls some dice."""

        try:
            rollarr = rollstr.split("d")
            amount = int(rollarr[0])
            if "+" in rollarr[1]:
                die = int(rollarr[1].split("+")[0])
                mod = int(rollarr[1].split("+")[1])
                op = 1
            elif "-" in rollarr[1]:
                die = int(rollarr[1].split("-")[0])
                mod = int(rollarr[1].split("-")[1])
                op = -1
            else:
                die = int(rollarr[1])
                op = 0
        except:
            await ctx.send("I don't understand that, please use common dice notation.")
            return

        if amount > 500:
            await ctx.send("Woah there, that's a lotta dice. This would result in an explosion, so I'd rather not.")
            return
        else:
            total = 0
            rolls = []
            await ctx.send(":arrow_down: Contacting fate:")
            for i in range(int(amount)):
                curr = rd.randint(1, die)
                rolls.append(curr)
                total += curr
            if op == 1:
                total += mod
            elif op == -1:
                total -= mod

            await ctx.send(rolls)
            await ctx.send(f'The total is {total}.')
            await self.Karma.add_karma(ctx, 1)

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
        await self.Karma.add_karma(ctx, 1)


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
        await self.Karma.add_karma(ctx, 1)


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
        summ = 0
        for stat in stats:
            summ += stat

        await ctx.send(f'Your stats, in ascending order, are: {stats}, and the sum is: {summ}')


    @commands.command()
    async def rollHP(self, ctx, lvl, dice, conmod):
        """Rolls the maximum HP for your character."""
        sum = int(dice) + int(conmod)
        for i in range(int(lvl) - 1):
            sum += rd.randint(1, int(dice)) + int(conmod)
        await ctx.send("Your maximum HP is: " + str(sum))
        await self.Karma.add_karma(ctx, 1)

    @commands.command(aliases=['character', 'gimmeCharacter', 'randCharacter', 'char', 'randChar'])
    async def randomCharacter(self, ctx):
        """Generates a random Character with race, class and stats."""
        racesfile = open("Discord Bot/races.txt",
                        "r", encoding='utf-8')
        races = racesfile.readlines()
        rd.shuffle(races)
        rd.shuffle(classes)
        await ctx.send(f"Your random Character is of the race:\n```{races[0]}```They are a {classes[0]}, and their stats (without race modifiers) look as such:")
        await self.rollStats.__call__(ctx)
        await ctx.send("Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
        racesfile.close()
        await self.Karma.add_karma(ctx, 5)

    @commands.command()
    async def map(self, ctx):
        """Returns the current map for the campaign."""
        await ctx.channel.send(file=discord.File('Discord Bot/map1.png'))
        await self.Karma.add_karma(ctx, 1)

    @commands.command()
    async def wikidot(self, ctx, *, string):
        """DOESNT WORK AT THE MOMENT - Searches wikidot and returns the top result. Only works well for spells."""
        searchstring = "http://dnd5e.wikidot.com/search:site/q/" + string.replace(' ', '%20')
        try:
            browser = Chrome(options=opts)
        except Exception as e:
            await ctx.send(e)
            return
        browser.get(searchstring)
        browser.implicitly_wait(5)

        try:
            browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div/div/div/div[3]/div/div[1]/div/div[3]/div[1]/div[1]/a').click()
        except:
            browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/a').click()
        
        url = browser.current_url

        thingy = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div/div/div/div[1]/span')
        
        em = discord.Embed(title=thingy.text, color=discord.Colour.magenta())

        try:
            if "spell" in url:
                text = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div/div/div/div[3]/p[4]').text
                title = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div/div/div/div[3]/p[2]').text
                em.add_field(name=title, value=text)
            else:
                text = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div/div/div/div[3]/p/strong/em').text

                em.add_field(name="Description:", value=text)
        except:
            em.add_field(name="Couldn't find a short enough description.")

        await ctx.send(f"This is the top result: \n{url}", embed=em)

        await ctx.send(f"If this isn't what you wanted, try this link: \n{searchstring}")
        browser.quit()
        await self.Karma.add_karma(ctx, 5)


def setup(bot):
    bot.add_cog(DnD(bot))