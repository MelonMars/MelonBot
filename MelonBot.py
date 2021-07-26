import discord, wikipedia, requests, random, json
from bs4 import BeautifulSoup as bs
from mtgsdk import Card


with open('D:\MelonBot\config.json', 'r') as config:
    global fortniteKey, Token, hypixelKey, nasaKey
    config_json = json.load(config)
    Token = config_json["Token"][0]
    hypixelKey = config_json["Hypixel-Api-Key"][0]
    nasaKey = config_json["Nasa-Api-Key"][0]

def coolWikis():
    res = requests.get("https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles")
    soup = bs(res.text, "html.parser")
    wikisList = []
    global badList
    badList = ["Kuso_Miso_Technique", "MILF_pornography", "Forest_swastika", "National_Rifle_Association", "Sex_position"]
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if "/wiki/" in url:
            wikisList.append(url)

    toSend = wikisList[random.randint(0, len(wikisList))]
    if toSend in badList:
        toSend = "Sorry, but the article the random number generator landed on... is not the most appropriate."
    return toSend

def usernameToUUID(uname):
    res = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uname}")
    return(res.text)

def getHypixelStats(uuid):
    res = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(hypixelKey, uuid))
    return res.json()


client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(';cool wikis'):
        x = coolWikis()
        await message.channel.send("https://en.wikipedia.org/"+x)
    
    if message.content.startswith(';wiki'):
        x = message.content
        x = x.replace(";wiki ", "")
        try:
          data = wikipedia.WikipediaPage(title = x).summary
        except Exception as e:
          data = str(e)
        data = data[0:2000]
        await message.channel.send(data)
        
    if message.content.startswith(';bedwars'):
        import json
        try:
            usersMessage = str(message.content)
            usersMessage = usersMessage.split(" ")
            uuid = usernameToUUID(usersMessage[1])
            uuid = json.loads(uuid)
            uuid = uuid["id"]
        except Exception as e:
            print(e)
            
        statsRaw = getHypixelStats(uuid)
        try:
            playerKills = statsRaw["player"]["stats"]["Bedwars"]["kills_bedwars"]
            playerGames = statsRaw["player"]["stats"]["Bedwars"]["games_played_bedwars_1"]
            playerDeaths = statsRaw["player"]["stats"]["Bedwars"]["deaths_bedwars"]
            playerWins = statsRaw["player"]["stats"]["Bedwars"]["wins_bedwars"]
            playerLosses = int(playerGames) - int(playerWins)
            kd = playerKills/playerDeaths
            wnlRatio = playerWins/playerLosses
        
            await message.channel.send("{} has {} kills, and {} deaths, which makes a total k/d ratio of {}. They have won {} times, and lost {} times, for a win/loss ratio of {}.".format(usersMessage[1], playerKills, playerDeaths, kd, playerWins, playerLosses, wnlRatio))
        except Exception as e:
           # await message.channel.send("That is not a valid username")
           print(e)

    if message.content.startswith(';skywars'):
        import json
        try:
            usersMessage = str(message.content)
            usersMessage = usersMessage.split(" ")
            uuid = usernameToUUID(usersMessage[1])
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
            await message.channel.send("{} has {} kills, {} losses, for a k/d of {}, and has {} wins and {} losses, for a wnl ratio of {}".format(usersMessage[1], playerKills, playerDeaths, kd, playerWins, playerDeaths, wnlRatio))
        except:
            await message.channel.send("That is not a valid username")

    if message.content.startswith(';dadjoke'):
        res = requests.get("https://www.icanhazdadjoke.com/slack")
        await message.channel.send(res.json()["attachments"][0]["fallback"])

    if message.content.startswith(';magic'):
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
        await message.channel.send(result)

    if message.content.startswith(';nasa'):
        import json
        year = random.randint(1996, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 29)
        date = "{}-{}-{}".format(year, month, day)
        r = requests.get("https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(nasaKey, date))
        data2 = r.json()
        result = "\n{}: \n{}. \nThe image is found here: \n{}".format(data2["title"], data2["explanation"], data2["url"])
        await message.channel.send(result)

    if message.content.startswith(';e'):
        x = message.content.split(' ')
        n = x[1]
        #(1 + 1/n)^n
        beforeMultiply = 1 + 1/int(n)
        afterMultiply = beforeMultiply**float(n)
        await message.channel.send(afterMultiply)

    if message.content.startswith(';id'):
        await message.channel.send(f"Your discord user id is {message.author.id}")

    if message.content.startswith(';airplane'):
        content = message.content.split(' ')
        url = f'https://contentzone.eurocontrol.int/aircraftperformance/default.aspx?NameFilter={content[1]}'
        

client.run(Token)