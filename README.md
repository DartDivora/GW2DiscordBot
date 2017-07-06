# GW2DiscordBot
A place for developing a Guild Wars 2 Discord Bot using the [discord.py library](https://github.com/Rapptz/discord.py).

### Things you probably need:
 - **Git** - You can pick it up [here](https://git-scm.com/download/) if you don't have it. You need it to clone the repo.
 - **Python** - This allows you to run python scripts locally. Installing this is different depending on your host OS. Use google.
 - **PIP** - This is the python package manager. It pulls in the junk that other folks wrote that our awesome project needs.

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
