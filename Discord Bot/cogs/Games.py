import discord, json
import random as rd
from discord.ext import commands
from .Karma import Karma
from .Checkers.checkers.game import Game

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.karma = Karma(bot)
    
    allgames = set()
    gamestrings = ["Checkers"]
    for thing in gamestrings:
        allgames.add(thing)
    
    async def get_game_data(self):
        with open("01TrainingCode/Discord Bot/cogs/games.json", 'r') as f:
            games = json.load(f)
        return games

    async def check_for_existing_game(self, authorID, opponentID, currgame):
        games = await self.get_game_data()

        i = 0

        while games[str(i)]["Active"] == True:
            if  games[str(i)]["Game"] == currgame:
                if games[str(i)]["Players"]['1'] == str(authorID):
                    if games[str(i)]["Players"]['2'] == str(opponentID):
                        return True
                elif games[str(i)]["Players"]['1'] == str(opponentID):
                    if games[str(i)]["Players"]['2'] == str(authorID):
                        return True
            i += 1
        return False


    async def startgame(self, ctx, opponentID, currgame):
        games = await self.get_game_data()

        for i in range(0, 256):
            if games[str(i)]["Active"] == False:
                games[str(i)]["Active"] = True
                games[str(i)]["Game"] = currgame
                games[str(i)]["Players"]['1'] = str(ctx.author.id)
                games[str(i)]["Players"]['2'] = opponentID
                if currgame == "Checkers":
                    games[str(i)]["Data"]['Turn'] = 'White'
                    #TODO add board repr to json file, make game work. This will take some time.
                    games[str(i)]["Data"]['Board'] = 'TODO'
                break
        
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
    async def startGame(self, ctx, otherplayer, game):
        if game not in self.allgames:
            await ctx.send("I'm sorry, but we either don't have that game, or you misspelled something.\nUse the command getGames to see all available games and their spelling.")
            return
        otherplayer = otherplayer[3:-1]
        if not await self.check_for_existing_game(ctx.author.id, otherplayer, game):
            await self.startgame(ctx, otherplayer, game)
            await ctx.send(f"You started a new {game} game with <@!{otherplayer}>")
        else:
            await ctx.send(f"You already have a game of {game} with this person!")

    @commands.command()
    async def getGames(self, ctx):
        await ctx.send(self.allgames)

    @commands.command()
    async def resetGames(self, ctx):
        """Debug, only for developer."""
        if ctx.author.id == 154979334002704384:
            games = {}
            for i in range(0, 256):
                games[i] = {}
                games[i]["Active"] = False
                games[i]["Game"] = None
                games[i]["Players"] = {}
                games[i]["Players"][1] = None
                games[i]["Players"][2] = None
                games[i]["Data"] = {}
            with open('01TrainingCode/Discord Bot/cogs/games.json', 'w') as f:
                json.dump(games,f)
        else:
            await ctx.send("You don't have the rights to cast that much destruction!")

def setup(bot):
    bot.add_cog(Games(bot))