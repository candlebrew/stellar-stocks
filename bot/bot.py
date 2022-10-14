import discord
from discord.ext import commands
import random
import typing
import os
import asyncio
import asyncpg
import datetime

# placeholder: ODQxMDMyNTgzNjg4ODgwMTM4.GCLm8m.yoZatAZ4tv0rn53F_f8Vbs3BQzuxfFm3ny_8MU

# https://discord.com/api/oauth2/authorize?client_id=841032583688880138&permissions=126016&scope=bot

db = None

## SQL -----------------------------------------------------
playersSetupSQL = '''
    CREATE TABLE IF NOT EXISTS players (
        uid BIGINT NOT NULL,
        species TEXT,
        e_kfe BOOL DEFAULT false,
        e_ecce BOOL DEFAULT false,
        e_cwe BOOL DEFAULT false,
        e_dfe BOOL DEFAULT false,
        e_hfe BOOL DEFAULT false,
        e_ife BOOL DEFAULT false,
        e_lle BOOL DEFAULT false,
        e_mme BOOL DEFAULT false,
        e_rfe BOOL DEFAULT false,
        e_vion BOOL DEFAULT false,
        e_cenz BOOL DEFAULT false,
        e_leli BOOL DEFAULT false,
        e_aaro BOOL DEFAULT false,
        e_frey BOOL DEFAULT false,
        e_farm BOOL DEFAULT false,
        e_moth BOOL DEFAULT false,
        e_tori BOOL DEFAULT false,
        e_clem BOOL DEFAULT false,
        e_lach BOOL DEFAULT false,
        e_krab BOOL DEFAULT false,
        e_hors BOOL DEFAULT false,
        e_chas BOOL DEFAULT false,
        e_torr BOOL DEFAULT false,
        e_choe BOOL DEFAULT false,
        e_peon BOOL DEFAULT false,
        e_mich BOOL DEFAULT false,
        e_brut BOOL DEFAULT false,
        e_star BOOL DEFAULT false,
        e_aure BOOL DEFAULT false,
        e_grav BOOL DEFAULT false,
        e_lizb BOOL DEFAULT false,
        e_rune BOOL DEFAULT false,
        e_levy BOOL DEFAULT false,
        e_hawk BOOL DEFAULT false,
        e_brew BOOL DEFAULT false,
        badges_equipped INT DEFAULT 0,
        biz_type TEXT,
        biz_name TEXT,
        biz_level INT DEFAULT 0,
        biz_investment BIGINT DEFAULT 0,
        employees TEXT[],
        uniform TEXT,
        accessory TEXT,
        badges TEXT[]
        );'''
employeesSetupSQL = None
    #'''
    #CREATE TABLE IF NOT EXISTS employees (
        #uid BIGINT,
        #id INT,
        #name TEXT,
        #stock TEXT,
        #price INT,
        #type TEXT,
        #base TEXT,
        #eyes TEXT,
       # mouth TEXT,
        #nose TEXT,
       # hair TEXT
       # );'''
stocksSetupSQL = '''
    CREATE TABLE IF NOT EXISTS stocks (
        id TEXT,
        name TEXT,
        value BIGINT,
        phase TEXT,
        phase_weights INT[]
        );'''
