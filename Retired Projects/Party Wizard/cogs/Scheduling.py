import nextcord
import json
import asyncio
from datetime import datetime, timedelta, time, timezone
from nextcord.ext import commands, tasks
from .consts import status, weekdays

class Scheduling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.bg_task = self.loop.create_task(self.checkTime())

    async def checkTime(self):
        """Checks if there is a session going on."""
        while True:

            await asyncio.sleep(20)

            schedules = await self.get_campaign_data()

            for campaign in schedules:

                await self.bot.wait_until_ready()

                channel = self.bot.get_channel(schedules[campaign]["channel"])

                current_time = (datetime.now() - timedelta(hours=8)).strftime("%A, %H:%M")

                camp_time = schedules[campaign]["time"]

                # print(camp_time, current_time)

                if(current_time == camp_time):
                    # print("match")
                    for i in range(5):
                        await channel.send("THE TIME IS NOW, REJOICE!\n@everyone")
                    await self.bot.change_presence(activity=nextcord.Game(status[0]))
                else:
                    # print("No match")
                    await self.bot.change_presence(activity=nextcord.Game(status[1]))

    async def add_campaign(self, ctx):
        campaigns = await self.get_campaign_data()

        if str(ctx.guild.id) in campaigns:
            return
        else:
            campaigns[str(ctx.guild.id)] = {}
            campaigns[str(ctx.guild.id)]["time"] = 0
            campaigns[str(ctx.guild.id)]["channel"] = ctx.channel.id
            await ctx.send("This channel has been set as the main announcement channel. If this is not the channel I should be spamming, go to the appropriate channel and call 'wizard setChannel'")

        with open("Party Wizard/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)

    async def get_campaign_data(self):
        with open("Party Wizard/cogs/campaigns.json", 'r') as f:
            campaigns = json.load(f)
        return campaigns


    async def getIfPartyTime(self, ctx):

        await self.add_campaign(ctx)

        campaigns = await self.get_campaign_data()

        time = campaigns[str(ctx.guild.id)]["time"]

        now = datetime.now() - timedelta(hours=8)
        current_time = now.strftime("%A, %H:%M")
        if(current_time == time):
            return True
        else:
            return False

    @nextcord.slash_command(name="set_channel", description="Sets the current channel as the main channel")
    async def setChannel(self, ctx):
        await self.add_campaign(ctx)

        campaigns = await self.get_campaign_data()

        campaigns[str(ctx.guild.id)]["channel"] = ctx.channel.id

        with open("Party Wizard/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)
        
        await ctx.send("This channel is now the main wizard channel.")


    @nextcord.slash_command(name="get_time", description="Gets the current time.")
    async def getTime(self, ctx):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        await ctx.send("Current time at my location = " + current_time)
        current_day = now.strftime("%A")
        await ctx.send("It's " + current_day + " today.")

    @nextcord.slash_command(name="get_meeting_time", description="Gets the meeting time of the server's campaign.")
    async def getMeetingTime(self, ctx, timezone = "0"):

        await self.add_campaign(ctx)

        campaigns = await self.get_campaign_data()
        
        em = nextcord.Embed(title = f"{ctx.guild}'s campaign's info:", color=nextcord.Colour.magenta())
        
        await self.bot.wait_until_ready()

        daytime = campaigns[str(ctx.guild.id)]["time"]

        day, time = daytime.split(", ")[0], daytime.split(", ")[1]

        day, time = await self.convert_times_to_tz(day, time, timezone)

        daytime = f"{day}, {time}"

        channel = self.bot.get_channel(campaigns[str(ctx.guild.id)]["channel"])

        if int(timezone) == 0:
            timezone = ""
        elif "+" not in timezone and "-" not in timezone:
            timezone = "+" + timezone
            

        em.add_field(name="Channel: ", value=channel)
        em.add_field(name="Time: ", value=f"{daytime} (GMT{timezone})")

        await ctx.send(embed=em)

    @nextcord.slash_command(name="set_meeting_time", description="Sets the meeting time of the server's campaign.")
    async def setMeetingTime(self, ctx, weekday=(datetime.now() - timedelta(hours=8)).strftime('%A'), time=(datetime.now() - timedelta(hours=8)).strftime('%H:%M'), timezone = "0"):

        await self.add_campaign(ctx)

        weekday, time = await self.convert_times_from_tz(weekday, time, timezone)

        timestring = f'{weekday}, {time}'

        campaigns = await self.get_campaign_data()

        campaigns[str(ctx.guild.id)]["time"] = timestring

        with open("Party Wizard/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)

        await ctx.send(f"Changed the meeting time to {weekday}, {time} GMT")

    async def convert_times_from_tz(self, weekday, time, timezone):

        if int(time.split(":")[0]) - int(timezone) > 23:
            weekday = weekdays[(weekdays.index(weekday) - 1) % 7]
            
        elif int(time.split(":")[0]) - int(timezone) < 0:
            weekday = weekdays[(weekdays.index(weekday) + 1) % 7]
        
        if (int(time.split(':')[0]) - int(timezone)) % 24 < 10:
            time = f"0{(int(time.split(':')[0]) - int(timezone)) % 24}:{time.split(':')[1]}"     
        else:
            time = f"{(int(time.split(':')[0]) - int(timezone)) % 24}:{time.split(':')[1]}"     

        return weekday, time
    
    async def convert_times_to_tz(self, weekday, time, timezone):

        if int(time.split(":")[0]) + int(timezone) > 23:
            weekday = weekdays[(weekdays.index(weekday) + 1) % 7]
        elif int(time.split(":")[0]) + int(timezone) < 0:
            weekday = weekdays[(weekdays.index(weekday) - 1) % 7]

        time = f"{(int(time.split(':')[0]) + int(timezone)) % 24}:{time.split(':')[1]}"

        return weekday, time


    @nextcord.slash_command(name="party_time", description="Party Time?!")
    async def partyTime(self, ctx):
        """Gets if the server's campaign is currently on."""
        if(await self.getIfPartyTime(ctx)):
            await ctx.send("THE TIME IS NOW, REJOICE!\n@everyone")
        else:
            await ctx.send("We shall wait yet for the time to come... \nSoon brother, soon...")


def setup(bot):
    bot.add_cog(Scheduling(bot))
