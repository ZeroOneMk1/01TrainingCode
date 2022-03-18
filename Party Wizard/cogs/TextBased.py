import nextcord
from nextcord.ext import commands
from .Karma import Karma
import traceback

class TextBased(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Karma = Karma(bot)
    
    @nextcord.slash_command(name="clapify", description="Replaces spaces with :clap:")
    async def clapify(self, ctx, text):
        newtext = text.replace(' ', ':clap:')
        await ctx.channel.purge(limit=1)
        await ctx.send(newtext)
        await self.Karma.add_karma(ctx, 1)
    
    
    @nextcord.slash_command(name="say", description="Repeats a message.")
    async def say(self, ctx, message):
        if(message == "I'm gay"):
            await ctx.send('I know')
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send(message)
    
    @nextcord.slash_command(name="cursed", description="Immortalizes the cursedness of thy post above.")
    async def cursed(self, ctx, lvl=0):
        # await ctx.channel.purge(limit=1)
        if(abs(lvl) == 0):
            await ctx.send("Wait! Let me cast guidance, cause y'all need Jesus.")
        elif(abs(lvl) == 1):
            await ctx.send(f"Woaah there, I need to drop concentration on Comprehend Languages.")
        elif(abs(lvl) == 2):
            await ctx.send(f"I'm getting a restraining order, I need you out of Misty Step range!")
        elif(abs(lvl) == 3):
            await ctx.send(f"KILL IT WITH FIREBALL! QUICKEN THE SPELL YOU USELESS SORCERER I NEED IT ***NOW***.")
        elif(abs(lvl) == 4):
            await ctx.send(f"Yeah, this definitely deserves Banishment.")
        elif(abs(lvl) == 5):
            await ctx.send(f"Oh lord, I'm unseeing this. MODIFY MEMORY *wooshes wand*")
        elif(abs(lvl) == 6):
            await ctx.send(f"Did someone cast Eyebite? I feel sickened!")
        elif(abs(lvl) == 7):
            await ctx.send(f"That's it. I'm summoning Jesus. CONJURE CELESTIAL *wooshes wand*")
        elif(abs(lvl) == 8):
            await ctx.send(f"I'm casting Mind Blank, I need immunity to the psychic damage you just caused with... that...")
        if(lvl > 8):
            await ctx.send("Good Lord, I'll need a wish spell to unsee this! Anyone have spare GP?")
        await self.Karma.add_karma(ctx, 1)
    

    @nextcord.slash_command(name="spam", description="Spams the message you input. Currently Disabled.")
    async def spam(self, ctx, person, amount=1):
        await ctx.send("Hugo made me diable this. Bad Hugo.")
        # for i in range(int(amount)):
        #     await ctx.send(person)
    
    @nextcord.slash_command(name='69', description= 'funny number')
    async def nice(self, ctx):
        """nice"""
        await ctx.send('Nice')
        await self.Karma.add_karma(ctx, 1)



    @nextcord.slash_command(name="livelaughlove", description="just no")
    async def livelaughlove(self, ctx):
        await ctx.send("Watch out there! We got a white girl in our hands! I'll cast mold earth to make some 'magic' crystals as a distraction while you get her!")
        await self.Karma.add_karma(ctx, 1)


    @nextcord.slash_command(name="uwufy", description="UwU nyaa~~ rawr XD")
    async def uwufy(self, ctx, text):
        await ctx.channel.purge(limit=1)
        text = text.replace("r", "w")
        text = text.replace("l", "w")
        text = text.replace('ove', 'uv')
        await ctx.send(text)
        await self.Karma.add_karma(ctx, 1)
    
    @nextcord.slash_command(name="test_button", description="Test button!")
    async def test_button(self, ctx):
        button = nextcord.ui.Button(label="Test", style=nextcord.ButtonStyle.primary)

        async def test_callback(interaction):
            await interaction.response.send_message("Responded", ephemeral=True)

        button.callback = test_callback
        
        view = nextcord.ui.View()
        view.add_item(button)
        
        await ctx.send("BUUTON", view=view)
        
    

def setup(bot):
    bot.add_cog(TextBased(bot))