portfoliosSetupSQL = '''
    CREATE TABLE IF NOT EXISTS portfolios (
        uid BIGINT NOT NULL,
        money BIGINT DEFAULT 100000,
        kfe_unlocked BOOL DEFAULT false,
        ecce_unlocked BOOL DEFAULT false,
        cwe_unlocked BOOL DEFAULT false,
        dfe_unlocked BOOL DEFAULT false,
        hfe_unlocked BOOL DEFAULT false,
        ife_unlocked BOOL DEFAULT false,
        lle_unlocked BOOL DEFAULT false,
        mme_unlocked BOOL DEFAULT false,
        rfe_unlocked BOOL DEFAULT false,
        vion_unlocked BOOL DEFAULT false,
        cenz_unlocked BOOL DEFAULT false,
        leli_unlocked BOOL DEFAULT false,
        aaro_unlocked BOOL DEFAULT false,
        frey_unlocked BOOL DEFAULT false,
        farm_unlocked BOOL DEFAULT false,
        moth_unlocked BOOL DEFAULT false,
        tori_unlocked BOOL DEFAULT false,
        clem_unlocked BOOL DEFAULT false,
        lach_unlocked BOOL DEFAULT false,
        krab_unlocked BOOL DEFAULT false,
        hors_unlocked BOOL DEFAULT false,
        chas_unlocked BOOL DEFAULT false,
        torr_unlocked BOOL DEFAULT false,
        choe_unlocked BOOL DEFAULT false,
        peon_unlocked BOOL DEFAULT false,
        mich_unlocked BOOL DEFAULT false,
        brut_unlocked BOOL DEFAULT false,
        star_unlocked BOOL DEFAULT false,
        aure_unlocked BOOL DEFAULT false,
        grav_unlocked BOOL DEFAULT false,
        lizb_unlocked BOOL DEFAULT false,
        rune_unlocked BOOL DEFAULT false,
        levy_unlocked BOOL DEFAULT false,
        hawk_unlocked BOOL DEFAULT false,
        brew_unlocked BOOL DEFAULT false,
        kfe_stocks BIGINT DEFAULT 0,
        ecce_stocks BIGINT DEFAULT 0,
        cwe_stocks BIGINT DEFAULT 0,
        dfe_stocks BIGINT DEFAULT 0,
        hfe_stocks BIGINT DEFAULT 0,
        ife_stocks BIGINT DEFAULT 0,
        lle_stocks BIGINT DEFAULT 0,
        mme_stocks BIGINT DEFAULT 0,
        rfe_stocks BIGINT DEFAULT 0,
        vion_stocks BIGINT DEFAULT 0,
        cenz_stocks BIGINT DEFAULT 0,
        leli_stocks BIGINT DEFAULT 0,
        aaro_stocks BIGINT DEFAULT 0,
        frey_stocks BIGINT DEFAULT 0,
        farm_stocks BIGINT DEFAULT 0,
        moth_stocks BIGINT DEFAULT 0,
        tori_stocks BIGINT DEFAULT 0,
        clem_stocks BIGINT DEFAULT 0,
        lach_stocks BIGINT DEFAULT 0,
        krab_stocks BIGINT DEFAULT 0,
        hors_stocks BIGINT DEFAULT 0,
        chas_stocks BIGINT DEFAULT 0,
        torr_stocks BIGINT DEFAULT 0,
        choe_stocks BIGINT DEFAULT 0,
        peon_stocks BIGINT DEFAULT 0,
        mich_stocks BIGINT DEFAULT 0,
        brut_stocks BIGINT DEFAULT 0,
        star_stocks BIGINT DEFAULT 0,
        aure_stocks BIGINT DEFAULT 0,
        grav_stocks BIGINT DEFAULT 0,
        lizb_stocks BIGINT DEFAULT 0,
        rune_stocks BIGINT DEFAULT 0,
        levy_stocks BIGINT DEFAULT 0,
        hawk_stocks BIGINT DEFAULT 0,
        brew_stocks BIGINT DEFAULT 0
        );'''
newsSetupSQL = '''
    CREATE TABLE IF NOT EXISTS news (
        weekday TEXT,
        news_text TEXT,
        effect TEXT,
        stock TEXT
        );'''
timeMasterSQL = '''
    CREATE TABLE IF NOT EXISTS time_master (
        id TEXT,
        hour INT,
        stocks TEXT[]
        );'''

