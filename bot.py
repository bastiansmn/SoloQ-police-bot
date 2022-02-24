import discord
from discord.ext import commands, tasks
import random
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv
import time
import sys
import os
from dotenv import load_dotenv

load_dotenv()

if len(sys.argv) == 1:  
    print("ERROR: Use python bot.py [day/week/two]")
    exit(1)

#VARIABLES
api_key = os.environ.get("RIOT_API_KEY") # here please put in-between the quotes your Riot API Developer Key
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'
current_time = int(time.time())
last = (current_time - 86400)
week = (current_time - 604800)
two = (current_time - 172800)

player_name = ['NVS Luiku', 'NVS BeIit', 'NVS Einard', 'NVS Anyone', 'NVS uden']

#PUUIDS ----------------------------------
def sync_puuid():
    top_id = watcher.summoner.by_name(my_region, player_name[0])["puuid"]
    jgl_id = watcher.summoner.by_name(my_region, player_name[1])["puuid"]
    mid_id = watcher.summoner.by_name(my_region, player_name[2])["puuid"]
    adc_id = watcher.summoner.by_name(my_region, player_name[3])["puuid"]
    sup_id = watcher.summoner.by_name(my_region, player_name[4])["puuid"]
    return [top_id, jgl_id, mid_id, adc_id, sup_id]

oplon = sync_puuid()


#CALCULS ----------------------------------
game_nbrs = []

# DAY COMMAND ----------------------------------
if sys.argv[1] == "day":
    topmh = list(watcher.match.matchlist_by_puuid(region, oplon[0], type="ranked", start_time=last, end_time=current_time, count=100))
    jglmh = list(watcher.match.matchlist_by_puuid(region, oplon[1], type="ranked", start_time=last, end_time=current_time, count=100))
    midmh = list(watcher.match.matchlist_by_puuid(region, oplon[2], type="ranked", start_time=last, end_time=current_time, count=100))
    adcmh = list(watcher.match.matchlist_by_puuid(region, oplon[3], type="ranked", start_time=last, end_time=current_time, count=100))
    supmh = list(watcher.match.matchlist_by_puuid(region, oplon[4], type="ranked", start_time=last, end_time=current_time, count=100))

# WEEK COMMAND ----------------------------------
if sys.argv[1] == "week":
    topmh = list(watcher.match.matchlist_by_puuid(region, oplon[0], type="ranked", start_time=week, end_time=current_time, count=100))
    jglmh = list(watcher.match.matchlist_by_puuid(region, oplon[1], type="ranked", start_time=week, end_time=current_time, count=100))
    midmh = list(watcher.match.malist_by_puuid(region, oplon[2], type="ranked", start_time=week, end_time=current_time, count=100))
    adcmh = list(watcher.match.matchlist_by_puuid(region, oplon[3], type="ranked", start_time=week, end_time=current_time, count=100))
    supmh = list(watcher.match.matchlist_by_puuid(region, oplon[4], type="ranked", start_time=week, end_time=current_time, count=100))

#LAST TWO DAYS COMMAND ----------------------------------
if sys.argv[1] == "two":
    topmh = list(watcher.match.matchlist_by_puuid(region, oplon[0], type="ranked", start_time=two, end_time=current_time, count=100))
    jglmh = list(watcher.match.matchlist_by_puuid(region, oplon[1], type="ranked", start_time=two, end_time=current_time, count=100))
    midmh = list(watcher.match.matchlist_by_puuid(region, oplon[2], type="ranked", start_time=two, end_time=current_time, count=100))
    adcmh = list(watcher.match.matchlist_by_puuid(region, oplon[3], type="ranked", start_time=two, end_time=current_time, count=100))
    supmh = list(watcher.match.matchlist_by_puuid(region, oplon[4], type="ranked", start_time=two, end_time=current_time, count=100))

# API DATAFRAME CREATION ----------------------------------
game_nbrs.append(len(topmh))
game_nbrs.append(len(jglmh))
game_nbrs.append(len(midmh))
game_nbrs.append(len(adcmh))
game_nbrs.append(len(supmh))

def get_string_of_period(string):
    if string == "day":
        return "24 dernières heures"
    if string == "week":
        return "7 derniers jours"
    if string == "two":
        return "2 derniers jours"

df = pd.DataFrame(
    {'Player': player_name,
    'phrase': "a joué **",
    'Games': game_nbrs,
    'last': f"** games de soloQ pendant les dernières {get_string_of_period(sys.argv[1])}",
})

print(df)

i = 0
df1 = df.loc[[i]]


#DISCORD BOT COMMANDS ----------------------------------
bot = commands.Bot(command_prefix = "!", description = "SoloQ Bot")

@bot.event
async def on_ready():
	print("Your soloQ bot is ready for use !")

@bot.command()
async def soloQ(ctx):
    oplon = sync_puuid()
    for i in range(5):
        df1 = df.loc[[i]]
        await ctx.send(df1.to_string(header=False, index=False))
        i = i + 1


bot.run(os.environ.get("BOT_TOKEN"))
