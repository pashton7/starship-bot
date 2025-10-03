import discord
import os
import aiosqlite
from discord.ext import commands, tasks
from discord import interactions
from discord import app_commands
from typing import Literal
from itertools import cycle

from database import DatabaseManager


#intents = discord.Intents.default()
#client = commands.Bot(command_prefix = '!', intents=intents)
status = cycle(['Squishing Bugs','Modding','Pooping'])
class BotMain(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",
            intents= discord.Intents.default()
            
        )
        self.database = None
    
    async def init_db(self) -> None:
            async with aiosqlite.connect(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
            ) as db:
                with open(
                    f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql",
                    encoding = "utf-8"
                ) as file:
                    await db.executescript(file.read())
                await db.commit()
    
    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                except Exception as e:
                    print(e)
        await self.tree.sync()
    
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(status)))
    
    @change_status.before_loop
    async def before_status_task(self) -> None:
       
        await self.wait_until_ready()
    
    async def setup_hook(self):
        await self.init_db()
        await self.load_cogs()
        self.change_status.start()
        self.database = DatabaseManager(
                    connection=await aiosqlite.connect(
                        f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
                    )
                )
    async def on_message(self, message: discord.message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)
       


"""
@client.event
async def on_ready():
        change_status.start()
        await client.change_presence(status=discord.Status.online)
        await client.tree.sync()
        print('Bot is online.')


@client.tree.command(name="warn", description="Warn a user", options = interactions.)
@app_commands.describe(text = "Warn")
async def warnCommand(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"{text}")
"""
client = BotMain()
client.run('MTQyMjY3Nzg2MzQyMDc5Mjk2Mw.GCOqKo.RXqL2NzHJ7eNngaJ1I145QBSrBmA5BWYfX8CHI')