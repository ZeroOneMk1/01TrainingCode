import nextcord, json, asyncio
import random as rd
from nextcord.ext import commands

class Karma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def add_karma(self, ctx, amount):
        await self.open_account(ctx.user)

        users = await self.get_bank_data()

        karma = users[str(ctx.user.id)]["karma"]

        karma += int(amount)

        users[str(ctx.user.id)]["karma"] = karma

        await ctx.followup.send(f"Your new karma is {karma}", ephemeral=True)

        with open("Party Wizard/main.json", 'w') as f:
            json.dump(users, f)

    async def add_balance(self, ctx, amount):
        await self.open_account(ctx.user)

        users = await self.get_bank_data()
        
        bal = users[str(ctx.user.id)]["balance"]

        bal += int(amount)

        users[str(ctx.user.id)]["balance"] = bal

        await ctx.send(f"Your new balance is {bal}")

        with open("Party Wizard/main.json", 'w') as f:
            json.dump(users, f)
    
    async def open_account(self, user):

        users = await self.get_bank_data()

        if str(user.id) in users:
            return
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["karma"] = 0
            users[str(user.id)]["balance"] = 0

        with open("Party Wizard/main.json", 'w') as f:
            json.dump(users, f)

    async def open_account_by_id(self, ID):

        users = await self.get_bank_data()

        if str(ID) in users:
            return
        else:
            users[str(ID)] = {}
            users[str(ID)]["karma"] = 0
            users[str(ID)]["balance"] = 0

        with open("Party Wizard/main.json", 'w') as f:
            json.dump(users, f)

    async def get_bank_data(self):
        with open("Party Wizard/main.json", 'r') as f:
            users = json.load(f)
        return users

    @nextcord.slash_command(name="balance", description="Returns your karma and your balance.")
    async def karma(self, ctx):
        """Returns your current karma and money."""
        await self.open_account(ctx.user)

        users = await self.get_bank_data()

        karma = users[str(ctx.user.id)]["karma"]
        balance = users[str(ctx.user.id)]["balance"]

        em = nextcord.Embed(
            title=f"{ctx.user.name}, this is your karma.", color=nextcord.Colour.magenta())
        em.add_field(name="Karma", value=karma)
        em.add_field(name="Balance", value=balance)

        await ctx.send(embed=em)


    @nextcord.slash_command(name="make_me_rich", description="Only for owner, debug.", guild_ids=[706471625544957972])
    async def makeMeRich(self, ctx, karma, bal):
        tester = 1
        await self.open_account(ctx.user)

        try:
            pog = int(bal)
        except:
            await ctx.send("Fuck off.")
            return

        if(ctx.user.id == 154979334002704384):
            await self.add_karma(ctx, karma)
            await self.add_balance(ctx, bal)
            await ctx.send("Here you go daddy.")

        else:
            await ctx.send("You're not my dad!")


    @nextcord.slash_command(name="beg", description="Gives a random amount of money for some verbal abuse.")
    async def beg(self, ctx):
        await self.open_account(ctx.user)

        scraps = rd.randint(1, 10)

        await self.add_karma(ctx, scraps)
        await ctx.send("Peasant...")


    @nextcord.slash_command(name="thanks", description="Thanks!")
    async def thanks(self, ctx, pog=''):
        with open("Party Wizard/thankscount.json", 'r') as f:
            thankscount = json.load(f)
        thankscount["thanks"] += 1
        with open("Party Wizard/thankscount.json", 'w') as f:
            json.dump(thankscount, f)
        
        await ctx.send("Any time, my student.")
        await self.open_account(ctx.user)
        await self.add_karma(ctx, 20)
    
    @nextcord.slash_command(name="thanks_count", description="Returns the number of thanks.")
    async def thanksCount(self, ctx):
        with open("Party Wizard/thankscount.json", 'r') as f:
            thankscount = json.load(f)
        await ctx.send(f"I've been thanked {thankscount['thanks']} times!\nThank you for asking :grin:")


    @nextcord.slash_command(name="gift", description="Gift a friend your money!")
    async def gift(self, ctx, person, amount):
        await self.open_account(ctx.user)
        
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

            if data[str(ctx.user.id)]["balance"] < amount:
                await ctx.send("I'm sorry, but you don't have that much karma to give.")
            else:
                await self.add_balance(ctx, amount * -1)
                data = await self.get_bank_data()
                bal = data[str(person)]["balance"]
                
                bal += int(amount)

                data[str(person)]["balance"] = bal

                await ctx.send(f"Their new balance is {bal}")

                with open("Party Wizard/main.json", 'w') as f:
                    json.dump(data, f)
    
    @nextcord.slash_command(name="redeem", description="Redeem your levels using Karma")
    async def redeem(self, ctx):
        await self.open_account(ctx.user)

        users = await self.get_bank_data()

        karma = users[str(ctx.user.id)]["karma"]

        if karma > 10000:

            roles = await ctx.guild.fetch_roles()
            for role in roles:
                if role.name == 'Archwizard':
                    give = role
                    await ctx.user.add_roles(give)
                    await ctx.send("Congrats, you're now an Archwizard!")
                    break
            else:
                give = await ctx.guild.create_role(name='Archwizard', colour=nextcord.Colour.gold(), hoist=True)
                await ctx.user.add_roles(give)
                await ctx.send("Congrats, you're now an Archwizard!")

        elif karma > 1000:
            roles = await ctx.guild.fetch_roles()

            for role in roles:
                if role.name == 'Wizard':
                    give = role
                    await ctx.user.add_roles(give)
                    await ctx.send("Congrats, you're now a Wizard!")
                    break
            else:
                # ? Dooesn't work atm...
                # pos = 2
                # for role in roles:
                #     if role.name == "Apprentice":
                #         pos = role.position + 1
                give = await ctx.guild.create_role(name='Wizard', colour=nextcord.Colour.red(), hoist=True)
                # await give.edit(position=pos)
                await ctx.user.add_roles(give)
                await ctx.send("Congrats, you're now a Wizard!")

        elif karma > 100:

            roles = await ctx.guild.fetch_roles()
            for role in roles:
                if role.name == 'Apprentice':
                    give = role
                    try:
                        await ctx.user.add_roles(give)
                        await ctx.send("Congrats, you're now an Apprentice!")
                    except Exception as e:
                        print(e)
                    break
            else:
                give = await ctx.guild.create_role(name='Apprentice', colour=nextcord.Colour.green(), hoist=True)
                await ctx.user.add_roles(give)
                await ctx.send("Congrats, you're now an Apprentice!")
            
        else:
            await ctx.send("Sorry, but you don't have enough experience for a role.")



def setup(bot):
    bot.add_cog(Karma(bot))