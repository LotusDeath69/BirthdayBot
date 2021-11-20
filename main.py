import discord
from discord.ext import tasks, commands
from datetime import datetime, timezone, timedelta
from dateutil import relativedelta
import json 
from dotenv import load_dotenv
import os 
from datebase import * 
load_dotenv()
"""
Requires discord token
"""
client = commands.Bot(command_prefix="!")

# Loop N check 
@tasks.loop(hours=24)
async def checkBirthday(dates):
    # Get current year, month, date
    current_date = datetime.now(timezone(timedelta(hours=-5)))
    current_month, currently_day, current_year = current_date.month, current_date.day, current_date.year

    # Add check birthday action to log 
    L.add_log(f"{current_year}/{current_month}/{currently_day}", "Check birthday")

    # Get channel and user 
    channel = await client.fetch_channel(905623171716243457) # Edit channel
    user = await client.fetch_user(466042357553430539) # Edit user id       

    # Check if any birthdays is within 10 days of the current date; notify user in the channel if so 
    for i in dates:
        m, d = dates[i].split("/")[1], dates[i].split("/")[2]
        d1, d2 = datetime(1, current_month, currently_day), datetime(1, int(m), int(d))
        time_difference = relativedelta.relativedelta(d1, d2)
        if int(m) == current_month and int(d) == currently_day: 
            await channel.send(f"{user.mention} Today is {i}'s birthday.")
        elif time_difference.months == 0 and time_difference.days > -11 and time_difference.days < 0: 
            await channel.send(f"{user.mention} {i}'s birthday is in {time_difference.days *-1} days.")


# Calendar 
class Calendar:
    def __init__(self, file_location):
        self.file = file_location


    def add_date(self, name, date):
        try:
            with open(self.file, "r+") as f:
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
            with open(self.file, "r+") as f:
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
        with open(self.file, "r+") as f:
            return json.load(f)

    
    def format_dates(self, dates): 
        text = "```\nBirthdays:\n"
        for i in dates.keys():
            text += f"{i}: {dates[i]}\n"
        text += "```"
        return text


class Log:
    def add_log(self, date, action):
        try:
            logAdd(date, action, "logs")
            closeConnection()
        except Exception as e:
            return e 


    def get_logs(self):
        return logRetrive()


    def format_logs(self, logs):
        text = "```\nDate: Action\n"
        n = len(list(logs))
        if n > 20:
            n = 20
        for i in list(logs)[::-1][:n]:
            text += f"{i[0]}: {i[1]}\n"
        text += "```"
        return text


    def current_date(self):
        date = datetime.now(timezone(timedelta(hours=-5)))
        return f"{date.year}/{date.month}/{date.day}"


# Discord Command 
@client.command()
async def add(ctx, date, name):
    L.add_log(L.current_date(), f"Add {name}")
    await ctx.reply(C.add_date(date, name))


@client.command()
async def delete(ctx, name): 
    L.add_log(L.current_date(), f"Delete {name}")
    await ctx.reply(C.delete_date(name))


@client.command()
async def file(ctx):
    await ctx.reply(content="JSON file", file=discord.File("dates.json"))


@client.command()
async def dates(ctx):
    await ctx.reply(C.format_dates(C.get_dates()))


@client.command()
async def logs(ctx):
    await ctx.reply(L.format_logs(L.get_logs()))


@client.command()
async def src(ctx):
    await ctx.reply("https://github.com/LotusDeath69/BirthdayBot")


@client.event 
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="people's birthday"))
    print("DISCORD commands:\n!add <name> <date> (yyyy/mm/dd) format - example: !add Test 2006/1/1\n!delete <name> - example: !delete Test\n!file")
    print("bot logged in")


# @client.command()
# async def test(ctx, *args):
#     L.add_log("test", "test")


# Initiate 
token = os.environ["TOKEN"]
C = Calendar("dates.json")
L = Log()
checkBirthday.start(C.get_dates())
client.run(token)