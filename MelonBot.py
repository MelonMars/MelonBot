from io import DEFAULT_BUFFER_SIZE
from typing import Annotated
from discord.ext import commands
import wikipedia, requests, random, json
from bs4 import BeautifulSoup as bs
from mtgsdk import Card
from discord import Color as c
from discord import Embed, Game, Member
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option


bot = commands.Bot(command_prefix=';')
bot.remove_command("help")

def coolWikis():
    res = requests.get("https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles")
    soup = bs(res.text, "html.parser")
    wikisList = []
    global badList
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if "/wiki/" in url:
            wikisList.append(url)

    toSend = wikisList[random.randint(0, len(wikisList))]
    if toSend.contains('porn') or toSend.contains('sex') or toSend.contains('Fuck') or toSend.contains('swastika'):
        toSend = "Sorry, but the article the random number generator landed on... is not the most appropriate."
    return toSend

def usernameToUUID(uname):
    res = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uname}")
    return(res.text)

def getHypixelStats(uuid):
    res = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(hypixelKey, uuid))
    return res.json()

@bot.event
async def on_ready():
    print('------')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=Game(name=";help"))
    print('Custom Status is working')
    print('------')


@bot.command()
async def wiki(ctx, *page: str):
    try:
        data = wikipedia.WikipediaPage(title = page).summary
    except Exception as e:
        data = str(e)
    data = data[0:2000]
    await ctx.channel.send(data)

@bot.command()
async def dadjoke(ctx):
    res = requests.get("https://www.icanhazdadjoke.com/slack")
    await ctx.channel.send(res.json()["attachments"][0]["fallback"])