## Connecting the DB ----------------------------------------------------------
# TODO db loop
async def run():
    global db
    
    dbURL = os.environ.get('DATABASE_URL')
    db = await asyncpg.connect(dsn=dbURL, ssl='require')
    
    await db.execute(playersSetupSQL)
    await db.execute(stocksSetupSQL)
    await db.execute(portfoliosSetupSQL)
    await db.execute(newsSetupSQL)
    await db.execute(timeMasterSQL)

    emptyList = []
    checkDev = await db.fetchval('''
    SELECT uid FROM players WHERE uid = $1;''',devID)
    if checkDev is None:
        await db.execute('''
        INSERT INTO players VALUES ($1,'Human',True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,0,$2,$2,0,0,$3,$2,$2,$3);''',devID,None,emptyList)
    checkDevPortfolio = await db.fetchval('''
    SELECT uid FROM portfolios WHERE uid = $1;''',devID)
    if checkDevPortfolio is None:
        await db.execute('''
        INSERT INTO portfolios VALUES ($1,1000000000,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)''',devID)
    checkTimeMaster = await db.fetchval('''SELECT id FROM time_master WHERE id = '00MASTER00';''')
    if checkTimeMaster is None:
        currentStocks = [
            "KF.E",
            "ECC.E",
            "CW.E",
            "DF.E",
            "IF.E",
            "MM.E",
            "RF.E",
            "LF.E",
            "HL.E",
            "FREY",
            "STAR",
            "PEON",
            "BRUT",
            "BREW",
            "VION",
            "CENZ",
            "LELI",
            "AARO",
            "FARM",
            "MOTH",
            "TORI",
            "CLEM",
            "LACH",
            "KRAB",
            "HORS",
            "CHAS",
            "TORR",
            "CHOE",
            "MICH",
            "AURE",
            "GRAV",
            "LIZB",
            "RUNE",
            "LEVY",
            "HAWK",
            "BLBR",
            "GHWD",
            "MINK",
            "CHUR",
            "CHES",
            "KRYK",
            "MACK",
            "CAES",
            "PETR",
            "MARZ",
            "LAWR",
            "DWYN"
            ]
        now = datetime.datetime.now()
        await db.execute('''INSERT INTO time_master VALUES ('00MASTER00',$1,$2);''',now.hour,currentStocks)

## Bot Setup ----------------------------------------------------------
token = os.environ.get('DISCORD_BOT_TOKEN')
devID = int(os.environ.get('DEV_ID'))
stockPrices = int(os.environ.get('STOCK_PRICES_MESSAGE'))
stockChannelID = int(os.environ.get('STOCK_LOGS_CHANNEL'))
pricesChannelID = int(os.environ.get('STOCK_PRICES_CHANNEL'))
client = discord.Client()

bot = commands.Bot(command_prefix='ss.', db=db)

def is_dev():
    def predicate(ctx):
        return ctx.message.author.id == devID
    return commands.check(predicate)

stockPhases = [
    "slow growth",
    "fast growth",
    "slow decay",
    "fast decay",
    "stable",
    "chaotic growth",
    "chaotic decay",
    "chaotic stable",
    "true chaos"
]
stockPatterns = [
    "huge increase",
    "big increase",
    "small increase",
    "no change",
    "small decrease",
    "big decrease",
    "huge decrease"
]

## Automatic Actions -------------------------------------

@bot.event
async def on_ready():
    bot.loop.create_task(stocks_task())
    
async def update_stock_message():
    pricesChannel = bot.get_channel(pricesChannelID)
    channelMessage = ""
    stocksList = await db.fetchval('''SELECT stocks FROM time_master WHERE id = '00MASTER00';''')
    for stockID in stocksList:
        currentStockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
        currentStockName = await db.fetchval('''SELECT name FROM stocks WHERE id = $1;''',stockID)
        channelMessage += "[" + stockID + "] " + currentStockName + ": $" + str(currentStockValue) + "\n"
    channelMessage = "```Current Stock Prices:\n" + channelMessage + "```"
    pricesMessage = await pricesChannel.fetch_message(stockPrices)
    await pricesMessage.edit(content=channelMessage)

