import requests
import bs4
import json
import DataBaseUtils
import aiohttp
import Strings
from collections import defaultdict

gw2_api_url = "https://api.guildwars2.com/v2/"
gw2_wiki_url = "https://wiki.guildwars2.com/wiki/"
maxItems = 30

"""
This is a simple decorator to wrap a result in "```" characters to nicely
format text when sending back a message from the bot.
"""


def make_pretty(func):
    async def func_wrapper(*args, **kwargs):
        return "```{0}```".format(await func(*args, **kwargs))
    return func_wrapper


"""
Utility Functions
"""


async def getJSON(url):
    async with aiohttp.ClientSession().get(url) as r:
        if r.status == 200:
            js = await r.json()
            return js
"""
This is a generic helper method that can be used to get the response from a URL
as a soup object.
"""


def getSoup(url):
    try:
        print('Downloading page %s...' % url)
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None
    except requests.exceptions.ConnectionError as err:
        return (url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup


"""
Guild Wars 2 Wiki-specific functions
"""

"""
This function returns the first two paragraphs of the given wiki article.
"""


@make_pretty
async def getGWWikiHTML(query):
    result = getSoup(gw2_wiki_url + query.replace(" ", "_"))
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText() + "\n" + result.select("p")[1].getText()

"""
Guild Wars 2 API-specific functions
"""


def getAccessToken(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    AccessToken = "?access_token=" + APIKey
    return AccessToken


async def getAccountData(DiscordID):
    result = await getJSON(gw2_api_url + "account" + getAccessToken(DiscordID))
    return result


@make_pretty
async def getAchievements(DiscordID):
    acJSON = await getJSON(gw2_api_url + "account/achievements/" + getAccessToken(DiscordID))
    counter = 0
    for achievement in acJSON:
        if achievement.get('done'):
            counter += 1
    results = "You have: " + str(counter) + " achievements on your account."
    return results

# TODO figure out how to better refactor this...


@make_pretty
async def getBankCount(DiscordID, name):
    data = DataBaseUtils.findItemByName(name)
    if(len(data) > maxItems):
        return Strings.all["too_many_items"].format(str(len(data)), str(maxItems))
    elif(len(data) < 1):
        return Strings.all["no_results"]
    itemDict = {}
    for item in data:
        itemDict[item[0]] = (item[1], 0)
    url = gw2_api_url + "account/bank" + getAccessToken(DiscordID)
    bankItems = await getJSON(url)
    for item in bankItems:
        if item is None:
            continue
        itemID = item.get('id')
        if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0], old_value[1] + item.get('count')
            itemDict[itemID] = new_value
    results = "Here is a list of how many of each item you have in your bank... \n"
    for item in itemDict:
        value = itemDict[item]
        results += "ItemID: " + str(item) + "\n"
        results += "ItemDescription: " + value[0] + "\n"
        results += "ItemCount: " + str(value[1]) + "\n\n"
    return results


@make_pretty
async def getCats(DiscordID):
    results = "Here is a list of your cats: \n"
    catJSON = await getJSON(gw2_api_url + "account/home/cats" + getAccessToken(DiscordID))
    for cat in catJSON:
        results += "catID: " + str(cat.get('id')) + \
            " catName: " + cat.get('hint') + "\n"
    return results


@make_pretty
async def getCatHints():
    results = "Here is a list of cat hints: \n"
    catJSON = await getJSON(gw2_api_url + "cats?ids=all")
    for cat in catJSON:
        results += "catID: " + str(cat.get('id')) + \
            " catHint: " + cat.get('hint') + "\n"
    return results


# TODO Refactor this with getCharacters

@make_pretty
async def getCharacterInventory(DiscordID, ItemName):
    data = DataBaseUtils.findItemByName(ItemName)
    if(len(data) > maxItems):
        return Strings.all["too_many_items"].format(str(len(data)), str(maxItems))
    elif(len(data) < 1):
        return Strings.all["no_results"]
    itemDict = {}
    for item in data:
        itemDict[item[0]] = (item[1], 0)

    characterJSON = await getJSON(gw2_api_url + "characters" + getAccessToken(DiscordID))
    for character in characterJSON:
        characterInv = await getJSON(gw2_api_url + "characters/" + character + "/inventory" + getAccessToken(DiscordID))
        for bag in characterInv.get('bags'):
            if bag is None:
                continue
            for item in bag.get('inventory'):
                if item is None:
                    continue
                itemID = item.get('id')
                if itemID in itemDict:
                    print(str(itemDict))
                    old_value = itemDict[itemID]
                    new_value = old_value[0], old_value[1] + item.get('count')
                    itemDict[itemID] = new_value
    results = "Here is a list of how many of each item you have in your character inventories... \n"
    for item in itemDict:
        value = itemDict[item]
        results += "ItemID: " + str(item) + "\n"
        results += "ItemDescription: " + value[0] + "\n"
        results += "ItemCount: " + str(value[1]) + "\n\n"
    return results


@make_pretty
async def getCharacterEquipment(DiscordID, charname):
    CharacterEquipment = {}
    characterEqJSON = await getJSON(gw2_api_url + "characters/" + charname + "/equipment" + getAccessToken(DiscordID))
    if characterEqJSON is not None:
        CharacterEquipment[charname] = characterEqJSON
    else:
        return "Could not find the character: " + charname + "... Did you get the name wrong?"
    for character in CharacterEquipment:
        results = "Here is a list of equipment for " + character + ":\n\n"
        equipJSON = CharacterEquipment[character]
        for equipment in equipJSON.get('equipment'):
            results += equipment.get('slot') + ": "
            results += DataBaseUtils.findItemNameByID(
                str(equipment.get('id')))[0]
            results += "\n"
    return results


@make_pretty
async def getCharacters(DiscordID):
    results = "Here is a list of your characters: \n"
    characterJSON = await getJSON(gw2_api_url + "characters" + getAccessToken(DiscordID))
    for character in characterJSON:
        results += character + "\n"
    return results


async def getDailyAchievements(tomorrow):
    dailyURL = gw2_api_url + "achievements/daily"
    if(tomorrow):
        dailyURL += "/tomorrow"
    dailyJSON = await getJSON(dailyURL)
    result = "Here are the dailies: \n"
    for gameType in dailyJSON:
        result += gameType + ":\n"
        for daily in dailyJSON.get(gameType):
            dailyNameJSON = await getJSON(gw2_api_url + "achievements?id=" + str(daily.get('id')))
            result += "Achievement ID: " + \
                str(daily.get('id')) + " Achievement Name: " + \
                dailyNameJSON.get('name') + "\n"
        result += "\n"
    return result


@make_pretty
async def getDisplayName(DiscordID):
    nameJSON = await getAccountData(DiscordID)
    result = "Your account name is: " + nameJSON.get('name')
    return result


@make_pretty
async def getDungeons():
    results = Strings.all["list"].format("dungeons") + " \n"
    dungeonJSON = await getJSON(gw2_api_url + "dungeons")
    for dungeon in dungeonJSON:
        results += dungeon + "\n"
    return results


@make_pretty
async def getDyeCount(DiscordID):
    dyeJSON = await getJSON(gw2_api_url + "account/dyes" + getAccessToken(DiscordID))
    totalDyeJSON = await getJSON(gw2_api_url + "colors")
    results = Strings.all["count_with_total"].format(
        str(len(dyeJSON)), "dye", str(len(totalDyeJSON)))
    return results


@make_pretty
async def getFinisherCount(DiscordID):
    finisherJSON = await getJSON(gw2_api_url + "account/finishers" + getAccessToken(DiscordID))
    finisherCount = 0
    for finisher in finisherJSON:
        if finisher.get('permanent'):
            finisherCount += 1
    totalFinisherJSON = await getJSON(gw2_api_url + "finishers")
    results = Strings.all["count_with_total"].format(
        str(finisherCount), "permanent finisher", str(len(totalFinisherJSON)))
    return results


@make_pretty
async def getFractalLevel(DiscordID):
    accountJSON = await getAccountData(DiscordID)
    result = "Your Fractal Level is: " + str(accountJSON.get('fractal_level'))
    return result


@make_pretty
async def getFullAccountInfo(DiscordID):
    accountJSON = await getAccountData(DiscordID)
    result = "Here is all of your account information: \n"
    for k, v in accountJSON.items():
        result += k + ": " + str(v) + "\n"
    return result


@make_pretty
async def getFullItemCount(DiscordID, ItemName):
    data = DataBaseUtils.findItemByName(ItemName)
    if(len(data) > maxItems):
        return Strings.all["too_many_items"].format(str(len(data)), str(maxItems))
    elif(len(data) < 1):
        return Strings.all["no_results"]
    itemDict = {}
    for item in data:
        itemDict[item[0]] = (item[1], 0)

    # Bank
    bank_url = gw2_api_url + "account/bank" + getAccessToken(DiscordID)
    bankItems = await getJSON(bank_url)
    for item in bankItems:
        if item is None:
            continue
        itemID = item.get('id')
        if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0], old_value[1] + item.get('count')
            itemDict[itemID] = new_value
    # Character Inventory
    characterJSON = await getJSON(gw2_api_url + "characters" + getAccessToken(DiscordID))
    for character in characterJSON:
        characterInv = await getJSON(gw2_api_url + "characters/" + character + "/inventory" + getAccessToken(DiscordID))
        for bag in characterInv.get('bags'):
            if bag is None:
                continue
            for item in bag.get('inventory'):
                if item is None:
                    continue
                itemID = item.get('id')
                if itemID in itemDict:
                    old_value = itemDict[itemID]
                    new_value = old_value[0], old_value[1] + item.get('count')
                    itemDict[itemID] = new_value
    # Materials
    materialsJSON = await getJSON(gw2_api_url + "account/materials" + getAccessToken(DiscordID))
    for item in materialsJSON:
        if item is None:
            continue
        itemID = item.get('id')
        if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0], old_value[1] + item.get('count')
            itemDict[itemID] = new_value
    results = "Here is a list of how many of each item you have throughout your entire account... \n"
    for item in itemDict:
        value = itemDict[item]
        results += "ItemID: " + str(item) + "\n"
        results += "ItemDescription: " + value[0] + "\n"
        results += "ItemCount: " + str(value[1]) + "\n\n"
    return results


