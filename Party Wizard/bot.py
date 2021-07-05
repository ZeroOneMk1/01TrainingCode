import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=['wizard ', 'wiz ', 'Wizard ', 'Wiz '])

initial_extensions = ['cogs.DnD',
                      'cogs.Karma',
                      'cogs.Games', 
                      'cogs.Scheduling', 
                      'cogs.TextBased', 
                      'cogs.Utility',
                      'cogs.BitD']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.command(aliases = ['shelp', 'sh', 'short_help', 'shorthelp', 'hlp'])
async def shortHelp(ctx):
    cogs =  []

    for i in range(len(initial_extensions)):
        currcog = initial_extensions[i][5:]
        cogs.append(currcog)
    
    sendstr = "The current categories are: \n```"

    for cog in cogs:
        sendstr += f" - {cog}\n"
    
    sendstr += "```Write 'wizard help <category>' to get more info."

    await ctx.send(sendstr)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I'm sorry, but you didn't give me the necessary components for the spell. Do wizard help { command } to see what's required.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I'm sorry, but I either don't know this spell, or you gave me false instructions.")

token = open('Party Wizard/code.txt', 'r')

@bot.event
async def on_ready():
    print("Ready")


bot.run(token.read())