async def stocks_task():
    await asyncio.sleep(10)
    while True:
        logMessage = ""
        stocksChannel = bot.get_channel(stockChannelID)
        now = datetime.datetime.now()
        storedHour = await db.fetchval('''SELECT hour FROM time_master WHERE id = '00MASTER00';''')
        if now.hour != storedHour:
            stocksList = await db.fetchval('''SELECT stocks FROM time_master WHERE id = '00MASTER00';''')
            for stockID in stocksList:
                if now.hour == 5:
                    phase = await db.fetchval('''SELECT phase FROM stocks WHERE id = $1;''',stockID)
                    if phase == "slow growth":
                        patternWeights = [0,0,50,50,0,0,0]
                    elif phase == "fast growth":
                        patternWeights = [20,30,35,15,0,0,0]
                    elif phase == "slow decay":
                        patternWeights = [0,0,0,50,50,0,0]
                    elif phase == "fast decay":
                        patternWeights = [0,0,0,15,35,30,20]
                    elif phase == "chaotic growth":
                        patternWeights = [20,20,20,20,20,0,0]
                    elif phase == "chaotic decay":
                        patternWeights = [0,0,20,20,20,20,20]
                    elif phase == "stable":
                        patternWeights = [0,0,33,34,33,0,0]
                    elif phase == "chaotic stable":
                        patternWeights = [0,20,20,20,20,20,0]
                    elif phase == "true chaos":
                        patternWeights = [15,15,15,10,15,15,15]
                    pattern = random.choices(stockPatterns, weights=patternWeights,k=1)[0]
                    await db.execute('''UPDATE stocks SET pattern = $1 WHERE id = $2;''',pattern,stockID)
                currentPattern = await db.fetchval('''SELECT pattern FROM stocks WHERE id = $1;''',stockID)
                if currentPattern in ["huge increase","huge decrease"]:
                    changeMin = 100
                    changeMax = 1000
                elif currentPattern in ["big increase","big decrease"]:
                    changeMin = 50
                    changeMax = 100
                elif currentPattern in ["small increase","small decrease"]:
                    changeMin = 10
                    changeMax = 50
                elif currentPattern == "no change":
                    changeMin = 0
                    changeMax = 20
                changeValue = random.randint(changeMin, changeMax)
                if currentPattern in ["huge decrease","big decrease","small decrease"]:
                    changeValue *= -1
                elif currentPattern == "no change":
                    if changeValue > 10:
                        changeValue -= 10
                        changeValue *= -1
                currentStockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
                newValue = currentStockValue + changeValue
                if newValue <= 0:
                    newValue = 1
                await db.execute('''UPDATE stocks SET value = $1 WHERE id = $2;''',newValue,stockID)
                logMessage += stockID + " " + str(currentStockValue) + " >>> " + str(newValue) + "\n"
            await db.execute('''UPDATE time_master SET hour = $1 WHERE id = '00MASTER00';''',now.hour)
            logMessage = "``` ```" + logMessage
            await stocksChannel.send(logMessage)
            await update_stock_message()
        await asyncio.sleep(30)


## Commands ----------------------------------------------------------
@bot.command(aliases=["c"])
async def calculate(ctx, stockID: str, numberStocks: int):
    stockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
    if stockValue is None:
        await ctx.send("Sorry, I could not find stock with the ID \"" + stockID + "\"")
    else:
        cost = stockValue * numberStocks
        await ctx.send("The value of " + str(numberStocks) + " of " + stockID + " would be **$" + str(cost) + "**")

@bot.command(aliases=["p"])
async def portfolio(ctx):
    user = ctx.message.author.id
    name = ctx.message.author.name
    userMoney = await db.fetchval('''SELECT money FROM portfolios WHERE uid = $1;''',user)
    portfolioMessage = "__**" + name + "'s Portfolio:**__"
    stocksList = await db.fetchval('''SELECT stocks FROM time_master WHERE id = '00MASTER00';''')
    stockCounter = 1
    for stockID in stocksList:
        lowerID = stockID.lower()
        try:
            lowerID = lowerID.replace(".", "")
        except:
            pass
        stockName = await db.fetchval('''SELECT name FROM stocks WHERE id = $1;''',stockID)
        accessText = "SELECT " + lowerID + "_unlocked FROM portfolios WHERE uid = $1;"
        userAccess = await db.fetchval(accessText,user)
        if userAccess == False:
            pass
        else:
            stocksText = '''SELECT ''' + lowerID + '''_stocks FROM portfolios WHERE uid = $1;'''
            userStocks = await db.fetchval(stocksText,user)
            stockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
            if userStocks is None:
                userStocks = 0
            valueOwned = userStocks * stockValue
            if userStocks == 0:
                pass
            else:
                portfolioMessage += "\n*"
                portfolioMessage += stockName
                portfolioMessage += " [" + stockID + "]:* "
                portfolioMessage += "$" + str(valueOwned) + " | "
                portfolioMessage += str(userStocks)
                stockCounter += 1
        if stockCounter >= 20:
            await ctx.send(portfolioMessage)
            portfolioMessage = ""
            stockCounter = 0
    await ctx.send(portfolioMessage)

@bot.command(aliases=["prices"])
async def stocks(ctx):
    pricesChannel = bot.get_channel(pricesChannelID)
    pricesMessage = await pricesChannel.fetch_message(stockPrices)
    await ctx.send(pricesMessage.content)

