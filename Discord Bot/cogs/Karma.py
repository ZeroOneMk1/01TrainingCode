import discord, json, asyncio
import random as rd
from discord.ext import commands

class Karma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def add_karma(self, ctx, amount):
        await self.open_account(ctx.author)

        users = await self.get_bank_data()

        karma = users[str(ctx.author.id)]["karma"]

        karma += int(amount)

        users[str(ctx.author.id)]["karma"] = karma

        await ctx.send(f"Your new karma is {karma}")

        with open("01TrainingCode/Discord Bot/main.json", 'w') as f:
            json.dump(users, f)

    async def add_balance(self, ctx, amount):
        await self.open_account(ctx.author)

        users = await self.get_bank_data()
        
        bal = users[str(ctx.author.id)]["balance"]

        bal += int(amount)

        users[str(ctx.author.id)]["balance"] = bal

        await ctx.send(f"Your new balance is {bal}")

        with open("01TrainingCode/Discord Bot/main.json", 'w') as f:
            json.dump(users, f)
    
    async def open_account(self, author):

        users = await self.get_bank_data()

        if str(author.id) in users:
            return
        else:
            users[str(author.id)] = {}
            users[str(author.id)]["karma"] = 0
            users[str(author.id)]["balance"] = 0

        with open("01TrainingCode/Discord Bot/main.json", 'w') as f:
            json.dump(users, f)

    async def open_account_by_id(self, ID):

        users = await self.get_bank_data()

        if str(ID) in users:
            return
        else:
            users[str(ID)] = {}
            users[str(ID)]["karma"] = 0
            users[str(ID)]["balance"] = 0

        with open("01TrainingCode/Discord Bot/main.json", 'w') as f:
            json.dump(users, f)

    async def get_bank_data(self):
        with open("01TrainingCode/Discord Bot/main.json", 'r') as f:
            users = json.load(f)
        return users

    @commands.command(aliases = ['bal', 'balance'])
    async def karma(self, ctx):
        """Returns your current karma."""
        await self.open_account(ctx.author)

        users = await self.get_bank_data()

        karma = users[str(ctx.author.id)]["karma"]
        balance = users[str(ctx.author.id)]["balance"]

        em = discord.Embed(
            title=f"{ctx.author.name}, this is your karma.", color=discord.Colour.magenta())
        em.add_field(name="Karma", value=karma)
        em.add_field(name="Balance", value=balance)

        await ctx.send(embed=em)


    @commands.command()
    async def makeMeRich(self, ctx, karma, bal):
        """Only for daddy, debug."""
        await self.open_account(ctx.author)

        try:
            pog = int(bal)
        except:
            await ctx.send("Fuck off.")
            return

        if(ctx.author.id == 154979334002704384):
            await self.add_karma(ctx, karma)
            await self.add_balance(ctx, bal)
            await ctx.send("Here you go daddy.")

        else:
            await ctx.send("You're not my dad!")


    @commands.command()
    async def beg(self, ctx):
        """Gives a random amount of money."""
        await self.open_account(ctx.author)

        scraps = rd.randint(1, 10)

        await self.add_karma(ctx, scraps)
        await ctx.send("Peasant...")


    @commands.command()
    async def thanks(self, ctx, *, pog=''):
        """Thanks"""
        with open("01TrainingCode/Discord Bot/thankscount.json", 'r') as f:
            thankscount = json.load(f)
        thankscount["thanks"] += 1
        with open("01TrainingCode/Discord Bot/thankscount.json", 'w') as f:
            json.dump(thankscount, f)
        
        await ctx.send("Any time, my student.")
        await self.open_account(ctx.author)
        await self.add_karma(ctx, 50)
    
    @commands.command()
    async def gift(self, ctx, person, amount):
        """Gift a friend with karma!"""
        await self.open_account(ctx.author)
        
        person = person[3:-1]

        try:
            int(person)
        except:
            await ctx.send("Please ping someone in the person input slot.")
            return
        
        try:
            amount = int(amount)
        except:
            await ctx.send("Please enter a valid amount to gift.")
            return

        if amount < 0:
            await ctx.send("HEY! Stealing is BAD! Don't steal!")
            await self.add_balance(ctx, amount)
        else:
            await self.open_account_by_id(person)
            data = await self.get_bank_data()

            if data[str(ctx.author.id)]["balance"] < amount:
                await ctx.send("I'm sorry, but you don't have that much karma to give.")
            else:
                await self.add_balance(ctx, amount * -1)
                data = await self.get_bank_data()
                bal = data[str(person)]["balance"]
                
                bal += int(amount)

                data[str(person)]["balance"] = bal

                await ctx.send(f"Their new balance is {bal}")

                with open("01TrainingCode/Discord Bot/main.json", 'w') as f:
                    json.dump(data, f)
            


def setup(bot):
    bot.add_cog(Karma(bot))