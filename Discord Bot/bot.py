import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='wizard ')

initial_extensions = ['cogs.DnD',
                      'cogs.Karma',
                      'cogs.Miscellaneous', 
                      'cogs.Scheduling', 
                      'cogs.TextBased', 
                      'cogs.Utility']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I'm sorry, but you didn't give me enough information to perform this command. Do wizard help { command } to see what's required.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I'm sorry, but I either don't know this spell, or you gave me false instructions.")

token = open('01TrainingCode/Discord Bot/code.txt', 'r')

@bot.event
async def on_ready():
    print("Ready")


bot.run(token.read())