@make_pretty
async def getGliderCount(DiscordID):
    gliderJSON = await getJSON(gw2_api_url + "account/gliders" + getAccessToken(DiscordID))
    totalGliderJSON = await getJSON(gw2_api_url + "gliders")
    results = Strings.all["count_with_total"].format(
        str(len(gliderJSON)), "glider", str(len(totalGliderJSON)))
    return results


@make_pretty
async def getHeroPoints(DiscordID, charname):
    HeroPointDict = {}
    if charname is None:
        characterJSON = await getJSON(gw2_api_url + "characters" + getAccessToken(DiscordID))
        for character in characterJSON:
            characterHP = await getJSON(gw2_api_url + "characters/" + character + "/heropoints" + getAccessToken(DiscordID))
            HeroPointDict[character] = len(characterHP)
            results = "Here is a list of how many of Hero Points you have on each character... \n"
    else:
        characterJSON = await getJSON(gw2_api_url + "characters/" + charname + "/heropoints" + getAccessToken(DiscordID))
        if characterJSON is not None:
            HeroPointDict[charname] = len(characterJSON)
            results = "Here are how many Hero Points you have on " + charname + "... \n"
        else:
            return "Could not find the character: " + charname + "... Did you get the name wrong?"

    for character in HeroPointDict:
        value = HeroPointDict[character]
        results += "Character: " + str(character) + "\n"
        results += "Hero Points: " + str(value) + "\n\n"
    return results


