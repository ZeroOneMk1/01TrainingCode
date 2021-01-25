import discord, time
from discord.ext import commands
from .Karma import Karma

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
    
    @commands.command(aliases=['clear',  'erase', 'purge'])
    async def delete(self, ctx, amount=1):
        """Deletes messages."""
        await ctx.channel.purge(limit=amount+1)
    

    @commands.command(aliases=['commissions', 'toDo', 'toDos'])
    async def todos(self, ctx):
        """Returns the current active commissions."""
        todos = open("01TrainingCode/Discord Bot/todos.txt", "r")
        if(todos.read() == ''):
            await ctx.send("I have completed all spells. Commission more for me to start working again.")
        else:
            todosfile = open("01TrainingCode/Discord Bot/todos.txt", "r")
            todos = todosfile.read()
            print(todos)
            await ctx.send("These are the spells I'm currently working on:\n" + todos)
        todosfile.close()
    
    @commands.command()
    async def commission(self, ctx, *, thecommision):
        """Sends text to a text file on my computer."""
        todos = open("01TrainingCode/Discord Bot/todos.txt", "a")
        todos.write(f'{thecommision}\n')
        await ctx.send(f'Added "{thecommision}" to the to-do list.')
        todos.close()
        self.Karma.add_karma(ctx, 50)

    @commands.command()
    async def ping(self, ctx):
        """Sends latency"""
        await ctx.send(f'{int(self.bot.latency * 1000)}ms latency.')
    

    @commands.command(aliases=['sleep', 'nappytime', 'naptime', 'nap'])
    async def stop(self, ctx):
        """Stops the bot for 60s"""
        await ctx.send(':sleeping:Sleeping for 60 seconds, see you then!')
        time.sleep(60)

    

def setup(bot):
    bot.add_cog(Utility(bot))