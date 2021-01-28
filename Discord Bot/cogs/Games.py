import discord, json
import random as rd
from discord.ext import commands
from .Karma import Karma
from .Checkers.checkers.game import Game

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.karma = Karma(bot)
    
    allgames = ['Checkers']
    
    async def get_game_data(self):
        with open("01TrainingCode/Discord Bot/cogs/games.json", 'r') as f:
            games = json.load(f)
        return games

    async def startgame(self, ctx, opponentID, currgame):
        games = await self.get_game_data()

        if str(ctx.guild.id) in games:
            if ctx.author.id in games[str(ctx.guild.id)]['players']:
                for game in self.allgames:
                    if game != currgame:
                        games[str(ctx.guild.id)]['players'][ctx.author.id][game] = False
                    else:
                        games[str(ctx.guild.id)]['players'][ctx.author.id][game] = True
            else:
                games[str(ctx.guild.id)]['players'][ctx.author.id] = {}
                for game in self.allgames:
                    if game != currgame:
                        games[str(ctx.guild.id)]['players'][ctx.author.id][game] = False
                    else:
                        games[str(ctx.guild.id)]['players'][ctx.author.id][game] = True
            
            if opponentID in games[str(ctx.guild.id)]['players']:
                for game in self.allgames:
                    if game != currgame:
                        games[str(ctx.guild.id)]['players'][opponentID][game] = False
                    else:
                        games[str(ctx.guild.id)]['players'][opponentID][game] = True
            else:
                games[str(ctx.guild.id)]['players'][opponentID] = {}
                for game in self.allgames:
                    if game != currgame:
                        games[str(ctx.guild.id)]['players'][opponentID][game] = False
                    else:
                        games[str(ctx.guild.id)]['players'][opponentID][game] = True
        else:
            games[str(ctx.guild.id)] = {}
            games[str(ctx.guild.id)]["players"] = {}
            games[str(ctx.guild.id)]['players'][ctx.author.id] = {}
            games[str(ctx.guild.id)]['players'][opponentID] = {}
            for game in self.allgames:
                if game != currgame:
                    games[str(ctx.guild.id)]['players'][ctx.author.id][game] = False
                    games[str(ctx.guild.id)]['players'][opponentID][game] = False
                else:
                    games[str(ctx.guild.id)]['players'][ctx.author.id][game] = True
                    games[str(ctx.guild.id)]['players'][opponentID][game] = True
        
        with open("01TrainingCode/Discord Bot/cogs/games.json", 'w') as f:
            json.dump(games, f)


    @commands.command()
    async def guess(self, ctx, theguess):
        """Guess a random number between 1 and 10."""
        temp = rd.randint(1, 10)
        try:
            int(theguess)
        except:
            await ctx.send('The stars didn\'t align, or you were just stupid. Try again, but with a number this time :angry:.')
            return

        if(int(theguess) == temp):
            await ctx.send('Correct! Are you a divination wizard by chance?')
            await self.karma.add_balance(ctx, 200)
        else:
            await ctx.send(f'Gotta work on those divination spells, huh?\nThe true value was {temp}.')

    @commands.command()
    async def guess100(self, ctx, theguess):
        """Guess a random number between 1 and 100."""
        temp = rd.randint(1, 100)
        try:
            int(theguess)
        except:
            await ctx.send('The stars didn\'t align, or you were just stupid. Try again, but with a number this time :angry:.')
            return

        if(int(theguess) == temp):
            await ctx.send('Correct! Are you a divination wizard by chance?')
            await self.karma.add_balance(ctx, 5000)
        else:
            await ctx.send(f'Gotta work on those divination spells, huh?\nThe true value was {temp}.')

    @commands.command(aliases = ['checkers', 'Checkers'])
    async def startCheckers(self, ctx, otherplayer):
        otherplayer = otherplayer[3:-1]
        await self.startgame(ctx, otherplayer, 'Checkers')

def setup(bot):
    bot.add_cog(Games(bot))