@bot.command(aliases=["b"])
async def buy(ctx, stockID: str, numberStocks: int):
    user = ctx.message.author.id
    stockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
    lowercaseID = stockID.lower()
    userMoney = await db.fetchval('''SELECT money FROM portfolios WHERE uid = $1;''',user)
    accessText = '''SELECT ''' + lowercaseID + '''_unlocked FROM portfolios WHERE uid = $1;'''
    userAccess = await db.fetchval(accessText,user)
    stocksText = '''SELECT ''' + lowercaseID + '''_stocks FROM portfolios WHERE uid = $1;'''
    userStocks = await db.fetchval(stocksText,user)
    if stockValue is None:
        await ctx.send("Sorry, I could not find stock with the ID \"" + stockID + "\"")
    elif userAccess == False:
        await ctx.send("Sorry, you do not have access to " + stockID + ". Purchase access with `ss.unlock " + stockID + "` for $10,000.")
    else:
        cost = stockValue * numberStocks
        if userMoney < cost:
            await ctx.send("You cannot afford to purchase " + str(numberStocks) + " of " + stockID + " stocks (value of $" + str(cost) + ")")
        else:
            userMoney -= cost
            userStocks += numberStocks
            updateStocksText = '''UPDATE portfolios SET ''' + stockID + '''_stocks = $1 WHERE uid = $2'''
            await db.execute(updateStocksText,userStocks,user)
            await db.execute('''UPDATE portfolios SET money = $1 WHERE uid = $2''',userMoney,user)
            await ctx.send("You have purchased " + str(numberStocks) + " for $" + str(cost) + ". \nCurrent money: $" + str(userMoney) + "\nCurrent number of " + stockID + " stocks: " + str(userStocks))
        
@bot.command(aliases=["s"])
async def sell(ctx, stockID: str, numberStocks: int):
    user = ctx.message.author.id
    stockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
    lowercaseID = stockID.lower()
    userMoney = await db.fetchval('''SELECT money FROM portfolios WHERE uid = $1;''',user)
    accessText = '''SELECT ''' + lowercaseID + '''_unlocked FROM portfolios WHERE uid = $1;'''
    userAccess = await db.fetchval(accessText,user)
    stocksText = '''SELECT ''' + lowercaseID + '''_stocks FROM portfolios WHERE uid = $1;'''
    userStocks = await db.fetchval(stocksText,user)
    if stockValue is None:
        await ctx.send("Sorry, I could not find stock with the ID \"" + stockID + "\"")
    elif userAccess == False:
        await ctx.send("Sorry, you do not have access to " + stockID + ". Purchase access with `ss.unlock " + stockID + "` for $10,000.")
    else:
        cost = stockValue * numberStocks
        if userStocks < numberStocks:
            await ctx.send("You do not have " + str(numberStocks) + " " + stockID + " stocks. Current amount of stocks held: " + str(userStocks))
        else:
            userMoney += cost
            userStocks -= numberStocks
            updateStocksText = '''UPDATE portfolios SET ''' + stockID + '''_stocks = $1 WHERE uid = $2'''
            await db.execute(updateStocksText,userStocks,user)
            await db.execute('''UPDATE portfolios SET money = $1 WHERE uid = $2''',userMoney,user)
            await ctx.send("You have sold " + str(numberStocks) + " stocks for $" + str(cost) + ". \nCurrent money: $" + str(userMoney) + "\nCurrent number of " + stockID + " stocks: " + str(userStocks))

