import discord
from discord.ext import tasks, commands
from datetime import datetime
from dateutil import relativedelta
import json 
from dotenv import load_dotenv
import os 
load_dotenv()
"""
Requires discord token
"""
client = commands.Bot(command_prefix="!", help_command=None)

# Loop N check 
@tasks.loop(hours=24)
async def checkBirthday(dates):
    current_month, currently_day = datetime.now().month, datetime.now().day
    channel = await client.fetch_channel(905623171716243457) # Edit channel
    user = await client.fetch_user(466042357553430539) # Edit user id       
    for i in dates:
        m, d = dates[i].split("/")[1], dates[i].split("/")[2]
        d1, d2 = datetime(1, current_month, currently_day), datetime(1, int(m), int(d))
        time_difference = relativedelta.relativedelta(d1, d2)
        if int(m) == current_month and int(d) == currently_day: 
            await channel.send(f"{user.mention} Today is {i}'s birthday.")
        elif time_difference.months < 1 and time_difference.days > -11 and time_difference.days < 0: 
            await channel.send(f"{user.mention} {i}'s birthday is in {time_difference.days *-1} days.")


# Calendar 
class Calendar:
    def __init__(self) -> None:
        pass 

    def add_date(self, name, date):
        try:
            with open("dates.json", "r+") as f:
                data = json.load(f)
                data[name] = date
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return "Sucess"
        except Exception as e:
            return e

    
    def delete_date(self, name):
        try:
            with open("dates.json", "r+") as f:
                data = json.load(f)
                for i in data:
                    if i.lower() == name.lower():
                        del data[i]
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                        return "Sucess"
                return f"Error: Cannot find {name}"
        except Exception as e:
            return e
        
    
    def get_dates(self):
        with open("dates.json", "r+") as f:
            return json.load(f)


# Discord Command 
@client.command()
async def add(ctx, date, name):
    await ctx.reply(C.add_date(date, name))


@client.command()
async def delete(ctx, name): 
    await ctx.reply(C.delete_date(name))


@client.command()
async def file(ctx):
    await ctx.reply(content="JSON file", file=discord.File("dates.json"))


@client.event 
async def on_ready():
    print("logged in")



# Initiate 
token = os.environ["TOKEN"]
C = Calendar()
checkBirthday.start(C.get_dates())
client.run(token)