@make_pretty
async def getHomeNodes(DiscordID):
    homeNodeJSON = await getJSON(gw2_api_url + "account/home/nodes" + getAccessToken(DiscordID))
    totalNodeJSON = await getJSON(gw2_api_url + "nodes")
    results = "Here are a list of nodes you have in your home: "
    for node in homeNodeJSON:
        results += node + "\n"
    results += "\n" + Strings.all["count_with_total"].format(
        str(len(homeNodeJSON)), "nodes", str(len(totalNodeJSON)))
    return results


@make_pretty
async def getItemInfoByName(name):
    data = DataBaseUtils.findItemByName(name)
    if(len(data) > maxItems):
        return Strings.all["too_many_items"].format(str(len(data)), str(maxItems))
    elif(len(data) < 1):
        return Strings.all["no_results"]
    results = ""
    for item in data:
        key = str(item[0])
        # url = gw2_api_url + "items?id=" + key
        # itemPicture = json.loads(getJSON(url).text).get('icon')
        results += key + ": " + item[1] + "\n"
    return results


@make_pretty
async def getItemPrice(name):
    data = DataBaseUtils.findItemByName(name)

    if(len(data) > maxItems):
        return Strings.all["too_many_items"].format(str(len(data)), str(maxItems))
    elif(len(data) < 1):
        return Strings.all["no_results"]
    results = ""
    for item in data:
        key = str(item[0])
        url = gw2_api_url + "commerce/prices?id=" + key
        itemJSON = await getJSON(url)
        if itemJSON == None:
            results += "Could not find on the Trading Post! This item is probably untradeable... \n\n"
        else:
            results += "Item ID: " + key + "\n"
            results += "Item Description: " + item[1] + "\n"
            results += "Buy price: " + \
                str(itemJSON.get('buys').get('unit_price') / 10000) + " gold \n"
            results += "Sell price: " + \
                str(itemJSON.get('sells').get(
                    'unit_price') / 10000) + " gold \n\n"
    return results