@bot.command()
async def unlock(ctx, stockID: str):
    lowercaseID = stockID.lower()
    user = ctx.message.author.id
    accessText = '''SELECT ''' + lowercaseID + '''_unlocked FROM portfolios WHERE uid = $1;'''
    userAccess = await db.fetchval(accessText,user)
    userMoney = await db.fetchval('''SELECT money FROM portfolios WHERE uid = $1;''',user)
    stockValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''',stockID)
    if stockValue is None:
        await ctx.send("Sorry, I could not find stock with the ID \"" + stockID + "\"")
    elif userAccess == True:
        await ctx.send("You already have access to " + stockID)
    elif userMoney < 10000:
        await ctx.send("You do not have enough money to purchase access. Access costs $10,000.")
    else:
        userMoney -= 10000
        await db.execute('''UPDATE portfolios SET money = $1 WHERE uid = $2''',userMoney,user)
        updateStocksText = '''UPDATE portfolios SET ''' + stockID + '''_unlocked = true WHERE uid = $1'''
        await db.execute(updateStocksText,user)
        await ctx.send("Congratulations! You now have access to " + stockID)
    
@bot.group(invoke_without_command=True)
async def species(ctx):
    await ctx.send("You can be the following species: *Krawzird, Human, Phomaek, Hvellen, Halosynth, Illiet, Elovias, Spacemun, or Retega*\n(WIP: a list of abilities will come soon!)")
    
@species.command()
async def set(ctx, species: str):
    userID = ctx.message.author.id
    species = species.lower()
    currentSpecies = await db.fetchval('''SELECT species FROM players WHERE uid = $1;''',userID)
    if species not in ["krawzird","human","phomaek","hvellen","halosynth","illiet","elovias","spacemun","retega"]:
        await ctx.send("Please select a valid species.")
    elif currentSpecies != None:
        await ctx.send("You already have a species selected.")
    else:
        species = species.capitalize()
        await db.execute('''UPDATE players SET species = $1 WHERE uid = $2;''',species,userID)
        if species == "Krawzird":
            stock = "kfe"
            aan = "a "
        elif species == "Human":
            stock = "ecce"
            aan = "a "
        elif species == "Phomaek":
            stock = "cwe"
            aan = "a "
        elif species == "Hvellen":
            stock = "dfe"
            aan = "a "
        elif species == "Halosynth":
            stock = "hle"
            aan = "a "
        elif species == "Illiet":
            stock = "ife"
            aan = "an "
        elif species == "Elovias":
            stock = "lfe"
            aan = "an "
        elif species == "Spacemun":
            stock = "mme"
            aan = "a "
        elif species == "Retega":
            stock = "rfe"
            aan = "a "
        unlockText = '''UPDATE portfolios SET ''' + stock + '''_unlocked = True WHERE uid = $1;'''
        await db.execute(unlockText,userID)
        stocksText = '''UPDATE portfolios SET ''' + stock + '''_stocks = 5 WHERE uid = $1;'''
        await db.execute(stocksText,userID)
        await db.execute('''UPDATE portfolios SET money = 100000 WHERE uid = $1;''',userID)
        await ctx.send("Congratulations! You are now " + aan + species + " and ready to buy stocks!")

@bot.command()
async def start(ctx):
    userID = ctx.message.author.id
    currentUser = await db.fetchval('''SELECT uid FROM players WHERE uid = $1;''',userID)
    if currentUser != None:
        await ctx.send("You are already registered!")
    else:
        await db.execute('''INSERT INTO players (uid) VALUES ($1);''',userID)
        await db.execute('''INSERT INTO portfolios (uid, money) VALUES ($1,0);''',userID)
        await ctx.send("You are signed up with the Stellar Stocks trading network. Please use `ss.species` to view the list of species, then use `ss.species set <species>` to set the species you are.")
    

## Dev Commands ------------------------------------------------------
@bot.group()
async def dev(ctx):
    pass
    
@dev.group()
async def set(ctx):
    pass
    
@dev.group()
async def get(ctx):
    pass
    
@dev.group()
async def test(ctx):
    pass
    
@dev.group()
async def new(ctx):
    pass

@dev.command()
@is_dev()
async def stimulus(ctx, stockID: str, increase: int):
    stocksChannel = bot.get_channel(stockChannelID)
    currentValue = await db.fetchval('''SELECT value FROM stocks WHERE id = $1;''', stockID)
    newValue = currentValue + increase
    await db.execute('''UPDATE stocks SET value = $1 WHERE id = $2;''',newValue,stockID)
    await update_stock_message()
    logMessage = stockID + " stimulus: " + str(increase)
    logMessage = "``` ```" + logMessage
    await stocksChannel.send(logMessage)
    await ctx.send("Task complete.")
    
@new.command()
@is_dev()
async def stock(ctx, stockID: str, slowGrow: int, fastGrow: int, slowDecay: int, fastDecay: int, stable: int, chaoticGrow: int, chaoticDecay: int, chaoticStable: int, chaos: int, *, stockName: str):
    stockList = await db.fetchval('''SELECT stocks FROM time_master WHERE id = '00MASTER00';''')
    if stockID in stockList:
        await ctx.send("That stock ID already exists.")
    else:
        phaseWeights = []
        phaseWeights.append(slowGrow)
        phaseWeights.append(fastGrow)
        phaseWeights.append(slowDecay)
        phaseWeights.append(fastDecay)
        phaseWeights.append(stable)
        phaseWeights.append(chaoticGrow)
        phaseWeights.append(chaoticDecay)
        phaseWeights.append(chaoticStable)
        phaseWeights.append(chaos)
        startPhase = random.choices(stockPhases, weights=phaseWeights,k=1)[0]
        if startPhase == "slow growth":
            patternWeights = [0,0,50,50,0,0,0]
        elif startPhase == "fast growth":
            patternWeights = [20,30,35,15,0,0,0]
        elif startPhase == "slow decay":
            patternWeights = [0,0,0,50,50,0,0]
        elif startPhase == "fast decay":
            patternWeights = [0,0,0,15,35,30,20]
        elif startPhase == "chaotic growth":
            patternWeights = [20,20,20,20,20,0,0]
        elif startPhase == "chaotic decay":
            patternWeights = [0,0,20,20,20,20,20]
        elif startPhase == "stable":
            patternWeights = [0,0,33,34,33,0,0]
        elif startPhase == "chaotic stable":
            patternWeights = [0,20,20,20,20,20,0]
        elif startPhase == "true chaos":
            patternWeights = [15,15,15,10,15,15,15]
        pattern = random.choices(stockPatterns, weights=patternWeights,k=1)[0]
        await db.execute('''INSERT INTO stocks VALUES ($1,$2,10000,$3,$4,$5);''',stockID,stockName,startPhase,phaseWeights,pattern)
        lowerCaseID = stockID.lower()
        playersText = '''ALTER TABLE players ADD COLUMN e_''' + lowerCaseID + ''' BOOL DEFAULT false;'''
        portfoliosUnlockText = '''ALTER TABLE portfolios ADD COLUMN ''' + lowerCaseID + '''_unlocked BOOL DEFAULT false;'''
        portfoliosStocksText = '''ALTER TABLE portfolios ADD COLUMN ''' + lowerCaseID + '''_stocks BIGINT DEFAULT 0;'''
        devPlayersText = '''UPDATE players SET e_''' + lowerCaseID + ''' = true WHERE uid = ''' + str(devID) + ''';'''
        devPortfoliosText = '''UPDATE portfolios SET ''' + lowerCaseID + '''_unlocked true WHERE uid = ''' + str(devID) + ''';'''
        await db.execute(playersText)
        await db.execute(portfoliosUnlockText)
        await db.execute(portfoliosStocksText)
        await db.execute(devPlayersText)
        await db.execute(devPortfoliosText)
        stockList.append(stockID)
        await db.execute('''UPDATE time_master SET stocks = $1 WHERE id = '00MASTER00';''',stockList)
        await ctx.send("Added " + stockName + " (" + stockID + ") to database successfully.")   

@test.command()
@is_dev()
async def list(ctx, slowGrow: int, fastGrow: int, slowDecay: int, fastDecay: int, stable: int, chaoticGrow: int, chaoticDecay: int, chaoticStable: int, chaos: int):
    #phaseWeights = []
    #phaseWeights.append(slowGrow)
    #phaseWeights.append(fastGrow)
    #phaseWeights.append(slowDecay)
    #phaseWeights.append(fastDecay)
    #phaseWeights.append(stable)
    #phaseWeights.append(chaoticGrow)
    #phaseWeights.append(chaoticDecay)
    #phaseWeights.append(chaoticStable)
    #phaseWeights.append(chaos)
    pass

@set.command()
@is_dev()
async def stockname(ctx, stockID: str, *, newName: str):
    await db.execute('''UPDATE stocks SET name = $1 WHERE id = $2;''',newName,stockID)
    await ctx.send(stockID + " has been set to " + newName)
    
@set.command()
@is_dev()
async def stockID(ctx, stockID: str, newID: str):
    await db.execute('''UPDATE stocks SET id = $1 WHERE id = $2;''',newID,stockID)
    stockList = await db.fetchval('''SELECT stocks FROM time_master WHERE id = '00MASTER00';''')
    stockList.remove(stockID)
    stockList.append(newID)
    await db.execute('''UPDATE time_master SET stocks = $1 WHERE id = '00MASTER00';''',stockList)
    await ctx.send(stockID + " has been set to " + newID)
    
@set.command()
@is_dev()
async def add_stock_fix(ctx):
#    stockFixList = ["BLBR","GHWD","MINK","CHUR","CHES","KRYK","MACK","CAES","PETR","MARZ","DWYN","LAWR"]
#    for stockID in stockFixList:
#        lowerCaseID = stockID.lower()
#        playersText = '''UPDATE players SET e_''' + lowerCaseID + ''' = true WHERE uid = ''' + str(devID) + ''';'''
#        portfoliosUnlockText = '''ALTER TABLE portfolios ADD COLUMN ''' + lowerCaseID + '''_unlocked BOOL DEFAULT false;'''
#        portfoliosStocksText = '''ALTER TABLE portfolios ADD COLUMN ''' + lowerCaseID + '''_stocks BIGINT DEFAULT 0;'''
#        portfoliosText = '''UPDATE portfolios SET ''' + lowerCaseID + '''_unlocked = true WHERE uid = ''' + str(devID) + ''';'''
#        await db.execute(playersText)
#        try:
#            await db.execute(portfoliosUnlockText)
#        except:
#            pass
#        try:
#            await db.execute(portfoliosStocksText)
#        except:
#            pass
#        await db.execute(portfoliosText)
#    await ctx.send("All done!")
    pass
    
@set.command()
@is_dev()
async def stock_patterns_fix(ctx):
    await db.execute('''ALTER TABLE stocks ADD COLUMN pattern TEXT;''')
    await ctx.send("Fix complete.")
    
@set.command()
@is_dev()
async def new_day(ctx):
    stocksList = await db.fetchval('''SELECT stocks FROM time_master WHERE id = '00MASTER00';''')
    for stockID in stocksList:
        phase = await db.fetchval('''SELECT phase FROM stocks WHERE id = $1;''',stockID)
        if phase == "slow growth":
            patternWeights = [0,0,50,50,0,0,0]
        elif phase == "fast growth":
            patternWeights = [20,30,35,15,0,0,0]
        elif phase == "slow decay":
            patternWeights = [0,0,0,50,50,0,0]
        elif phase == "fast decay":
            patternWeights = [0,0,0,15,35,30,20]
        elif phase == "chaotic growth":
            patternWeights = [20,20,20,20,20,0,0]
        elif phase == "chaotic decay":
            patternWeights = [0,0,20,20,20,20,20]
        elif phase == "stable":
            patternWeights = [0,0,33,34,33,0,0]
        elif phase == "chaotic stable":
            patternWeights = [0,20,20,20,20,20,0]
        elif phase == "true chaos":
            patternWeights = [15,15,15,10,15,15,15]
        pattern = random.choices(stockPatterns, weights=patternWeights,k=1)[0]
        await db.execute('''UPDATE stocks SET pattern = $1 WHERE id = $2;''',pattern,stockID)
    await ctx.send("Task complete.")
    
@dev.group()
async def delete(ctx):
    pass

@dev.group()
async def quick_fix(ctx):
    await db.execute('''ALTER TABLE portfolios RENAME COLUMN hfe_unlocked TO hle_unlocked;''')
    await db.execute('''ALTER TABLE portfolios RENAME COLUMN hfe_stocks TO hle_stocks;''')
    await db.execute('''ALTER TABLE portfolios RENAME COLUMN lle_unlocked TO lfe_unlocked;''')
    await db.execute('''ALTER TABLE portfolios RENAME COLUMN lle_stocks TO lfe_stocks;''')
    await ctx.send("Fix completed.")

#@delete.command()
#@is_dev()
#async def table_reset(ctx):
    #await db.execute('''DROP TABLE players;''')
    #await db.execute('''DROP TABLE portfolios;''')
    #await ctx.send("Fix complete.")

## Bot Setup & Activation ----------------------------------------------------------
asyncio.get_event_loop().run_until_complete(run())
bot.run(token)
