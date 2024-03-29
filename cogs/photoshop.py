import aiohttp
import discord
from bs4 import BeautifulSoup as soup
from discord.ext import commands
from random import randint
from settings import unsplash_client_id


class Photoshop(commands.Cog):
    """What could be better than Photoshop? Photoshop commands!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def search(self, ctx, query: str):
        """Gives you page links for a Photoshop query via adobe.io."""

        headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.159 Safari/537.36",
            "x-api-key": "helpxcomprod",
            "content-type": "application/vnd.adobe.search-request+json",
            "Accept": "*/*",
            "Origin": "https://helpx.adobe.com",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://helpx.adobe.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }

        data = (
            "{"
            '"scope":["helpx"],'
            '"subscope":[],'
            '"serp_content_type":["help"],'
            f'"q":"{query}",'
            '"limit":5,'
            '"locale":"en_us",'
            '"start_index":0,'
            '"sort_orderby":"relevancy",'
            '"sort_order":"desc",'
            '"facets_fields":["applicable_products"],'
            '"post_facet_filters":{"applicable_products":["Adobe Photoshop"]},'
            '"enable_spelling_correction":true,'
            '"request_region":"SE"'
            "}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://adobesearch-uss-enterprise.adobe.io/universal-search-enterprise/search",
                    headers=headers,
                    data=data,
            ) as response:
                dumped = await response.json()

        # List of all the relevant result items
        if dumped["metrics"]["total_hits"] == 0:
            return await ctx.send("Couldn't find anything. Sorry.")

        results = dumped["result_sets"][0]["items"]

        description = ""

        for count, result in enumerate(results):
            if count == 5:
                break

            description = (
                f"{description}\n"
                f'[{result["asset_name"]}]'
                f'({(result["_links"])["source"]["href"]} '
                f'"{result["excerpt"]}")'
            )

        embed = discord.Embed.from_dict(
            {
                "title": f"Search",
                "description": f"{description}",
                "color": discord.Color.og_blurple().value,
            }
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def poster(self, ctx):
        """Displays a vintage movie poster from jozefsquare.com."""

        def fetch(html_data):
            parsed = soup(html_data, "lxml")
            return parsed

        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'https://www.jozefsquare.com/shop/poster-shop/vintage-movie-posters/page/{randint(1, 90)}') as response:
                    html = await response.text()
                    parsed = await self.bot.loop.run_in_executor(None, fetch, html)

                    results = parsed.find_all("img", class_="attachment-woocommerce_thumbnail")
                    result = results[randint(0, len(results) - 1)]

        await ctx.send(result["alt"])
        await ctx.send(result["src"])

    @commands.command()
    @commands.guild_only()
    async def unsplash(self, ctx):
        """Gets an image from Unsplash. Heavily rated limited."""

        headers = {'Authorization': f'Client-ID {unsplash_client_id}'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.unsplash.com/photos/random', headers=headers) as response:
                r = await response.json()

        embed = discord.Embed.from_dict({'title': f"Unsplash",
                                         'image': {'url': r['urls']['full']},
                                         'color': discord.Color.og_blurple().value
                                         })

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Photoshop(bot))