@make_pretty
async def getMailCarrierCount(DiscordID):
    mailCarrierJSON = await getJSON(gw2_api_url + "account/mailcarriers" + getAccessToken(DiscordID))
    totalMailCarrierJSON = await getJSON(gw2_api_url + "mailcarriers")
    results = Strings.all["count_with_total"].format(
        str(len(mailCarrierJSON)), "mail carrier", str(len(totalMailCarrierJSON)))
    return results


@make_pretty
async def getMasteryCount(DiscordID):
    masteryJSON = await getJSON(gw2_api_url + "account/mastery/points" + getAccessToken(DiscordID))
    results = "You have the following mastery point counts: \n\n"
    for mastery in masteryJSON.get('totals'):
        results += "Region: " + mastery.get('region') + "\n"
        results += "Spent: " + str(mastery.get('spent')) + \
            " Earned: " + str(mastery.get('earned')) + "\n\n"
    results += "Individual Masteries: \n\n"
    individualMasteryJSON = await getJSON(gw2_api_url + "account/masteries" + getAccessToken(DiscordID))
    masteryDescJSON = await getJSON(gw2_api_url + "masteries?ids=all")
    individualMasteryDict = {}
    for mastery in individualMasteryJSON:
        individualMasteryDict[str(mastery.get('id'))] = str(
            mastery.get('level'))
    for mastery in masteryDescJSON:
        masteryID = str(mastery.get('id'))
        if(masteryID in individualMasteryDict):
            results += "Mastery ID: " + masteryID + " name: " + \
                mastery.get('name') + " level: " + \
                individualMasteryDict[masteryID]
            # Apparently, mastery levels start at 0 in the API...
            if len(mastery.get('levels')) <= (int(individualMasteryDict[masteryID]) + 1):
                results += " (max)"
            results += "\n"
    return results


