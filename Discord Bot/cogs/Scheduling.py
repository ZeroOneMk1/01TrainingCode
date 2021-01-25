import discord, json, asyncio
from datetime import datetime
from discord.ext import commands, tasks
from .consts import status, guilds


class Scheduling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.bg_task = self.loop.create_task(self.checkTime())
    
    async def checkTime(self):
        """Checks if there is a session going on."""
        while True:

            await asyncio.sleep(10)

            schedules = await self.get_campaign_data()
            i = 0
            for time in schedules:

                await self.bot.wait_until_ready()

                channel = self.bot.get_channel(guilds[i])

                current_time = datetime.now().strftime("%A, %H:%M")
                
                if(current_time == time):
                    for i in range(5):
                        await channel.send("THE TIME IS NOW, REJOICE!\n@everyone")
                    await self.bot.change_presence(activity=discord.Game(status[0]))
                else:
                    await self.bot.change_presence(activity=discord.Game(status[1]))
                i += 1

    
    async def getIfPartyTime(self, ctx):

        await self.add_campaign(ctx.guild)

        campaigns = await self.get_campaign_data()

        time = campaigns[str(ctx.guild.id)]

        now = datetime.now()
        current_time = now.strftime("%A, %H:%M")
        if(current_time == time):
            return True
        else:
            return False

    async def add_campaign(self, guild):
        campaigns = await self.get_campaign_data()
        
        if str(guild.id) in campaigns:
            return
        else:
            campaigns[str(guild.id)] = 0

        with open("01TrainingCode/Discord Bot/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)


    async def get_campaign_data(self):
        with open("01TrainingCode/Discord Bot/cogs/campaigns.json", 'r') as f:
            campaigns = json.load(f)
        return campaigns

    @commands.command()
    async def getTime(self, ctx):
        """Gets the current time."""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        await ctx.send("Current Time = " + current_time)
        current_day = now.strftime("%A")
        await ctx.send("It's " + current_day + " today.")
    
    
    @commands.command()
    async def getMeetingTime(self, ctx):
        """Gets the meeting time of the server's campaign."""

        await self.add_campaign(ctx.guild)

        campaigns = await self.get_campaign_data()

        time = campaigns[str(ctx.guild.id)]

        await ctx.send(f'We meet on {time}')
    
    @commands.command()
    async def setMeetingTime(self, ctx, weekday=datetime.now().strftime('%A'), time=datetime.now().strftime('%H:%M')):
        """Sets the meeting time of the server's campaign."""

        await self.add_campaign(ctx.guild)

        timestring = f'{weekday}, {time}'

        campaigns = await self.get_campaign_data()

        campaigns[str(ctx.guild.id)] = timestring

        with open("01TrainingCode/Discord Bot/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)

        await ctx.send(f"Changed the meeting time to {weekday}, {time}")


    @commands.command(aliases=['partyTime?', 'pogTime?', 'time?'])
    async def partyTime(self, ctx):
        """Gets if the server's campaign is currently on."""
        if(await self.getIfPartyTime(ctx)):
            await ctx.send("THE TIME IS NOW, REJOICE!\n@everyone")
        else:
            await ctx.send("We shall wait yet for the time to come... \nSoon brother, soon...")


    

def setup(bot):
    bot.add_cog(Scheduling(bot))