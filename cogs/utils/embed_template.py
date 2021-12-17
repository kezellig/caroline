from discord import Embed
from datetime import datetime


# Creates nice and simple embed templates for other files.
# dm_auto_embed: automatically sends DMs to user when they have tripped a filter
# dm_manual_embed: manual DM embeds with member argument

async def error_embed(
        ctx,
        title,
        field_name,
        field_value,
        footer,
        colour
):
    embed = Embed(
        title=title,
        color=colour,
    )
    embed.add_field(name=f"{field_name}",
                    value=f"{field_value}")
    embed.set_footer(text=footer)

    await ctx.send(embed=embed)


async def dm_auto_embed(
        message,
        title,
        body,
        footer,
        colour
):
    embed = Embed(
        title=title,
        description=f"{body}",
        color=colour,
    )

    embed.set_footer(text=footer)

    await message.author.send(embed=embed)


async def dm_manual_embed(
        member,
        title,
        body,
        footer,
        colour
):
    embed = Embed(
        title=title,
        description=f"{body}",
        color=colour,
    )

    embed.set_footer(text=footer)

    await member.send(embed=embed)


async def server_embed(
        channel,
        title,
        body,
        footer,
        colour
):
    embed = Embed(
        title=title,
        description=f"{body}",
        color=colour,
    )

    embed.set_footer(text=footer)

    await channel.send(embed=embed)


async def server_embed_full(
        channel,
        avatar,
        author,
        thumbnail,
        title,
        body,
        image,
        footer,
        timestamp,
        colour
):
    embed = Embed(
        title=title,
        description=f"{body}",
        timestamp=timestamp,
        color=colour
    )

    embed.set_author(name=author, icon_url=avatar)
    embed.set_thumbnail(url=thumbnail)
    embed.set_image(url=image)
    embed.set_footer(text=footer)

    await channel.send(embed=embed)