@make_pretty
async def getMaterials(DiscordID, ItemName):
    data = DataBaseUtils.findItemByName(ItemName)
    if(len(data) > maxItems):
        return Strings.all["too_many_items"].format(str(len(data)), str(maxItems))
    elif(len(data) < 1):
        return Strings.all["no_results"]
    itemDict = {}
    for item in data:
        itemDict[item[0]] = (item[1], 0)
    itemJSON = await getJSON(gw2_api_url + "account/materials" + getAccessToken(DiscordID))
    for item in itemJSON:
        if item is None:
            continue
        itemID = item.get('id')
        if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0], old_value[1] + item.get('count')
            itemDict[itemID] = new_value

    results = "Here is a list of how many of each item you have in your material storage... \n"
    for item in itemDict:
        value = itemDict[item]
        results += "ItemID: " + str(item) + "\n"
        results += "ItemDescription: " + value[0] + "\n"
        results += "ItemCount: " + str(value[1]) + "\n\n"
    return results


@make_pretty
async def getMiniCount(DiscordID):
    miniJSON = await getJSON(gw2_api_url + "account/minis" + getAccessToken(DiscordID))
    miniTotalJSON = await getJSON(gw2_api_url + "minis")
    results = Strings.all["count_with_total"].format(
        str(len(miniJSON)), "mini", str(len(miniTotalJSON)))
    return results


@make_pretty
async def getOutfitCount(DiscordID):
    outfitJSON = await getJSON(gw2_api_url + "account/outfits" + getAccessToken(DiscordID))
    outfitTotalJSON = await getJSON(gw2_api_url + "outfits")
    results = Strings.all["count_with_total"].format(
        str(len(outfitJSON)), "outfit", str(len(outfitTotalJSON)))
    return results


@make_pretty
async def getPermissions(DiscordID):
    tokenInfoJSON = await getJSON(gw2_api_url + "tokeninfo" + getAccessToken(DiscordID))
    print(tokenInfoJSON)
    result = "Here are the permissions associated with your API Key: \n"
    if 'permissions' not in tokenInfoJSON:
        return Strings.all["bad_api_key"]
    for permission in tokenInfoJSON.get('permissions'):
        result += permission + "\n"
    return result


@make_pretty
async def getProfessions():
    results = Strings.all["list"].format("professions") + " \n"
    profJSON = await getJSON(gw2_api_url + "professions")
    for prof in profJSON:
        results += prof + "\n"
    return results


async def getQuaggans():
    quagganJSON = await getJSON(gw2_api_url + "quaggans?ids=all")
    results = "Here are all the different Quaggan pictures: \n"
    for quaggan in quagganJSON:
        results += "ID: " + quaggan.get('id') + \
            " url: " + quaggan.get('url') + "\n"
    return results


@make_pretty
async def getRaces():
    results = Strings.all["list"].format("races") + " \n"
    raceJSON = await getJSON(gw2_api_url + "races")
    for race in raceJSON:
        results += race + "\n"
    return results


@make_pretty
async def getRaids():
    results = "Here is a list of raids and their bosses: \n"
    raidJSON = await getJSON(gw2_api_url + "raids?ids=all")
    for raid in raidJSON:
        results += "Raid Name: " + raid.get('id') + "\n\n"
        for wing in raid.get('wings'):
            results += "Wing Name: " + wing.get('id') + "\n"
            for event in wing.get('events'):
                if event.get('type') == "Boss":
                    results += "Boss: " + event.get('id') + "\n"
            results += "\n"
    return results


@make_pretty
async def getRemainingAP(DiscordID):
    accountJSON = await getAccountData(DiscordID)
    result = 15000 - (int(accountJSON.get('daily_ap')) +
                      int(accountJSON.get('monthly_ap')))
    if(result > 0):
        text = "You have " + str(result) + " remaining. Only " + \
            str(result / 10) + " more days before the nightmare ends!"
    else:
        text = "YOU ARE FREE FROM THE NIGHTMARE"
    return text


