# GW2DiscordBot
A place for developing a Guild Wars 2 Discord Bot using the [discord.py library](https://github.com/Rapptz/discord.py).

### Things you probably need:
 - **Git** - You can pick it up [here](https://git-scm.com/download/) if you don't have it. You need it to clone the repo.
 - **Python** - You need this to run Python. The link is [here](https://www.python.org).
 - **PIP** - This is the python package manager. This comes along with the Python installation.

### Some nice to haves:
People like using different things to get their local environment set up. Here is some of the stuff we use:
 - **Atom** - This is a lightweight program/text editor with a ton of nice plugins. It was developed by the fine folks here at GitHub. ([Download](https://atom.io/)).
    - **Atom Packages that are nice to have:**
       - **[atom-runner](https://github.com/lsegal/atom-runner)** - Allows you to run python scripts from within Atom.
       - **[atom-beautify](https://atom.io/packages/atom-beautify)** - Allows you to easily make your python code look real pretty.
 - **Scoop** - This is a windows utility that acts like Homebrew. It is a command line installer and  application package manager/repository. You can use it to really easily install python for windows. ([Download](http://scoop.sh/))
 - **Cmder** - This is a really nice windows terminal. Please don't use native Windows cmd. Every time you do, a puppy dies. ([Download](http://cmder.net/))

### Getting started:
Here are some quick, but detailed instructions on how to get the project running locally.
 - First, go to the [Discord Developers Page](https://discordapp.com/developers/docs/intro). This has a ton of good info you might need. Also it has a link to the [Applications Page](https://discordapp.com/developers/applications/me#top). Go there.
 - Make a new App by clicking on the circle with the plus inside.
 - Take your client ID from that page and use it in this URL: ```https://discordapp.com/oauth2/authorize?&client_id=<CLIENT ID>&scope=bot&permissions=0```
 - Get your _token_ from that page and save it for later.
 - Clone this repo to your local machine.
 - From the root of the project:
    - Run `./install/install.bat
    - Run GWBotSetup.py to create the database and tables, as well as loading the tables for future use.
    - Run the main application file with `python GWBotMain.py <bot-token>` where the bot token is for the App you created.
- By default the bots will listen to mentions and commands after `!gw2`.
- To register an api key, you can use "register INSERT_API_KEY_HERE" (it is recommended to pm the bot this information so that it is not visible to everyone).
- To get a list of commands the bot supports, you can use the command "help".

### Commands:
- accountinfo - presents a full list of basic account information.
- bank - retrieves a count of a given item from you bank.
- cats - gets a list of unlocked cats.
- cathint - gets a list of hints for cats that the API provides.
- characters - gets a list of characters for your account.
- coins - gives the rate for a certain amount of coins (in bronze)
- continents - gets a list of continents.
- currencies - gets a list of currencies.
- dailies (usages: "today","tomorrow") - gets a list of daily achievements.
- dailyap - tells the user how many daily AP they can get before maxing out.
- dungeons - gets a list of dungeons.
- dyes - gets a count of dyes unlocked on your account.
- equip (usages: "all" or character name) - gets a list of equipment for a given character or all characters.
- findall - finds a count of a given item across all character, bank, and material storage (will check by partial name as well).
- finishers - gets a count of finishers unlocked on your account.
- fractals - gets a list of fractals.
- gems - gives the rate for a certain amount of gems to gold.
- gliders - gets a count of gliders unlocked on your account.
- hp (usages: "all" or character name) - gets a count of Hero Points for a given character or all characters.
- inventory - searches through all characters for a count of a given item (will check by partial name as well).
- item - retrieves item info for a given item (will check by partial name as well).
- mailcarriers - gets a count of Mail Carriers unlocked on your account.
- mastery - gets a list of mastery points, as well as information for each mastery category.
- materials - searches through material storage for a count of a given item (will check by partial name as well).
- minis - gets a count of minis unlocked on your account.
- name - gets your display name.
- nodes - gets a list of home instance nodes unlocked on your account.
- outfits - gets a list of outfits unlocked on your account.
- permissions - gets a list of permissions associated with the API Key provided.
- professions - gets a list of professions.
- price - gets the price of a given item (will check by partial name as well).
- quaggans - gets a list of quaggans.
- races - gets a list of races.
- raids - gets a list of raids.
- register - registers a given API Key to your Discord ID. 
- recipes - gets a count of recipes unlocked on your account.
- skins - gets a count of skins unlocked on your account.
- titles - gets a list of titles unlocked on your account.
- wallet (usages: "all" or a given currency) - provides a count of all currencies or the currency name provided in your wallet.
- wiki - searches the wiki for a given search string and returns the beginning of the page.
- world - gets the world you are on by name.
- wvw - gets your World vs. World rank.
