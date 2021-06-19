import discord, time, json
from discord.ext import commands
from .Karma import Karma
from .Scheduling import Scheduling

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
        self.Scheduling = Scheduling(bot)

    def is_person(self, m):
        with open("Discord Bot/person.json", 'r') as f:
                person = json.load(f)
        return m.author.id == person["person"]

    @commands.command(aliases=['clear',  'erase', 'purge'])
    async def delete(self, ctx, amount=1, person = None):
        """Deletes messages."""
        if ctx.author.guild_permissions.administrator == True or ctx.author.id == 154979334002704384 or ctx.author.guild_permissions.manage_messages == True:
            if person is not None:
                
                person = person[3:-1]

                with open("Discord Bot/person.json", 'r') as f:
                    deleted = json.load(f)
                deleted["person"] = int(person)
                with open("Discord Bot/person.json", 'w') as f:
                    json.dump(deleted, f)
                
                await ctx.channel.purge(limit=amount+1, check=self.is_person)
            else:
                await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.send("You're not allowed to use this spell!")
    

    @commands.command(aliases=['commissions', 'toDo', 'toDos'])
    async def todos(self, ctx):
        """Returns the current active commissions."""
        todos = open("Discord Bot/todos.txt", "r")
        if(todos.read() == ''):
            await ctx.send("I have completed all spells. Commission more for me to start working again.")
        else:
            todosfile = open("Discord Bot/todos.txt", "r")
            todos = todosfile.read()
            await ctx.send("These are the spells I'm currently working on:\n" + todos)
        todosfile.close()
    
    @commands.command()
    async def commission(self, ctx, *, thecommision):
        """Sends text to a text file on my computer."""
        todos = open("Discord Bot/todos.txt", "a")
        todos.write(f'{thecommision} - {ctx.author.id}\n')
        await ctx.send(f'Added "{thecommision}" to the to-do list.')
        todos.close()
        await self.Karma.add_karma(ctx, 50)

    @commands.command()
    async def ping(self, ctx):
        """Sends latency"""
        await ctx.send(f'{int(self.bot.latency * 1000)}ms latency.')
    

    @commands.command(aliases=['sleep', 'nappytime', 'naptime', 'nap'])
    async def stop(self, ctx):
        """Stops the bot for 60s"""
        await ctx.send(':sleeping:Sleeping for 60 seconds, see you then!')
        time.sleep(60)
        await self.Karma.add_karma(ctx, 1)
    
    @commands.command()
    async def broadcast(self, ctx, *, message):
        """Broadcasts message to all wizard channels"""
        campaigns = await self.Scheduling.get_campaign_data()
        if(ctx.author.id == 154979334002704384):
            for campaign in campaigns:
                await self.bot.wait_until_ready()
                channel = self.bot.get_channel(campaigns[campaign]["channel"])
                await channel.send("Broadcast from the bot's developer:")
                await channel.send(message)
        else:
            await ctx.send("Only the dev can use this.")
    
    @commands.command()
    async def botLink(self, ctx):
        """Gives the bot invite link."""
        await ctx.send("Invite me to your server :grin: \nhttps://discord.com/api/oauth2/authorize?client_id=791887063901274123&permissions=8&scope=bot")



def setup(bot):
    bot.add_cog(Utility(bot))