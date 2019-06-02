import discord
import sys
import WebUtils
import inspect
import random
import DataBaseUtils
import Strings
from discord.ext import commands
from discord.ext.commands import Bot

"""
This is the main script for the Guild Wars 2 Bot for a discord server.

In order to run this script, simply call this from the command line
with the first argument being your Bot Token from the Discord API.
"""

help_attrs = dict(hidden=True)
bot = Bot(command_prefix=commands.when_mentioned_or(
    '!gw2 '), help_attrs=help_attrs)

emotes = ["(／≧ω＼)", "(´～｀ヾ)", "(๑ÒωÓ๑)", "ﾍ(=^･ω･^= )ﾉ", "(^･ω･^=)~"]

"""
Utility functions
"""


async def fetchGW2Data(ctx, functionName):
    data = DataBaseUtils.selectAllQuery(functionName)
    results = "```Here is the list: \n"
    for item in data:
        results += "ID: " + str(item[0]) + " Description: " + item[1] + "\n"
    results += "```"
    await ctx.channel.send(results)

"""
Bot Events
"""


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_read():
    print("bot logged in")

"""
Bot Commands
"""


@bot.group(pass_context=True)
async def achievements(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getAchievements(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def accountinfo(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getFullAccountInfo(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def bank(ctx, *, message):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getBankCount(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all)


@bot.group(pass_context=True)
async def cats(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getCats(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def cathint(ctx):
    await ctx.message.channel.send( await WebUtils.getCatHints())


@bot.group(pass_context=True)
async def characters(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getCharacters(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def coins(ctx, *, message):
    currencyType = inspect.getframeinfo(inspect.currentframe()).function
    await ctx.message.channel.send( await WebUtils.gw2Exchange(currencyType, message))


@bot.group(pass_context=True)
async def continents(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)


@bot.group(pass_context=True)
async def currencies(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)


@bot.group(pass_context=True)
async def dailies(ctx, *, message):
    if message == "tomorrow":
        dailies = await WebUtils.getDailyAchievements(True)
    elif message == "today":
        dailies = await WebUtils.getDailyAchievements(False)
    else:
        await ctx.message.channel.send( "Invalid message: " + message + " options are today and tomorrow!")
    counter = 0
    results = "```"
    print(dailies)
    for dailies in dailies.split("\n"):
        counter += 1
        results += dailies + "\n"
        if counter >= 30:
            results += "```"
            await ctx.message.channel.send( results)
            results = "```"
            counter = 0
    results += "```"
    await ctx.message.channel.send( results)

@bot.group(pass_context=True)
async def dailyap(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getRemainingAP(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def dungeons(ctx):
    await ctx.message.channel.send( await WebUtils.getDungeons())


@bot.group(pass_context=True)
async def dyes(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getDyeCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def equip(ctx, *, message):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getCharacterEquipment(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def findall(ctx, *, message):
    DiscordID = ctx.message.author.id
    await ctx.message.channel.send( "Please hold on, I need to go through a lot of characters... " + random.choice(emotes))
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getFullItemCount(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def finishers(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getFinisherCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def fractals(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getFractalLevel(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def gems(ctx, *, message):
    currencyType = inspect.getframeinfo(inspect.currentframe()).function
    await ctx.message.channel.send( await WebUtils.gw2Exchange(currencyType, message))


@bot.group(pass_context=True)
async def gliders(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getGliderCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def hp(ctx, *, message):
    DiscordID = ctx.message.author.id
    if message == "all":
        message = None
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getHeroPoints(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def inventory(ctx, *, message):
    DiscordID = ctx.message.author.id
    await ctx.message.channel.send( "Please hold on, I need to go through a lot of characters... " + random.choice(emotes))
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getCharacterInventory(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def item(ctx, *, message):
    await ctx.message.channel.send( await WebUtils.getItemInfoByName(message))


@bot.group(pass_context=True)
async def mailcarriers(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getMailCarrierCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def mastery(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getMasteryCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def materials(ctx, *, message):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getMaterials(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def minis(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getMiniCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def name(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getDisplayName(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def nodes(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getHomeNodes(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def outfits(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getOutfitCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def permissions(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getPermissions(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def professions(ctx):
    await ctx.message.channel.send( await WebUtils.getProfessions())


@bot.group(pass_context=True)
async def price(ctx, *, message):
    await ctx.message.channel.send( await WebUtils.getItemPrice(message))


@bot.group(pass_context=True)
async def quaggans(ctx):
    quaggans = await WebUtils.getQuaggans()
    counter = 0
    results = "```"
    for quaggan in quaggans.split("\n"):
        counter += 1
        results += quaggan + "\n"
        if counter >= 30:
            results += "```"
            await ctx.message.channel.send( results)
            results = "```"
            counter = 0


@bot.group(pass_context=True)
async def races(ctx):
    await ctx.message.channel.send( await WebUtils.getRaces())


@bot.group(pass_context=True)
async def raids(ctx):
    await ctx.message.channel.send( await WebUtils.getRaids())


@bot.group(pass_context=True)
async def register(ctx, *, message):
    DiscordID = ctx.message.author.id
    permissions = await WebUtils.hasPermissions(message)
    print(permissions)
    if permissions:
        DataBaseUtils.registerAPIKey(
            DiscordID, ctx.message.author.display_name, message)
        await ctx.message.channel.send( "API Key Registered!")
    else:
        await ctx.message.channel.send( Strings.all["bad_api_key"])


@bot.group(pass_context=True)
async def recipes(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getRecipeCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def skins(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getSkinCount(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])

"""
Gets a list of titles. This needs to be chunked, as the results are too large
to send at once and causes a generic HTTP Exception from the Discord Library.
"""


@bot.group(pass_context=True)
async def titles(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        titles = await WebUtils.getTitles(DiscordID)
        counter = 0
        results = "```"
        for title in titles.split("\n"):
            counter += 1
            results += title + "\n"
            if counter >= 30:
                results += "```"
                await ctx.message.channel.send( results)
                results = "```"
                counter = 0
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def wallet(ctx, *, message):
    DiscordID = ctx.message.author.id
    if message == "all":
        message = None
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getWallet(DiscordID, message))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.command(pass_context=True)
async def wiki(ctx, *, message):
    await ctx.message.channel.send( await WebUtils.getGWWikiHTML(message))


@bot.group(pass_context=True)
async def world(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getWorld(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])


@bot.group(pass_context=True)
async def wvw(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await ctx.message.channel.send( await WebUtils.getWVWRank(DiscordID))
    else:
        await ctx.message.channel.send( Strings.all["no_api_key"])

"""
Init script
"""
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        bot_token = sys.argv[1]
        bot.run(sys.argv[1])
    else:
        print("A bot token was not provided, the script will now end!!!")
