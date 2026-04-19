import discord
from discord import app_commands


async def respond(interaction: discord.Interaction, *args, ephemeral=True, **kwargs):
    kwargs["ephemeral"] = ephemeral
    if interaction.response.is_done():
        return await interaction.followup.send(*args, **kwargs)
    return await interaction.response.send_message(*args, **kwargs)


async def defer(interaction: discord.Interaction, *, ephemeral=True, thinking=True):
    if not interaction.response.is_done():
        await interaction.response.defer(ephemeral=ephemeral, thinking=thinking)


async def owner_check(interaction: discord.Interaction):
    if hasattr(interaction.client, "is_owner"):
        return await interaction.client.is_owner(interaction.user)
    return False


def owner_only():
    return app_commands.check(owner_check)


def chunk_values(values, *, separator=", ", max_length=1000):
    chunks = []
    current = ""

    for value in values:
        candidate = value if not current else f"{current}{separator}{value}"
        if len(candidate) <= max_length:
            current = candidate
            continue

        if current:
            chunks.append(current)
        current = value

    if current:
        chunks.append(current)

    return chunks or ["無"]