@make_pretty
async def getRecipeCount(DiscordID):
    recipeJSON = await getJSON(gw2_api_url + "account/recipes" + getAccessToken(DiscordID))
    totalRecipeJSON = await getJSON(gw2_api_url + "recipes")
    results = Strings.all["count_with_total"].format(
        str(len(recipeJSON)), "recipe", str(len(totalRecipeJSON)))
    return results


@make_pretty
async def getSkinCount(DiscordID):
    skinJSON = await getJSON(gw2_api_url + "account/skins" + getAccessToken(DiscordID))
    totalSkinJSON = await getJSON(gw2_api_url + "skins")
    results = Strings.all["count_with_total"].format(
        str(len(skinJSON)), "skin", str(len(totalSkinJSON)))
    return results


async def getTitles(DiscordID):
    titles = await getJSON(gw2_api_url + "account/titles" + getAccessToken(DiscordID))
    titleDescriptions = await getJSON(gw2_api_url + "titles?ids=all")
    titleDict = {}
    for description in titleDescriptions:
        if description.get('id') in titles:
            titleDict[description.get('id')] = description.get('name')
    results = "Here are a list of your titles: \n"
    for title, description in titleDict.items():
        results += "TitleID: " + str(title) + \
            " Title Desc: " + description + "\n"
    return results


@make_pretty
async def getWallet(DiscordID, currencyName):
    if currencyName is not None:
        data = DataBaseUtils.findCurrencyByName(currencyName)
        if(len(data) < 1):
            return Strings.all["no_results"]
    else:
        data = DataBaseUtils.selectAllQuery("currencies")
    itemDict = {}
    for item in data:
        itemDict[item[0]] = (item[1], 0)
    itemJSON = await getJSON(gw2_api_url + "account/wallet" + getAccessToken(DiscordID))
    for item in itemJSON:
        if item is None:
            continue
        itemID = item.get('id')
        if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0], old_value[1] + item.get('value')
            itemDict[itemID] = new_value
    results = "Here are the amounts of your requested currencies... \n"
    for item in itemDict:
        value = itemDict[item]
        results += "ItemID: " + str(item) + "\n"
        results += "ItemDescription: " + value[0] + "\n"
        results += "ItemCount: " + str(value[1]) + "\n\n"
    return results


@make_pretty
async def getWorld(DiscordID):
    world = await getAccountData(DiscordID)
    worldJSON = await getJSON(gw2_api_url + "worlds?id=" + str(world.get('world')))
    result = "Your world is: " + worldJSON.get('name')
    return result


@make_pretty
async def getWVWRank(DiscordID):
    accountJSON = await getAccountData(DiscordID)
    result = "Your WVW Rank is: " + str(accountJSON.get('wvw_rank'))
    return result


@make_pretty
async def gw2Exchange(currencyType, quantity):
    currencyJSON = await getJSON(gw2_api_url + 'commerce/exchange/' + currencyType + '?quantity=' + quantity)
    if currencyType == 'gems':
        results = Strings.all["exchange"].format("coins", quantity, "gems", str(currencyJSON.get(
            'coins_per_gem') / 10000), str(currencyJSON.get('quantity') / 10000), "gold")
    else:
        results = Strings.all["exchange"].format("gems", quantity, "coins", str(currencyJSON.get(
            'coins_per_gem') / 10000), str(currencyJSON.get('quantity') / 10000), "gems")
    return results


async def hasPermissions(APIKey):
    tokenInfoJSON = await getJSON(gw2_api_url + "tokeninfo?access_token=" + APIKey)
    print(tokenInfoJSON)
    if tokenInfoJSON is None:
        return False
    elif 'permissions' not in tokenInfoJSON:
        return False
    else:
        return True
