import nextcord
import random as rd
from nextcord.ext import commands
from .consts import classes
from .Karma import Karma
from time import sleep
import urllib.request
import re
import json
from nextcord.ui import Button, View


class DnD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)

    @nextcord.slash_command(name="random_class", description="Returns one random class.")
    async def randomClass(self, ctx):
        rd.shuffle(classes)
        await ctx.send("Your random class is " + classes[0])
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="random_race", description="Returns one random race.")
    async def randomRace(self, ctx):
        racesfile = open("Party Wizard/races.txt", "r")
        races = racesfile.readlines()
        rd.shuffle(races)
        await ctx.send(f"Your random race is:\n```{races[0]}```Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
        racesfile.close()
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="random_feat", description="Returns one random feat.")
    async def randomFeat(self, ctx):
        featsfile = open("Party Wizard/feats.txt", "r")
        feats = featsfile.readlines()
        rd.shuffle(feats)
        await ctx.send(f"Your random feat is:\n```{feats[0]}```Visit http://www.jsigvard.com/dnd/Feats.html for more information on this feat.")
        featsfile.close()
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="roll", description="Rolls some dice.")
    async def roll(self, ctx, rollstr):

        rollsarr = rollstr.split("+")

        await ctx.send(f":arrow_down: Contacting fate on {rollstr}:")

        total = 0
        rolls = []

        for roll in rollsarr:

            try:
                rollarr = roll.split("d")
                for _ in range(int(rollarr[0])):

                    try:
                        temp = rollarr[1].split("-")
                        rollarr[1] = temp[0]
                        rollarr.append(temp[1])
                    except:
                        rollarr.append(0)

                    curr = rd.randint(1, int(rollarr[1]))
                    rolls.append(curr)
                    total += curr

                total -= int(rollarr[2])

            except:

                try:

                    total += int(roll)

                except:

                    await ctx.send("I don't understand that, please use common dice notation.")
                    return

        await self.print_long(ctx, str(rolls))
        await ctx.send(f'The total is {total}.')
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="advantage", description="Rolls with advantage")
    async def advantage(self, ctx, die=20):
        await ctx.send(":arrow_down: Contacting fate, with advantage:")
        curr1 = rd.randint(1, int(die))
        curr2 = rd.randint(1, int(die))
        await ctx.send(str(curr1) + ', ' + str(curr2))
        if(curr1 < curr2):
            await ctx.send('Final: ' + str(curr2))
        else:
            await ctx.send('Final: ' + str(curr1))
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="disadvantage", description="Rolls with disadvantage.")
    async def disadvantage(self, ctx, die=20):
        await ctx.send(":arrow_down: Contacting fate, with disadvantage:")
        curr1 = rd.randint(1, int(die))
        curr2 = rd.randint(1, int(die))
        await ctx.send(str(curr1) + ', ' + str(curr2))
        if(curr1 > curr2):
            await ctx.send('Final: ' + str(curr2))
        else:
            await ctx.send('Final: ' + str(curr1))
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="stats", description="Rolls an array of 6 4d6 drop lowest stats.")
    async def rollStats(self, ctx):
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

    @nextcord.slash_command(name="roll_hp", description="Rolls the RAW maximum HP for your character.")
    async def rollHP(self, ctx, lvl, dice, conmod):
        sum = int(dice) + int(conmod)
        for i in range(int(lvl) - 1):
            sum += rd.randint(1, int(dice)) + int(conmod)
        await ctx.send("Your maximum HP is: " + str(sum))
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="random_character", description="Generates a random Character with race, class and stats.")
    async def randomCharacter(self, ctx):
        racesfile = open("Party Wizard/races.txt",
                         "r", encoding='utf-8')
        races = racesfile.readlines()
        rd.shuffle(races)
        rd.shuffle(classes)
        await ctx.send(f"Your random Character is of the race:\n```{races[0]}```They are a {classes[0]}, and their stats (without race modifiers) look as such:")
        await self.rollStats.__call__(ctx)
        await ctx.send("Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
        racesfile.close()
        await self.Karma.add_karma(ctx, 5)

    @nextcord.slash_command(name="map", description="Returns the current map for the campaign.")
    async def map(self, ctx):
        await ctx.channel.send(file=nextcord.File('Party Wizard/map1.png'))
        await self.Karma.add_karma(ctx, 1)

    @nextcord.slash_command(name="boo", description="Adds one tick to this person in the loserboard.")
    async def loserboard(self, ctx, loser="Check"):

        await self.add_loserboard(ctx)

        with open("Party Wizard/cogs/loserboards.json", 'r') as f:
            loserboards = await self.get_loserboard_data()
            f.close()

        if loser != "Check":

            loser_id = loser[3:-1]

            try:
                int(loser_id)
            except:
                await ctx.send("Please ping the person you want to add to the loserboard, or write nothing if you just want to read it.")

            try:

                losercount = loserboards[str(ctx.guild.id)][loser_id]

            except:

                loserboards[str(ctx.guild.id)][loser_id] = 0
                losercount = 0

            losercount += 1

            loserboards[str(ctx.guild.id)][loser_id] = losercount

            with open("Party Wizard/cogs/loserboards.json", 'w') as f:

                json.dump(loserboards, f)

            await self.print_losers(ctx)

        else:

            await self.print_losers(ctx)

    async def print_losers(self, ctx):

        with open("Party Wizard/cogs/loserboards.json", 'r') as f:
            loserboards = await self.get_loserboard_data()
            f.close()

        sendstr = "LOSERBOARD:\n```"

        sorted_loserboard = sorted(loserboards[str(ctx.guild.id)].items(), key=lambda x: x[1], reverse=True)

        for person in sorted_loserboard:

            sendstr += f"{ctx.guild.get_member(int(person[0])).display_name} - {person[1]}\n"

        sendstr += "```"

        await ctx.send(sendstr)

    async def add_loserboard(self, ctx):
        loserboards = await self.get_loserboard_data()

        if str(ctx.guild.id) in loserboards:
            return
        else:
            loserboards[str(ctx.guild.id)] = {}

        with open("Party Wizard/cogs/loserboards.json", 'w') as f:
            json.dump(loserboards, f)

    async def get_loserboard_data(self):
        with open("Party Wizard/cogs/loserboards.json", 'r') as f:
            loserboards = json.load(f)
        return loserboards

    @nextcord.slash_command(name="wikidot", description="Searches wikidot and returns the top result. VERY UNRELIABLE.")
    async def wikidot(self, ctx, string):
        await ctx.send("Searching Wikidot. This may take a while.")

        url = "http://dnd5e.wikidot.com/search:site/q/" + \
            string.replace(' ', '%20')
        with urllib.request.urlopen(url) as response:
            html = response.read()

        urllist = re.findall(r"""<\s*a\s*href=["'](http:\/\/dnd5e\.wikidot\.com\/[^=]+)["']""",
                             urllib.request.urlopen(url).read().decode("utf-8"))

        try:
            result = urllist[0]
        except:
            if "timed out" in urllib.request.urlopen(url).read().decode("utf-8"):

                await ctx.send("I'm sorry, but the website timed out.")

                button = Button(label="go to Wikidot", url=url)
                view = View()
                view.add_item(button)

                await ctx.send("There's a chance this link works better than it did for me:", view=view)

            else:
                print("No URLs found")

        print(result)

        site = urllib.request.urlopen(result).read().decode("utf-8")

        paragraphs = "<p>" + \
            re.findall(r"""<p>([^=]+)<\/p>""", site)[0] + "</p>"

        infos = re.findall(r"<[^>]+>([^\\<]+)", paragraphs)

        chunknum = 0
        printstr = []
        printstr.append('')

        for thing in infos:
            tempprintstr = printstr[chunknum] + thing
            if len(tempprintstr) > 1000:
                await ctx.send("Result too long. Made a new ~1000 character chunk")
                chunknum += 1
                printstr.append(thing)
                tempprintstr = ''
            else:
                printstr[chunknum] += thing

        resultname = re.findall(r":([^/]+)", result)[0]

        await ctx.send(f"This is the top result: \n{resultname}")

        em = nextcord.Embed(
            title=f"Result: {resultname}", color=nextcord.Colour.magenta())

        em.add_field(name="Description:", value=printstr)

        await ctx.send(embed=em)

        try:
            for i in range(len(printstr) - 1):

                em = nextcord.Embed(color=nextcord.Colour.magenta())

                em.add_field(name="...", value=printstr[i + 1])

                await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(e)
        
        button = Button(label="go to Wikidot", url=url)
        view = View(button)

        await ctx.send(f"If this isn't what you wanted, try this link:", view=view)

        await self.Karma.add_karma(ctx, 5)

    async def print_long(self, ctx, to_be_printed: str):

        chunknum = 0
        printstr = []
        printstr.append('')

        for char in to_be_printed:
            tempprintstr = printstr[chunknum] + char
            if len(tempprintstr) > 1000:
                await ctx.send("Result too long. Made a new ~1000 character chunk")
                chunknum += 1
                printstr.append(char)
                tempprintstr = ''
            else:
                printstr[chunknum] += char
        
        try:
            for i in range(len(printstr)):

                em = nextcord.Embed(color=nextcord.Colour.magenta())

                em.add_field(name="Rolls", value=printstr[i])

                await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(DnD(bot))
