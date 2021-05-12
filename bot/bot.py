# FIX ON UPLOAD:
# DB loop: line
# Token ID: line
# Start async loop: line
import discord
from discord.ext import commands
import random
import typing
import os
import asyncio
import asyncpg
import datetime

# https://discord.com/api/oauth2/authorize?client_id=841032583688880138&permissions=126016&scope=bot

db = None

## SQL -----------------------------------------------------
playersSetupSQL = '''
    CREATE TABLE IF NOT EXISTS players (
        uid BIGINT,
        species TEXT,
        e_kfe BOOL,
        e_ecce BOOL,
        e_cwe BOOL,
        e_dfe BOOL,
        e_hfe BOOL,
        e_ife BOOL,
        e_lle BOOL,
        e_mme BOOL,
        e_rfe BOOL,
        e_vion BOOL,
        e_cenz BOOL,
        e_leli BOOL,
        e_aaro BOOL,
        e_frey BOOL,
        e_farm BOOL,
        e_moth BOOL,
        e_tori BOOL,
        e_clem BOOL,
        e_lach BOOL,
        e_krab BOOL,
        e_hors BOOL,
        e_chas BOOL,
        e_torr BOOL,
        e_choe BOOL,
        e_peon BOOL,
        e_mich BOOL,
        e_brut BOOL,
        e_star BOOL,
        e_aure BOOL,
        e_grav BOOL,
        e_lizb BOOL,
        e_rune BOOL,
        e_levy BOOL,
        e_hawk BOOL,
        e_brew BOOL,
        badges_equipped INT,
        biz_type TEXT,
        biz_name TEXT,
        biz_level INT,
        biz_investment BIGINT,
        employees TEXT[],
        uniform TEXT,
        accessory TEXT,
        badges TEXT[]
        );'''
#employeesSetupSQL = '''
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
        uid BIGINT,
        money BIGINT,
        kfe_unlocked BOOL,
        ecce_unlocked BOOL,
        cwe_unlocked BOOL,
        dfe_unlocked BOOL,
        hfe_unlocked BOOL,
        ife_unlocked BOOL,
        lle_unlocked BOOL,
        mme_unlocked BOOL,
        rfe_unlocked BOOL,
        vion_unlocked BOOL,
        cenz_unlocked BOOL,
        leli_unlocked BOOL,
        aaro_unlocked BOOL,
        frey_unlocked BOOL,
        farm_unlocked BOOL,
        moth_unlocked BOOL,
        tori_unlocked BOOL,
        clem_unlocked BOOL,
        lach_unlocked BOOL,
        krab_unlocked BOOL,
        hors_unlocked BOOL,
        chas_unlocked BOOL,
        torr_unlocked BOOL,
        choe_unlocked BOOL,
        peon_unlocked BOOL,
        mich_unlocked BOOL,
        brut_unlocked BOOL,
        star_unlocked BOOL,
        aure_unlocked BOOL,
        grav_unlocked BOOL,
        lizb_unlocked BOOL,
        rune_unlocked BOOL,
        levy_unlocked BOOL,
        hawk_unlocked BOOL,
        brew_unlocked BOOL,
        kfe_stocks BIGINT,
        ecce_stocks BIGINT,
        cwe_stocks BIGINT,
        dfe_stocks BIGINT,
        hfe_stocks BIGINT,
        ife_stocks BIGINT,
        lle_stocks BIGINT,
        mme_stocks BIGINT,
        rfe_stocks BIGINT,
        vion_stocks BIGINT,
        cenz_stocks BIGINT,
        leli_stocks BIGINT,
        aaro_stocks BIGINT,
        frey_stocks BIGINT,
        farm_stocks BIGINT,
        moth_stocks BIGINT,
        tori_stocks BIGINT,
        clem_stocks BIGINT,
        lach_stocks BIGINT,
        krab_stocks BIGINT,
        hors_stocks BIGINT,
        chas_stocks BIGINT,
        torr_stocks BIGINT,
        choe_stocks BIGINT,
        peon_stocks BIGINT,
        mich_stocks BIGINT,
        brut_stocks BIGINT,
        star_stocks BIGINT,
        aure_stocks BIGINT,
        grav_stocks BIGINT,
        lizb_stocks BIGINT,
        rune_stocks BIGINT,
        levy_stocks BIGINT,
        hawk_stocks BIGINT,
        brew_stocks BIGINT
        );'''
newsSetupSQL = '''
    CREATE TABLE IF NOT EXISTS news (
        weekday TEXT,
        news_text TEXT,
        effect TEXT,
        stock TEXT
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

## Bot Setup ----------------------------------------------------------
#TODO token id
token = os.environ.get('DISCORD_BOT_TOKEN')
devID = int(os.environ.get('DEV_ID'))
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

## Commands ----------------------------------------------------------





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
    
@new.command()
@is_dev()
async def stock(ctx, stockID: str, slowGrow: int, fastGrow: int, slowDecay: int, fastDecay: int, stable: int, chaoticGrow: int, chaoticDecay: int, chaoticStable: int, chaos: int, *, stockName: str):
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
    startPhase = random.choices(stockPhases, weights=phaseWeights,k=1)[1]
    await db.execute('''INSERT INTO stocks VALUES ($1,$2,10000,$3,$4);''',stockID,stockName,startPhase,phaseWeights)

@test.command()
@is_dev()
async def list(ctx, slowGrow: int, fastGrow: int, slowDecay: int, fastDecay: int, stable: int, chaoticGrow: int, chaoticDecay: int, chaoticStable: int, chaos: int):
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


## Bot Setup & Activation ----------------------------------------------------------
asyncio.get_event_loop().run_until_complete(run())
bot.run(token)
