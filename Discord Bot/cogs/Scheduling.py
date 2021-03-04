import discord
import json
import asyncio
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

            await asyncio.sleep(20)

            schedules = await self.get_campaign_data()

            for campaign in schedules:

                await self.bot.wait_until_ready()

                channel = self.bot.get_channel(schedules[campaign]["channel"])

                current_time = datetime.now().strftime("%A, %H:%M")

                camp_time = schedules[campaign]["time"]

                if(current_time == camp_time):
                    for i in range(5):
                        await channel.send("THE TIME IS NOW, REJOICE!\n@everyone")
                    await self.bot.change_presence(activity=discord.Game(status[0]))
                else:
                    await self.bot.change_presence(activity=discord.Game(status[1]))

    async def add_campaign(self, ctx):
        campaigns = await self.get_campaign_data()

        if str(ctx.guild.id) in campaigns:
            return
        else:
            campaigns[str(ctx.guild.id)] = {}
            campaigns[str(ctx.guild.id)]["time"] = 0
            campaigns[str(ctx.guild.id)]["channel"] = ctx.channel.id
            await ctx.send("This channel has been set as the main announcement channel. If this is not the channel I should be spamming, go to the appropriate channel and call 'wizard setChannel'")

        with open("01TrainingCode/Discord Bot/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)

    async def get_campaign_data(self):
        with open("01TrainingCode/Discord Bot/cogs/campaigns.json", 'r') as f:
            campaigns = json.load(f)
        return campaigns


    async def getIfPartyTime(self, ctx):

        await self.add_campaign(ctx)

        campaigns = await self.get_campaign_data()

        time = campaigns[str(ctx.guild.id)]["time"]

        now = datetime.now()
        current_time = now.strftime("%A, %H:%M")
        if(current_time == time):
            return True
        else:
            return False

    @commands.command()
    async def setChannel(self, ctx):
        """Sets the current channel as the main channel"""
        await self.add_campaign(ctx)

        campaigns = await self.get_campaign_data()

        campaigns[str(ctx.guild.id)]["channel"] = ctx.channel.id

        with open("01TrainingCode/Discord Bot/cogs/campaigns.json", 'w') as f:
            json.dump(campaigns, f)
        
        await ctx.send("This channel is now the main wizard channel.")


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

        await self.add_campaign(ctx)

        campaigns = await self.get_campaign_data()
        
        em = discord.Embed(title = f"{ctx.guild}'s campaign's info:", color=discord.Colour.magenta())
        
        await self.bot.wait_until_ready()

        time = campaigns[str(ctx.guild.id)]["time"]
        channel = self.bot.get_channel(campaigns[str(ctx.guild.id)]["channel"])

        em.add_field(name="Channel: ", value=channel)
        em.add_field(name="Time: ", value=time)

        await ctx.send(embed=em)

    @commands.command()
    async def setMeetingTime(self, ctx, weekday=datetime.now().strftime('%A'), time=datetime.now().strftime('%H:%M')):
        """Sets the meeting time of the server's campaign."""

        await self.add_campaign(ctx)

        timestring = f'{weekday}, {time}'

        campaigns = await self.get_campaign_data()

        campaigns[str(ctx.guild.id)]["time"] = timestring

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