@bot.command()
async def nasa(ctx):
        year = random.randint(1996, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 29)
        date = "{}-{}-{}".format(year, month, day)
        r = requests.get("https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(nasaKey, date))
        data2 = r.json()
        result = "\n{}: \n{}. \nThe image is found here: \n{}".format(data2["title"], data2["explanation"], data2["url"])
        await ctx.channel.send(result)

@bot.command()
async def id(ctx):
    await ctx.channel.send(f"Your user id is: {ctx.author.id}")

@bot.command()
async def programmingjoke(ctx):
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    res = requests.get(url)
    data = dict(res.json()[0])
    await ctx.channel.send(data["setup"]+data["punchline"])

@bot.command()
async def generaljoke(ctx):
        url = "https://official-joke-api.appspot.com/jokes/general/random"
        res = requests.get(url)
        data = dict(res.json()[0])
        await ctx.channel.send(data["setup"]+data["punchline"])

@bot.command()
async def shibu(ctx):
    url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true"
    res = requests.get(url)
    await ctx.channel.send(res.json()[0])

@bot.command()
async def fox(ctx):
    url = "https://randomfox.ca/floof/"
    res = requests.get(url)
    await ctx.channel.send(res.json()["image"])

@bot.command()
async def cat(ctx):
    url = "https://randomfox.ca/floof/"
    res = requests.get(url)
    await ctx.channel.send(res.json()["image"])

@bot.command()
async def food(ctx): 
        url = "https://foodish-api.herokuapp.com/api"
        res = requests.get(url)
        await ctx.channel.send(res.json()["image"])

@bot.command()
async def author(ctx, *author: str):
        #https://openlibrary.org/search/authors.json?q=
        msglist = str(author).split(' ')
        msglist = msglist[1:]
        upname = str(msglist).replace(']', '').replace('[', '').replace(' ', '%20').replace(',', '').replace('\'', '')
        res = requests.get(f"https://openlibrary.org/search/authors.json?q={upname}")
        data = res.json()["docs"]
        data = list(data)[0]
        data = dict(data)
       # await message.channel.send(data["name"])
        em= Embed(title=data["name"], color=c.red())
        em.add_field(name="Birth", value=data["birth_date"], inline=True)
        em.add_field(name="Death", value=data["death_date"], inline=True)
        em.add_field(name="Top Work", value=data["top_work"], inline=True)
        await ctx.channel.send(embed=em)

@bot.command()
async def freegame(ctx):
    id = random.randint(1, 512)
    res = requests.get(f"https://www.freetogame.com/api/game?id={id}")
    data = res.json()
    em = discord.Embed(title=data["title"], url=data["game_url"], description=data["short_description"], )
    em.add_field(name="Publisher", value=data["publisher"], inline=True)
    em.add_field(name="Developer", value=data["developer"], inline=True)
    em.add_field(name="Platform", value=data["platform"], inline=True)
    em.add_field(name="genre", value=data["genre"], inline=True)
    em.set_thumbnail(url="https://www.freetogame.com/g/427/thumbnail.jpg")
    await ctx.channel.send(embed=em)

@bot.command()
async def tronalddump(ctx):
    url = "https://www.tronalddump.io/random/quote"
    res = requests.get(url)
    await ctx.channel.send("A stupid Trump quote is:" + " " + res.json()["value"])

@bot.command()
async def insult(ctx):
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    res = requests.get(url)
    await ctx.channel.send(ctx.author.mention + "," + " " + res.json()["insult"])

@bot.command()
async def quote(ctx):
    url = "https://api.quotable.io/random"
    res = requests.get(url)
    await ctx.channel.send(res.json()["content"] + '\n' + '-' + res.json()["author"])

@bot.command()
async def advice(ctx):
    url = "https://api.adviceslip.com/advice"
    res = requests.get(url)
    await ctx.channel.send(res.json()["slip"]["advice"])

@bot.command()
async def coolwikis(ctx):
    x = coolWikis()
    await ctx.channel.send("https://en.wikipedia.org/"+x)

@bot.command()
async def bedwars(ctx, uname: str):
    if uname=="MelonsMars":
        try:
                uuid = usernameToUUID(uname)
                uuid = json.loads(uuid)
                uuid = uuid["id"]
        except:
            pass
        statsRaw = getHypixelStats(uuid)
        try:
            playerKills = statsRaw["player"]["stats"]["Bedwars"]["kills_bedwars"]
            playerGames = statsRaw["player"]["stats"]["Bedwars"]["games_played_bedwars_1"]
            playerDeaths = statsRaw["player"]["stats"]["Bedwars"]["deaths_bedwars"]
            playerWins = statsRaw["player"]["stats"]["Bedwars"]["wins_bedwars"]
            playerLosses = int(playerGames) - int(playerWins)
            kd = playerKills/playerDeaths
            wnlRatio = playerWins/playerLosses
        
            await ctx.channel.send("{} has {} kills, and {} deaths, which makes a total k/d ratio of {}. They have won {} times, and lost {} times, for a win/loss ratio of {}.".format(uname, playerKills, playerDeaths, kd, playerWins, playerLosses, wnlRatio))
        except Exception as e:
            await ctx.channel.send("That is not a valid username")
            print(e)
    await ctx.channel.send("MelonsMars has 30000 kills, and 300 deaths, which makes a total k/d ratio of 100. They have won 5000 times, and lost 50 times, for a win/loss ratio of 100")
@bot.command()
async def skywars(ctx, uname: str):
    try:
            uuid = usernameToUUID(uname)
            uuid = json.loads(uuid)
            uuid = uuid["id"]
    except:
        uuid = "none"
    
    statsRaw = getHypixelStats(uuid)
    try:
        playerWins = statsRaw["player"]["stats"]["SkyWars"]["wins"]
        playerGames = statsRaw["player"]["stats"]["SkyWars"]["games_played_skywars"]
        playerKills = statsRaw["player"]["stats"]["SkyWars"]["kills"]
        playerDeaths = playerGames - playerWins
        kd = playerKills/playerDeaths
        wnlRatio = playerWins/playerDeaths
        await ctx.channel.send("{} has {} kills, {} losses, for a k/d of {}, and has {} wins and {} losses, for a wnl ratio of {}".format(uname, playerKills, playerDeaths, kd, playerWins, playerDeaths, wnlRatio))
    except:
        await ctx.channel.send("That is not a valid username")

@bot.command()
async def magic(ctx):
        running = True
        while running == True:
            try:
                card = Card.find(random.randint(1, 99999))
                cardType = card.type
                cardType = cardType.split(" ")
                if cardType[0] == "Creature":
                    result = "\nThe card {} costs {} with a power / toughness ratio of {} / {} \n{}".format(card.name, card.mana_cost, card.power, card.toughness, card.text)
                else:
                    result = "\nThe card {} costs {} \n{}".format(card.name, card.mana_cost, card.text)
                running = False
            except:
                pass
        await ctx.channel.send(result)

@bot.command()
async def e(ctx, n: int):
    #(1 + 1/n)^n
    beforeMultiply = 1 + 1/int(n)
    afterMultiply = beforeMultiply**float(n)
    await ctx.channel.send(afterMultiply)

@bot.command()
async def affirmation(ctx):
    res = requests.get("https://www.affirmations.dev/")
    await ctx.channel.send(res.json()["affirmation"])

@bot.command()
async def randomnumber(ctx):
    res = requests.get("http://numbersapi.com/random")
    await ctx.channel.send(res.text)

@bot.command()
async def number(ctx, n: int):
    res = requests.get(f"http://numbersapi.com/{n}")
    await ctx.channel.send(res.text)

@bot.command()
async def iss(ctx):
    res = requests.get("http://api.open-notify.org/iss-now.json")
    long = res.json()["iss_position"]["longitude"]
    lat = res.json()["iss_position"]["latitude"]
    await ctx.channel.send(f"Lat: {lat} \nLong: {long}")

@bot.command()
async def help(ctx, type=''):
    if type == '':
        em = Embed(title="Melon Bot Help", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="📓wikipedia", value="`;help wikipedia`", inline=True)
        em.add_field(name="😃miscellaneous", value="`;help misc`", inline=True)
        em.add_field(name="🎮games", value="`;help games`", inline=True)
        em.add_field(name="🐻animals", value="`;help animals`", inline=True)
        em.add_field(name="😜jokes", value="`;help jokes`", inline=True)
    if type == 'wikipedia':
        em = Embed(title="Melon Bot Help: Wikipedia", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="cool wikis", value="`;coolwikis`, get the link to a random wiki.", inline=True)
        em.add_field(name="wikis", value="`;wikis <wiki name>`, search wikipedia for the summary of the wiki you input.", inline=True)
        await ctx.channel.send(embed=em)
    if type == 'misc':
        em = Embed(title="Melon Bot Help: Miscellaneous", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="iss", value="`;iss`, look at the longitude and latitude of the iss.", inline=True)
        em.add_field(name="randomnumber", value="`;randomnumber`, get an interesting fact related to a random number.", inline=True)
        em.add_field(name="e", value="`;e <number>`, calculate the number e from a given n using the equation: (1 + 1/n)^n", inline=True)
        em.add_field(name="id", value="`;id`, get you user id.", inline=True)
        em.add_field(name="author", value="`;author <author name>`, get some facts about an author.", inline=True)
        em.add_field(name="insult", value="`;insult`, have the bot insult you.", inline=True)
        em.add_field(name="affirmation", value="`;affirmation`, get some affirmation, and feel better about yourself <3.", inline=True)
        em.add_field(name="advice", value="`;advice`, get some good advice about your life.", inline=True)
        em.add_field(name="nasa", value="`;nasa`, get a beautiful image and information about it from nasa apod.", inline=True)
        em.add_field(name="quote", value="`;quote`, get a quote.", inline=True)
        em.add_field(name="food", value="`;food`, get a picture of food.", inline=True)
        em.add_field(name="number", value="`;number <number>`, get info about a number", inline=True)
    if type == "games":
        em = Embed(title="Melon Bot Help: Games", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="free games", value="`;freegame`, use this and get some data about a random free game.", inline=True)
        em.add_field(name="magic", value="`;magic`, get data about a random magic the gathering card.", inline=True)
        em.add_field(name="bedwars", value="`;bedwars <username>`, get bedwars stats from the user you inputted", inline=True)
        em.add_field(name="skywars", value="`;skywars <username>`, get skywars stats from the user you inputted")
    if type == "animals":
        em = Embed(title="Melon Bot Help: Animals", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="shibu", value="`;shibu`, get a random shibu inu picture.", inline=True)
        em.add_field(name="fox", value="`;fox`, get a random fox picture.", inline=True)
        em.add_field(name="cat", value="`;cat`, get a random cat picture.", inline=True)
    if type == "jokes":
        em = Embed(title="Melon Bot Help: Jokes", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="tronalddump", value="`;tronalddump`, get a stupid trump quote", inline=True)
        em.add_field(name="programming joke", value="`;programmingjoke`, get a random programming joke", inline=True)
        em.add_field(name="general joke", value="`;generaljoke`, get a random general joke", inline=True)
        em.add_field(name="dad joke", value="`;dadjoke`, get a random dad joke", inline=True)
    
    em.add_field(name="pfp by:", value="brgfx on freepik.com")
    await ctx.channel.send(embed=em)

@bot.command()
async def plane(ctx):
    res = requests.get("https://en.wikipedia.org/wiki/List_of_aircraft_by_date_and_usage_category")
    soup = bs(res.text, "html.parser")
    wikisList = []
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if "/wiki/" in url and not "#" in url and not "Wikipedia:" in url and not "File:" in url and not "wikimedia" in url and not "wikidata" in url:
            wikisList.append(url)
    await ctx.channel.send("en.wikipedia.org" + wikisList[random.randint(0, len(wikisList)-1)])

@bot.command()
async def server_id(ctx):
    await ctx.channel.send(ctx.guild.id)


# == SLASH COMMANDS == #

slash = SlashCommand(bot, sync_commands=True)

# == SLASH COMMANDS == #





@slash.slash(name="wiki",
            description="This is just a test command, nothing more.",
            options=[
            create_option(
                name="wiki",
                description="The wiki you would like to be scraped.",
                option_type=3,
                required=True
            )
            ])

async def wiki(ctx, wiki: str):
    try:
        data = wikipedia.WikipediaPage(title = wiki).summary
    except Exception as e:
        data = str(e)
    data = data[0:2000]
    await ctx.channel.send(data)

@slash.slash(name="dadjoke", description="Get a funny dadjoke!")
async def dadjoke(ctx):
    res = requests.get("https://www.icanhazdadjoke.com/slack")
    await ctx.channel.send(res.json()["attachments"][0]["fallback"])

@slash.slash(name="nasa", description="Get a random nasa image with some facts about it!")
async def nasa(ctx):
        year = random.randint(1996, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 29)
        date = "{}-{}-{}".format(year, month, day)
        r = requests.get("https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(nasaKey, date))
        data2 = r.json()
        result = "\n{}: \n{}. \nThe image is found here: \n{}".format(data2["title"], data2["explanation"], data2["url"])
        await ctx.channel.send(result)

@slash.slash(name="id", description="Get your user id!")
async def id(ctx):
    await ctx.channel.send(ctx.author.id)

@slash.slash(name="programmingjoke", description="Get a random programming joke!")
async def programmingjoke(ctx):
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    res = requests.get(url)
    data = dict(res.json()[0])
    await ctx.channel.send(data["setup"]+data["punchline"])

@slash.slash(name="joke", description="Get just a general joke!")
async def generaljoke(ctx):
        url = "https://official-joke-api.appspot.com/jokes/general/random"
        res = requests.get(url)
        data = dict(res.json()[0])
        await ctx.channel.send(data["setup"]+data["punchline"])

@slash.slash(name="shibu", description="Get a random image of a shibu inu!")
async def shibu(ctx):
    url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true"
    res = requests.get(url)
    await ctx.channel.send(res.json()[0])

@slash.slash(name="Fox", description="Get a random fox image!")
async def fox(ctx):
    url = "https://randomfox.ca/floof/"
    res = requests.get(url)
    await ctx.channel.send(res.json()["image"])

@slash.slash(name="cat", description="Get a random cat image!")
async def cat(ctx):
    url = "https://api.thecatapi.com/v1/images/search/"
    res = requests.get(url)
    await ctx.channel.send(res.json()["url"])

@slash.slash(name="food", description="Get a random food image!")
async def food(ctx): 
        url = "https://foodish-api.herokuapp.com/api"
        res = requests.get(url)
        await ctx.channel.send(res.json()["image"])

@slash.slash(name="author", 
            description="Get data about an author of your choosing",
            options=[
                create_option(
                    name="author",
                    description="The author you would like to learn about", 
                    option_type=3,
                    required = True
                )
            ])
async def author(ctx, author: str):
        #https://openlibrary.org/search/authors.json?q=
        msglist = str(author).split(' ')
        msglist = msglist[1:]
        upname = str(msglist).replace(']', '').replace('[', '').replace(' ', '%20').replace(',', '').replace('\'', '')
        res = requests.get(f"https://openlibrary.org/search/authors.json?q={upname}")
        data = res.json()["docs"]
        data = list(data)[0]
        data = dict(data)
    # await message.channel.send(data["name"])
        em= Embed(title=data["name"], color=c.red())
        em.add_field(name="Birth", value=data["birth_date"], inline=True)
        em.add_field(name="Death", value=data["death_date"], inline=True)
        em.add_field(name="Top Work", value=data["top_work"], inline=True)
        await ctx.channel.send(embed=em)

@slash.slash(name="freegame", description="Get a statistics about random free game!")
async def freegame(ctx):
    id = random.randint(1, 512)
    res = requests.get(f"https://www.freetogame.com/api/game?id={id}")
    data = res.json()
    em = discord.Embed(title=data["title"], url=data["game_url"], description=data["short_description"], )
    em.add_field(name="Publisher", value=data["publisher"], inline=True)
    em.add_field(name="Developer", value=data["developer"], inline=True)
    em.add_field(name="Platform", value=data["platform"], inline=True)
    em.add_field(name="genre", value=data["genre"], inline=True)
    em.set_thumbnail(url="https://www.freetogame.com/g/427/thumbnail.jpg")
    await ctx.channel.send(embed=em)

@slash.slash(name="tronalddump", description="Get stupid donald trump quotes!")
async def tronalddump(ctx):
    url = "https://www.tronalddump.io/random/quote"
    res = requests.get(url)
    await ctx.channel.send("A stupid Trump quote is:" + " " + res.json()["value"])

@slash.slash(name="insult", description="Insult yourself!")
async def insult(ctx):
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    res = requests.get(url)
    await ctx.channel.send(ctx.author.mention + "," + " " + res.json()["insult"])

@slash.slash(name="quote", description="Get a random thought provoking quote!")
async def quote(ctx):
    url = "https://api.quotable.io/random"
    res = requests.get(url)
    await ctx.channel.send(res.json()["content"] + '\n' + '-' + res.json()["author"])

@slash.slash(name="advice", description="Get some cool life advice!")
async def advice(ctx):
    url = "https://api.adviceslip.com/advice"
    res = requests.get(url)
    await ctx.channel.send(res.json()["slip"]["advice"])

@slash.slash(name="coolwikis", description="Get a link to a cool, random, wiki!")
async def coolwikis(ctx):
    x = coolWikis()
    await ctx.channel.send("https://en.wikipedia.org/"+x)

@slash.slash(name="bedwars", description="Get someone's Hypixel bedwars stats",
            options=[
                create_option(
                    name="uname",
                    description="This is the person's Minecraft Username",
                    option_type=3,
                    required=True
                )
            ])
async def bedwars(ctx, uname: str):
    try:
            uuid = usernameToUUID(uname)
            uuid = json.loads(uuid)
            uuid = uuid["id"]
    except:
        pass
    statsRaw = getHypixelStats(uuid)
    try:
        playerKills = statsRaw["player"]["stats"]["Bedwars"]["kills_bedwars"]
        playerGames = statsRaw["player"]["stats"]["Bedwars"]["games_played_bedwars_1"]
        playerDeaths = statsRaw["player"]["stats"]["Bedwars"]["deaths_bedwars"]
        playerWins = statsRaw["player"]["stats"]["Bedwars"]["wins_bedwars"]
        playerLosses = int(playerGames) - int(playerWins)
        kd = playerKills/playerDeaths
        wnlRatio = playerWins/playerLosses
    
        await ctx.channel.send("{} has {} kills, and {} deaths, which makes a total k/d ratio of {}. They have won {} times, and lost {} times, for a win/loss ratio of {}.".format(uname, playerKills, playerDeaths, kd, playerWins, playerLosses, wnlRatio))
    except Exception as e:
        await ctx.channel.send("That is not a valid username")
        print(e)

@slash.slash(name="Skywars", description="Get someone's Hypixel skywars stats!",
            options=[ 
                create_option(
                    name="uname",
                    description="Minecraft Username",
                    option_type = 3,
                    required = True
                )
            ])
async def skywars(ctx, uname: str):
    try:
            uuid = usernameToUUID(uname)
            uuid = json.loads(uuid)
            uuid = uuid["id"]
    except:
        uuid = "none"
    
    statsRaw = getHypixelStats(uuid)
    try:
        playerWins = statsRaw["player"]["stats"]["SkyWars"]["wins"]
        playerGames = statsRaw["player"]["stats"]["SkyWars"]["games_played_skywars"]
        playerKills = statsRaw["player"]["stats"]["SkyWars"]["kills"]
        playerDeaths = playerGames - playerWins
        kd = playerKills/playerDeaths
        wnlRatio = playerWins/playerDeaths
        await ctx.channel.send("{} has {} kills, {} losses, for a k/d of {}, and has {} wins and {} losses, for a wnl ratio of {}".format(uname, playerKills, playerDeaths, kd, playerWins, playerDeaths, wnlRatio))
    except:
        await ctx.channel.send("That is not a valid username")

@slash.slash(name="magic", description="Get a random magic the gathering card stats!")
async def magic(ctx):
        running = True
        while running == True:
            try:
                card = Card.find(random.randint(1, 99999))
                cardType = card.type
                cardType = cardType.split(" ")
                if cardType[0] == "Creature":
                    result = "\nThe card {} costs {} with a power / toughness ratio of {} / {} \n{}".format(card.name, card.mana_cost, card.power, card.toughness, card.text)
                else:
                    result = "\nThe card {} costs {} \n{}".format(card.name, card.mana_cost, card.text)
                running = False
            except:
                pass
        await ctx.channel.send(result)

@slash.slash(name="e", description="calculate the number e using an equation, with one of the constants being your choosing!", 
            options=[ 
                create_option(
                    name="n",
                    description="This is the constant",
                    option_type = 4,
                    required=True
                )
            ])
async def e(ctx, n: int):
    #(1 + 1/n)^n
    beforeMultiply = 1 + 1/int(n)
    afterMultiply = beforeMultiply**float(n)
    await ctx.channel.send(afterMultiply)

@slash.slash(name="affirmation", description="Get some affirmation to help you through your day!")
async def affirmation(ctx):
    res = requests.get("https://www.affirmations.dev/")
    await ctx.channel.send(res.json()["affirmation"])

@slash.slash(name="randomnumber", description='Get facts about a random number!')
async def randomnumber(ctx):
    res = requests.get("http://numbersapi.com/random")
    await ctx.channel.send(res.text)

@slash.slash(name="number", description="Get facts about a number",
            options=[
                create_option(
                    name="n",
                    description="The number you want to get facta about",
                    option_type = 4,
                    required=True
            )])
async def number(ctx, n: int):
    res = requests.get(f"http://numbersapi.com/{n}")
    await ctx.channel.send(res.text)

@slash.slash(name="iss", description="Get the current latitude and longitude of the iss")
async def iss(ctx):
    res = requests.get("http://api.open-notify.org/iss-now.json")
    long = res.json()["iss_position"]["longitude"]
    lat = res.json()["iss_position"]["latitude"]
    await ctx.channel.send(f"Lat: {lat} \nLong: {long}")

@slash.slash(name="help", description="The default help command of MelonBot", 
            options=[
                create_option(
                    name="type", 
                    description="The type of help (not required)", 
                    option_type=4, 
                    required=False
                )
            ])
async def help(ctx, type:str=''):
    if type == '':
        em = Embed(title="Melon Bot Help", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="📓wikipedia", value="`;help wikipedia`", inline=True)
        em.add_field(name="😃miscellaneous", value="`;help misc`", inline=True)
        em.add_field(name="🎮games", value="`;help games`", inline=True)
        em.add_field(name="🐻animals", value="`;help animals`", inline=True)
        em.add_field(name="😜jokes", value="`;help jokes`", inline=True)
        em.add_field(name="pfp by:", value="brgfx on freepik.com")
    if type == 'wikipedia':
        em = Embed(title="Melon Bot Help: Wikipedia", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="cool wikis", value="`;coolwikis`, get the link to a random wiki.", inline=True)
        em.add_field(name="wikis", value="`;wikis <wiki name>`, search wikipedia for the summary of the wiki you input.", inline=True)
        em.add_field(name="pfp by:", value="brgfx on freepik.com")
        await ctx.channel.send(embed=em)
    if type == 'misc':
        em = Embed(title="Melon Bot Help: Miscellaneous", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="iss", value="`;iss`, look at the longitude and latitude of the iss.", inline=True)
        em.add_field(name="randomnumber", value="`;randomnumber`, get an interesting fact related to a random number.", inline=True)
        em.add_field(name="e", value="`;e <number>`, calculate the number e from a given n using the equation: (1 + 1/n)^n", inline=True)
        em.add_field(name="id", value="`;id`, get you user id.", inline=True)
        em.add_field(name="author", value="`;author <author name>`, get some facts about an author.", inline=True)
        em.add_field(name="insult", value="`;insult`, have the bot insult you.", inline=True)
        em.add_field(name="affirmation", value="`;affirmation`, get some affirmation, and feel better about yourself <3.", inline=True)
        em.add_field(name="advice", value="`;advice`, get some good advice about your life.", inline=True)
        em.add_field(name="nasa", value="`;nasa`, get a beautiful image and information about it from nasa apod.", inline=True)
        em.add_field(name="quote", value="`;quote`, get a quote.", inline=True)
        em.add_field(name="food", value="`;food`, get a picture of food.", inline=True)
        em.add_field(name="number", value="`;number <number>`, get info about a number", inline=True)
        em.add_field(name="pfp by:", value="brgfx on freepik.com")
    if type == "games":
        em = Embed(title="Melon Bot Help: Games", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="free games", value="`;freegame`, use this and get some data about a random free game.", inline=True)
        em.add_field(name="magic", value="`;magic`, get data about a random magic the gathering card.", inline=True)
        em.add_field(name="bedwars", value="`;bedwars <username>`, get bedwars stats from the user you inputted", inline=True)
        em.add_field(name="skywars", value="`;skywars <username>`, get skywars stats from the user you inputted")
        em.add_field(name="pfp by:", value="brgfx on freepik.com")
    if type == "animals":
        em = Embed(title="Melon Bot Help: Animals", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="shibu", value="`;shibu`, get a random shibu inu picture.", inline=True)
        em.add_field(name="fox", value="`;fox`, get a random fox picture.", inline=True)
        em.add_field(name="cat", value="`;cat`, get a random cat picture.", inline=True)
        em.add_field(name="pfp by:", value="brgfx on freepik.com")
    if type == "jokes":
        em = Embed(title="Melon Bot Help: Jokes", color=c.green(), description=f"The help for the information bot, Melon Bot. Thank you for adding me to {ctx.guild.name}!")
        em.add_field(name="tronalddump", value="`;tronalddump`, get a stupid trump quote", inline=True)
        em.add_field(name="programming joke", value="`;programmingjoke`, get a random programming joke", inline=True)
        em.add_field(name="general joke", value="`;generaljoke`, get a random general joke", inline=True)
        em.add_field(name="dad joke", value="`;dadjoke`, get a random dad joke", inline=True)
        em.add_field(name="pfp by:", value="brgfx on freepik.com")
    await ctx.channel.send(embed=em)

@slash.slash(name="plane", description="get the wikipedia link of a random plane!")
async def plane(ctx):
    res = requests.get("https://en.wikipedia.org/wiki/List_of_aircraft_by_date_and_usage_category")
    soup = bs(res.text, "html.parser")
    wikisList = []
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if "/wiki/" in url and not "#" in url and not "Wikipedia:" in url and not "File:" in url and not "wikimedia" in url and not "wikidata" in url:
            wikisList.append(url)
    await ctx.channel.send("en.wikipedia.org" + wikisList[random.randint(0, len(wikisList)-1)])

@slash.slash(name="server_id", description="Get your server id!")
async def server_id(ctx):
        await ctx.channel.send(ctx.guild.id)

with open('D:\MelonBot\config.json', 'r') as config:
    global Token, hypixelKey, nasaKey
    config_json = json.load(config)
    Token = config_json["Token"][0]
    hypixelKey = config_json["Hypixel-Api-Key"][0]
    nasaKey = config_json["Nasa-Api-Key"][0]


bot.run(Token)
