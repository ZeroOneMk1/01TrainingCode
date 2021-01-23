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

token = open('01TrainingCode/Discord Bot/code.txt', 'r')

@bot.event
async def on_ready():
    print("Ready")


bot.run(token.read())
