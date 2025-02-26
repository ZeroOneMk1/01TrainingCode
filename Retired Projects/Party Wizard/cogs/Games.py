import nextcord, json
import random as rd
from nextcord.ext import commands
from .Karma import Karma
from .Checkers.checkers.board import Board


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.karma = Karma(bot)
    
    allgames = set()
    gamestrings = ["Checkers"]
    for thing in gamestrings:
        allgames.add(thing)
    
    async def get_game_data(self):
        with open("Party Wizard/cogs/games.json", 'r') as f:
            games = json.load(f)
        return games

    async def check_for_existing_game(self, userID, opponentID, currgame):
        games = await self.get_game_data()

        for i in range(0, 256):
            if games[str(i)]["Active"] == True:
                if  games[str(i)]["Game"] == currgame:
                    if games[str(i)]["Players"]['1'] == str(userID):
                        if games[str(i)]["Players"]['2'] == str(opponentID):
                            return True
                    elif games[str(i)]["Players"]['1'] == str(opponentID):
                        if games[str(i)]["Players"]['2'] == str(userID):
                            return True
        return False

    async def get_game_id(self, userID, opponentID, currgame):
        games = await self.get_game_data()

        i = 0

        while games[str(i)]["Active"] == True:
            if  games[str(i)]["Game"] == currgame:
                if games[str(i)]["Players"]['1'] == str(userID):
                    if games[str(i)]["Players"]['2'] == str(opponentID):
                        return i
                elif games[str(i)]["Players"]['1'] == str(opponentID):
                    if games[str(i)]["Players"]['2'] == str(userID):
                        return i
            i += 1

    async def startgame(self, ctx, opponentID, currgame):
        games = await self.get_game_data()

        for i in range(0, 256):
            if games[str(i)]["Active"] == False:
                games[str(i)]["Active"] = True
                games[str(i)]["Game"] = currgame
                games[str(i)]["Players"]['1'] = str(ctx.user.id)
                games[str(i)]["Players"]['2'] = opponentID
                if currgame == "Checkers":
                    games[str(i)]["Data"]['Turn'] = '1'
                    board = Board()
                    games[str(i)]["Data"]["Board"] = board.__repr__()
                    await ctx.send(board.draw())
                    #TODO make game work. This will take some time.
                break
        
        with open("Party Wizard/cogs/games.json", 'w') as f:
            json.dump(games, f)

    @nextcord.slash_command(name="guess", description="Guess a random number between 1 and 10.")
    async def guess(self, ctx, theguess):
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

    @nextcord.slash_command(name="guess100", description="Guess a random number between 1 and 100.")
    async def guess100(self, ctx, theguess):
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

    @nextcord.slash_command(name="start_game", description="Start a new game from the list of games.")   
    async def startGame(self, ctx, game, otherplayer):
        if game not in self.allgames:
            await ctx.send("I'm sorry, but we either don't have that game, or you misspelled something.\nUse the command getGames to see all available games and their spelling.")
            return
        otherplayer = otherplayer[2:-1]
        try:
            int(otherplayer)
        except:
            otherplayer = otherplayer[1:]
        if not await self.check_for_existing_game(ctx.user.id, otherplayer, game):
            await self.startgame(ctx, otherplayer, game)
            await ctx.send(f"You started a new {game} game with <@!{otherplayer}>")
        else:
            await ctx.send(f"You already have a game of {game} with this person!")

    @nextcord.slash_command(name="get_game", description="Get the state of a currenrly running game.")
    async def getGame(self, ctx, otherplayer, game):
        if game not in self.allgames:
            await ctx.send("I'm sorry, but we either don't have that game, or you misspelled something.\nUse the command getGames to see all available games and their spelling.")
            return
        otherplayer = otherplayer[2:-1]
        try:
            int(otherplayer)
        except:
            otherplayer = otherplayer[1:]

        if not await self.check_for_existing_game(ctx.user.id, otherplayer, game):
            await ctx.send("You currently don't have a game with this person")
        else:
            gamedata = await self.get_game_data()
            gameid = await self.get_game_id(ctx.user.id, otherplayer, game)
            board = Board()
            board.overwrite(gamedata[str(gameid)])
            await ctx.send(board.draw())

    @nextcord.slash_command(name="move", description="move in a game.")
    async def move(self, ctx, game, otherplayer, startpos, endpos):
        if game not in self.allgames:
            await ctx.send("I'm sorry, but we either don't have that game, or you misspelled something.\nUse the command getGames to see all available games and their spelling.")
            return

        otherplayer = otherplayer[2:-1]
        try:
            int(otherplayer)
        except:
            otherplayer = otherplayer[1:]

        if not await self.check_for_existing_game(ctx.user.id, otherplayer, game):
            await ctx.send("You currently don't have a game with this person")
        else:
            if game == 'Checkers':
                
                gamedata = await self.get_game_data()
                gameid = await self.get_game_id(ctx.user.id, otherplayer, game)
                
                if gamedata[str(gameid)]["Players"][gamedata[str(gameid)]["Data"]["Turn"]]  == str(ctx.user.id):
                    
                    board = Board()
                    board.overwrite(gamedata[str(gameid)])

                    turn = gamedata[str(gameid)]["Data"]["Turn"]

                    # TODO        Only aaccept valid moves
                    await ctx.send(board.move(int(startpos[1]) - 1, int(startpos[0]) - 1, int(endpos[1]) - 1, int(endpos[0]) - 1, turn))
                    
                    oldboard = gamedata[str(gameid)]["Data"]["Board"]

                    gamedata[str(gameid)]["Data"]["Board"] = board.__repr__()
                    
                    if board.winner() != 'no':
                        gamedata[str(gameid)]["Active"] = False
                        
                    if oldboard != gamedata[str(gameid)]["Data"]["Board"]:
                        if gamedata[str(gameid)]["Data"]["Turn"] == '1':
                            gamedata[str(gameid)]["Data"]["Turn"] = '2'
                        else:
                            gamedata[str(gameid)]["Data"]["Turn"] = '1'
                    
                    with open("Party Wizard/cogs/games.json", 'w') as f:
                        json.dump(gamedata, f)
                    await ctx.send(board.draw())
                else:
                    await ctx.send("It's not your turn right now.")

    @nextcord.slash_command(name="get_games", description="Displays all games.")
    async def getGames(self, ctx):
        await ctx.send(self.allgames)
        
    @nextcord.slash_command(name="reset_games", description="Resets all games. Only for Developers.")
    async def resetGames(self, ctx):
        """Debug, only for developer."""
        if ctx.user.id == 154979334002704384:
            games = {}
            for i in range(0, 256):
                games[i] = {}
                games[i]["Active"] = False
                games[i]["Game"] = None
                games[i]["Players"] = {}
                games[i]["Players"][1] = None
                games[i]["Players"][2] = None
                games[i]["Data"] = {}
            with open('Party Wizard/cogs/games.json', 'w') as f:
                json.dump(games,f)
            await ctx.send("All games have been purged.")
        else:
            await ctx.send("You don't have the rights to cast that much destruction!")

def setup(bot):
    bot.add_cog(Games(bot))