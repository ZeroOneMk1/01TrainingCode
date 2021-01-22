import discord
import random as rd
from datetime import datetime
from discord.ext import commands, tasks
import time
import json
import os

cfile = open('01TrainingCode/Discord Bot/code.txt', 'r')
stopped = False
client = commands.Bot(command_prefix='wizard ')
status = ["it's time!", "it's not time yet..."]
classes = ['Artificer', 'Blood Hunter', 'Bard', 'Barbarian', 'Cleric', 'Druid',
           'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
guilds = [792311682898460693, 769850094353776654]
wizchannels = [792311682898460693, 769850094353776654]
schedstrings = ['01TrainingCode/Discord Bot/schedule.txt',
                '01TrainingCode/Discord Bot/schedule copy.txt']


@client.command(aliases=['sleep', 'nappytime', 'naptime', 'nap'])
async def stop(ctx):
    """Stops the bot for 60s"""
    await ctx.send(':sleeping:Sleeping for 60 seconds, see you then!')
    time.sleep(60)


@tasks.loop(seconds=5)
async def checkTime():
    """Checks if there is a session going on."""
    schedules = []
    schedules.append(open("01TrainingCode/Discord Bot/schedule.txt", "r"))
    schedules.append(open("01TrainingCode/Discord Bot/schedule copy.txt", "r"))

    for i in range(2):
        await client.wait_until_ready()
        channel = client.get_channel(guilds[i])

        current_time = datetime.now().strftime("%A, %H:%M")
        if(current_time == schedules[i].read()):
            schedules[i].close()
            for i in range(5):
                await channel.send("THE TIME IS NOW, REJOICE!\n@everyone")
            await client.change_presence(activity=discord.Game(status[0]))
        else:
            schedules[i].close()
            await client.change_presence(activity=discord.Game(status[1]))


@client.event
async def on_ready():
    checkTime.start()
    print("Ready")


@client.command()
async def ping(ctx):
    """Sends latency"""
    await ctx.send(f'{int(client.latency * 1000)}ms latency.')


@client.command()
async def commission(ctx, *, thecommision):
    """Sends text to a text file on my computer."""
    todos = open("01TrainingCode/Discord Bot/todos.txt", "a")
    todos.write(f'{thecommision}\n')
    await ctx.send(f'Added "{thecommision}" to the to-do list.')
    todos.close()


@client.command(aliases=['randClass', 'class', 'gimme class'])
async def randomClass(ctx):
    """Returns one random class."""
    rd.shuffle(classes)
    await ctx.send("Your random class is " + classes[0])


@client.command(aliases=['randRace', 'race', 'gimmeRace'])
async def randomRace(ctx):
    """Returns one random race."""
    racesfile = open("01TrainingCode/Discord Bot/races.txt", "r")
    races = racesfile.readlines()
    rd.shuffle(races)
    await ctx.send(f"Your random race is:\n```{races[0]}```Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
    racesfile.close()


@client.command(aliases=['randFeat', 'feat', 'gimmeFeat'])
async def randomFeat(ctx):
    """Returns one random feat."""
    featsfile = open("01TrainingCode/Discord Bot/feats.txt", "r")
    feats = featsfile.readlines()
    rd.shuffle(feats)
    await ctx.send(f"Your random feat is:\n```{feats[0]}```Visit http://www.jsigvard.com/dnd/Feats.html for more information on this feat.")
    featsfile.close()


@client.command(aliases=['character', 'gimmeCharacter', 'randCharacter', 'char', 'randChar'])
async def randomCharacter(ctx):
    """Generates a random Character with race, class and stats."""
    racesfile = open("01TrainingCode/Discord Bot/races.txt",
                     "r", encoding='utf-8')
    races = racesfile.readlines()
    rd.shuffle(races)
    rd.shuffle(classes)
    await ctx.send(f"Your random Character is of the race:\n```{races[0]}```They are a {classes[0]}, and their stats (without race modifiers) look as such:")
    await rollStats.__call__(ctx)
    await ctx.send("Visit https://www.dandwiki.com/wiki/Alphabetical_5e_Races for more information on this race.")
    racesfile.close()


@client.command(aliases=['69', 'funny number'])
async def nice(ctx):
    """nice"""
    await ctx.send('Nice')


@client.command(aliaes=['love', 'live', 'laugh', 'lovelivelaugh', 'lickmyass'])
async def livelaughlove(ctx):
    """just no"""
    await ctx.send("Watch out there! We got a white girl in our hands! I'll cast mold earth to make some 'magic' crystals as a distraction while you get her!")


@client.command(aliases=['commissions', 'toDo', 'toDos'])
async def todos(ctx):
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


@client.command()
async def spam(ctx, person, amount=1):
    """Spams the message you input."""
    for i in range(int(amount)):
        await ctx.send(person)


@client.command()
async def guess(ctx, theguess):
    """Guess a random number between 1 and 10 and checks if you got it."""
    temp = rd.randint(1, 10)
    try:
        int(theguess)
    except:
        await ctx.send('The stars didn\'t align, or you were just stupid. Try again, but with a number this time :angry:.')
        return

    if(int(theguess) == temp):
        await ctx.send('Correct! Are you a divination wizard by chance?')
    else:
        await ctx.send(f'Gotta work on those divination spells, huh?\nThe true value was {temp}.')


@client.command(aliases=['d', 'dice'])
async def roll(ctx, die=20, amount=1):
    """Rolls some dice."""
    total = 0
    rolls = []
    await ctx.send(":arrow_down: Contacting fate:")
    for i in range(int(amount)):
        curr = rd.randint(1, int(die))
        rolls.append(curr)
        total += curr
    await ctx.send(rolls)
    await ctx.send(f'The total is {total}.')


@client.command()
async def check(ctx, die=20, mod=0, operator='plus'):
    """Rolls one dice with a modifier on it."""
    if(operator == 'plus'):
        await ctx.send(rd.randint(1, int(die)) + int(mod))
    elif(operator == 'minus'):
        await ctx.send(rd.randint(1, int(die)) - int(mod))
    else:
        await ctx.send("I don't understand, please try again.")


@client.command(aliases=['adv'])
async def advantage(ctx, die=20):
    """Rolls with advantage"""
    await ctx.send(":arrow_down: Contacting fate, with advantage:")
    curr1 = rd.randint(1, int(die))
    curr2 = rd.randint(1, int(die))
    await ctx.send(str(curr1) + ', ' + str(curr2))
    if(curr1 < curr2):
        await ctx.send('Final: ' + str(curr2))
    else:
        await ctx.send('Final: ' + str(curr1))


@client.command(aliases=['disadv'])
async def disadvantage(ctx, die=20):
    """Rolls with disadvantage."""
    await ctx.send(":arrow_down: Contacting fate, with disadvantage:")
    curr1 = rd.randint(1, int(die))
    curr2 = rd.randint(1, int(die))
    await ctx.send(str(curr1) + ', ' + str(curr2))
    if(curr1 > curr2):
        await ctx.send('Final: ' + str(curr2))
    else:
        await ctx.send('Final: ' + str(curr1))


@client.command(aliases=['stats', 'rollstats', 'randomstats', 'randstats'])
async def rollStats(ctx):
    """Rolls an array of 6 4d6 drop lowest stats."""
    await ctx.send(":arrow_down: Contacting fate:")
    rolls = []
    stats = []
    for i in range(6):
        for j in range(4):
            rolls.append(rd.randint(1, 6))
        rolls.sort()
        rolls.pop(0)
        stats.append(rolls[0] + rolls[1] + rolls[2])
        rolls.clear()
    stats.sort()
    await ctx.send(f'Your stats, in ascending order, are: {stats}')


@client.command()
async def rollHP(ctx, lvl, dice, conmod):
    """Rolls the maximum HP for your character."""
    sum = int(dice) + int(conmod)
    for i in range(int(lvl) - 1):
        sum += rd.randint(1, int(dice)) + int(conmod)
    await ctx.send("Your maximum HP is: " + str(sum))


@client.command()
async def setZachMeetingTime(ctx, weekday=datetime.now().strftime('%A'), time=datetime.now().strftime('%H:%M')):
    """Sets the meeting time of Zach's campaign."""
    schedule = open("01TrainingCode/Discord Bot/schedule.txt", "w")
    schedule.write(f'{weekday}, {time}')
    await ctx.send(f"Changed the meeting time to {weekday}, {time}")
    schedule.close()


@client.command()
async def setKyleMeetingTime(ctx, weekday=datetime.now().strftime('%A'), time=datetime.now().strftime('%H:%M')):
    """Sets the meeting time of Kyle's campaign."""
    schedule = open("01TrainingCode/Discord Bot/schedule copy.txt", "w")
    schedule.write(f'{weekday}, {time}')
    await ctx.send(f"Changed the meeting time to {weekday}, {time}")
    schedule.close()


@client.command()
async def getZachMeetingTime(ctx):
    """Gets the meeting time of Zach's campaign."""
    schedule = open("01TrainingCode/Discord Bot/schedule.txt", "r")
    await ctx.send(f'We meet on {schedule.read()}')
    schedule.close()


@client.command()
async def getKyleMeetingTime(ctx):
    """Gets the meeting time of Kyle's campaign."""
    schedule = open("01TrainingCode/Discord Bot/schedule copy.txt", "r")
    await ctx.send(f'We meet on {schedule.read()}')
    schedule.close()


@client.command()
async def thanks(ctx, *, pog=''):
    """Thanks"""
    await ctx.send("Any time, my student.")
    await open_account(ctx.author)
    await add_karma(ctx, 1000)


@client.command(aliases=['curse'])
async def cursed(ctx, lvl=0):
    """Immortalizes the cursedness of thy post above."""
    await ctx.channel.purge(limit=1)
    if(abs(lvl) == 0):
        await ctx.send("This is cursed.")
    elif(abs(lvl) % 10 == 1):
        await ctx.send(f"Woaah there, this is cursed to the {lvl}st level!")
    elif(abs(lvl) % 10 == 2):
        await ctx.send(f"Woaah there, this is cursed to the {lvl}nd level!")
    elif(abs(lvl) % 10 == 3):
        await ctx.send(f"Woaah there, this is cursed to the {lvl}rd level!")
    else:
        await ctx.send(f"Woaah there, this is cursed to the {lvl}th level!")
    if(lvl > 8):
        await ctx.send("I'll need a wish spell to unsee this! Anyone have spare GP?")


@client.command()
async def getTime(ctx):
    """Gets the current time."""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    await ctx.send("Current Time = " + current_time)
    current_day = now.strftime("%A")
    await ctx.send("It's " + current_day + " today.")


def getIfZachPartyTime():
    schedule = open("01TrainingCode/Discord Bot/schedule.txt", "r")
    now = datetime.now()
    current_time = now.strftime("%A, %H:%M")
    if(current_time == schedule.read()):
        schedule.close()
        return True
    else:
        schedule.close()
        return False


def getIfKylePartyTime():
    schedule = open("01TrainingCode/Discord Bot/schedule copy.txt", "r")
    now = datetime.now()
    current_time = now.strftime("%A, %H:%M")
    if(current_time == schedule.read()):
        schedule.close()
        return True
    else:
        schedule.close()
        return False


@client.command(aliases=['clear',  'erase', 'purge'])
async def delete(ctx, amount=1):
    """Deletes messages."""
    await ctx.channel.purge(limit=amount+1)


@client.command(aliases=['say'])
async def repeat(ctx, *, message):
    """Repeats a message."""
    if(message == "I'm gay"):
        await ctx.send('I know')
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send(message)


# ! DANGEROUS
# @client.command()
# async def makeRole(ctx, name, color):
#     await client.wait_until_ready()
#     guild = client.get_guild(706471625544957972)
#     await guild.create_role(name=name, colour=discord.Colour(int(color, 16)))

@client.command()
async def map(ctx):
    """Returns the current map for the campaign."""
    await ctx.channel.send(file=discord.File('01TrainingCode\Discord Bot\map.png'))

# ? Doesn't work
# @client.command()
# async def setMap(ctx, map):
#     premap = open('01TrainingCode\Discord Bot\map.png', 'w')
#     premap.write(map)


@client.command()
async def rainbowTime(ctx):
    """Does nothing atm."""
    await client.wait_until_ready()
    guild = ctx.guild
    roles = await guild.fetch_roles()
    for role in roles:
        if role not in ctx.author.roles:
            await ctx.author.add_roles(role)
            await ctx.author.remove_roles(role)


@client.command(aliases=['partyTime?', 'pogTime?', 'time?'])
async def zachPartyTime(ctx):
    """Gets if Zach's campaign is currently on."""
    if(getIfZachPartyTime()):
        await ctx.send("THE TIME IS NOW, REJOICE!\n@everyone")
    else:
        schedule = open("01TrainingCode/Discord Bot/schedule.txt", "r")
        await ctx.send("We shall wait yet for the time to come... \nSoon brother, soon...")
        await ctx.send(f'We meet on {schedule.read()}')
        schedule.close()


@client.command(aliases=['loreTime?', 'poggerTime?'])
async def kylePartyTime(ctx):
    """Gets if Kyle's campaign is currently on."""
    if(getIfZachPartyTime()):
        await ctx.send("THE TIME IS NOW, REJOICE!\n@everyone")
    else:
        schedule = open("01TrainingCode/Discord Bot/schedule copy.txt", "r")
        await ctx.send("We shall wait yet for the time to come... \nSoon brother, soon...")
        await ctx.send(f'We meet on {schedule.read()}')
        schedule.close()


@client.command()
async def clapify(ctx, *, text):
    """Replaces spaces with :clap:"""
    newtext = text.replace(' ', ':clap:')
    await ctx.channel.purge(limit=1)
    await ctx.send(newtext)


@client.command()
async def karma(ctx):
    """Returns your current karma."""
    await open_account(ctx.author)

    users = await get_bank_data()

    karma = users[str(ctx.author.id)]

    em = discord.Embed(
        title=f"{ctx.author.name}, this is your karma.", color=discord.Colour.magenta())
    em.add_field(name="Karma", value=karma)

    await ctx.send(embed=em)


@client.command()
async def makeMeRich(ctx, bal):
    """Only for daddy."""
    await open_account(ctx.author)

    try:
        pog = int(bal)
    except:
        await ctx.send("Fuck off.")
        return

    if(ctx.author.id == 154979334002704384):
        await add_karma(ctx, bal)

    else:
        await ctx.send("You're not my dad!")


@client.command()
async def beg(ctx):
    """Gives a random amount of money to the peasant casting the spell."""
    await open_account(ctx.author)

    scraps = rd.randint(1, 100)

    await add_karma(ctx, scraps)
    await ctx.send("Peasant...")


async def open_account(author):

    users = await get_bank_data()

    if str(author.id) in users:
        return
    else:
        users[str(author.id)] = 0

    with open("01TrainingCode/Discord Bot/karma.json", 'w') as f:
        json.dump(users, f)


async def get_bank_data():
    with open("01TrainingCode/Discord Bot/karma.json", 'r') as f:
        users = json.load(f)
    return users


async def add_karma(ctx, amount):
    await open_account(ctx.author)

    users = await get_bank_data()

    karma = users[str(ctx.author.id)]

    karma += int(amount)

    users[str(ctx.author.id)] = karma

    await ctx.send(f"Your new karma is {karma}")

    with open("01TrainingCode/Discord Bot/karma.json", 'w') as f:
        json.dump(users, f)



client.run(cfile.read())
