import nextcord, time, json
from nextcord.ext import commands
from .Karma import Karma
from .Scheduling import Scheduling

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
        self.Scheduling = Scheduling(bot)

    def is_person(self, m):
        with open("Party Wizard/person.json", 'r') as f:
                person = json.load(f)
        return m.user.id == person["person"]

    @nextcord.slash_command(name="clean", description="Deletes messages.")
    async def clear(self, ctx, amount=1, person = "None"):
        if ctx.user.id == 154979334002704384 or ctx.user.guild_permissions.manage_messages == True:
            if person != "None":
                
                person = person[3:-1]

                with open("Party Wizard/person.json", 'r') as f:
                    deleted = json.load(f)
                deleted["person"] = int(person)
                with open("Party Wizard/person.json", 'w') as f:
                    json.dump(deleted, f)
                
                await ctx.channel.purge(limit=amount+1, check=self.is_person)
            else:
                await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.send("You're not allowed to use this spell!")
    

    @nextcord.slash_command(name="todos", description="Returns the current active commissions.")
    async def todos(self, ctx):
        todos = open("Party Wizard/todos.txt", "r")
        if(todos.read() == ''):
            await ctx.send("I have completed all spells. Commission more for me to start working again.")
        else:
            todosfile = open("Party Wizard/todos.txt", "r")
            todos = todosfile.read()
            await ctx.send("These are the spells I'm currently working on:\n" + todos)
        todosfile.close()
    
    @nextcord.slash_command(name="commission", description="Sends text to a text file on my computer.")
    async def commission(self, ctx, thecommision):
        todos = open("Party Wizard/todos.txt", "a")
        todos.write(f'{thecommision} - {ctx.user.id}\n')
        await ctx.send(f'Added "{thecommision}" to the to-do list.')
        todos.close()
        await self.Karma.add_karma(ctx, 50)

    @nextcord.slash_command(name="ping", description="Sends latency")
    async def ping(self, ctx):
        await ctx.send(f'{int(self.bot.latency * 1000)}ms latency.')
    

    @nextcord.slash_command(name="stop", description="Stops the bot for 60s")
    async def stop(self, ctx):
        await ctx.send(':sleeping:Sleeping for 60 seconds, see you then!')
        time.sleep(60)
        await self.Karma.add_karma(ctx, 1)
    
    @nextcord.slash_command(name="broadcast", description="Broadcasts message to all wizard channels")
    async def broadcast(self, ctx, message):
        campaigns = await self.Scheduling.get_campaign_data()
        if(ctx.user.id == 154979334002704384):
            for campaign in campaigns:
                await self.bot.wait_until_ready()
                channel = self.bot.get_channel(campaigns[campaign]["channel"])
                await channel.send("Broadcast from the bot's developer:")
                await channel.send(message)
        else:
            await ctx.send("Only the dev can use this.")
    
    @nextcord.slash_command(name="bot_link", description="Gives the bot invite link.")
    async def botLink(self, ctx):
        await ctx.send("Invite me to your server :grin: \nhttps://discord.com/api/oauth2/authorize?client_id=791887063901274123&permissions=8&scope=bot%20applications.commands")



def setup(bot):
    bot.add_cog(Utility(bot))