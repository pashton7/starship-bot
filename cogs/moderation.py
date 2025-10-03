import os
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

def modTypeConvert(mod_type: str):
    if mod_type == "warn":
        return "Warned"
    else:
        return mod_type

class Moderation(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="test", description="test command")
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("boi")
    
    @app_commands.command(
        name="warn",
        description="Adds a warning to a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="The user that should be warned.",
        reason="The reason why the user should be warned.",
    )
    async def warning_add(
        self, interaction: discord.Interaction, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        author = interaction.user
        member = interaction.guild.get_member(user.id) or await interaction.guild.fetch_member(
            user.id
        )
        total = await self.bot.database.add_log(
            user.id, interaction.guild.id, author.id, "warn", reason
        )
        embed = discord.Embed(
            description=f"**{member}** was warned by **{author}**!\nTotal warns for this user: {total}",
            color=0xBEBEFE,
        )
        embed.add_field(name="Reason:", value=reason)
        await interaction.response.send_message(embed=embed)
        try:
            await member.send(
                f"You were warned by **<@{author.id}>** in **{interaction.guild.name}**!\nReason: {reason}"
            )
        except:
            # Couldn't send a message in the private messages of the user
            await interaction.response.send_message(
                f"{member.mention}, you were warned by **<@{author.id}>**!\nReason: {reason}"
            )
    @app_commands.command(name="modlog",description="Returns all moderations of a user.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user = "The user to retrieve logs of."
    )
    async def getModLog(self, interaction: discord.Interaction, user: discord.User) -> None:
        moderations_list = await self.bot.database.get_warnings(user.id, interaction.guild.id)
        embed = discord.Embed(title=f"Moderations of <@{user.id}>:", color=0xBEBEFE)
        description = ""
        if len(moderations_list) == 0:
            description = "This user has no infractions."
        else:
            for moderation in moderations_list:
                description += f"• {modTypeConvert(moderation[3])} by <@{moderation[2]}>: **{moderation[4]}** (<t:{moderation[5]}>) - Warn ID #{moderation[6]}\n"
        embed.description = description
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.bot) -> None:
    await bot.add_cog(Moderation(bot))