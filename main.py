import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import aiohttp
from datetime import datetime as d
import json
with open('config.json', 'r') as config_file:
	config = json.loads(config_file.read())

connection = MongoClient(config['mongodb'])
db = connection['Pylon']
keys = db['keys']

bot = commands.Bot(command_prefix= commands.when_mentioned_or('p.', 'p!'), description="Get stats about your Pylon script", case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('-----------------------------')
    print(f'Logged in as {bot.user.name}')
    print('-----------------------------')

@bot.command()
async def key(ctx, key:str=None):
    if key:
        if keys.find_one({'_id': ctx.author.id}) is not None:
            keys.update_one({'_id': ctx.author.id}, {'$set': {'key': key}})
        else:
            keys.insert_one({'_id': ctx.author.id, 'key': key})
        await ctx.send(f'Successfully updated your Pylon api key to `{key}`')
    else:
        active_key = keys.find_one({'_id': ctx.author.id})
        if not active_key is None:
            return await ctx.send(f'Your current registered api key is `{active_key}`')
        await ctx.send('You don\'t have a key registered! For an instruction how to find your api key, use `p.find_key`')

@bot.command()
async def find_key(ctx):
    embed=discord.Embed.from_dict({
        'title': 'How to get your Pylon api token',
        'description': '1) Open [pylon.bot](https://pylon.bot) in **google crome**\n\n2) Go into any script\n\n3) Active the crome developer console as described [here](https://developers.google.com/web/tools/chrome-devtools) \n\n4) Click on "Network" and then "XHR" and find a document that is named "user"\n\n5) Find your tkey after "authorisation"\n\n6) Now save your key on this bot with `p.key <key>`',
        'image': {'url':'https://cdn.discordapp.com/attachments/757169610599694356/816475908742447114/unknown.png'},
        'color': 0x426BE4
    })
    await ctx.send(embed=embed)
	
@bot.command()
async def invite(ctx): 
    embed=discord.Embed.from_dict({
        'title': 'Invite link',
        'description': 'Invite Pylon-stats [here](https://discord.com/oauth2/authorize?client_id=816460731654209596&scope=bot&permissions=0)',
        'thumbnail': {'url':'https://cdn.discordapp.com/attachments/757169610599694356/816654906462830622/Pylon_bug.png'},
        'color': 0x426BE4
    })
    await ctx.send(embed=embed)

@bot.command()
async def endpoints(ctx):
    embed=discord.Embed.from_dict({
        'title': 'Pylon API endpoints',
        'description': '**GET**\n\n`/api/deployments/:deployment_id` returns the current code on the script specified\n\n`/api/guilds/:guild_id` returns some normal guild info along with active cron tasks\n\n`/api/guilds/:guild_id/stats` returns the stats about the guild you can see with `p.stats`\n\n`/api/user` returns some very small info about the user assosiated with the key\n\n`/api/user/guilds` returns the guilds the user has access to with Pylon\n\n**POST**\n\n`/api/deployments/:deployment_id` Saves and publishes the script you send with it. :warning: **CAREFUL**, you could delete all your scripts with this, make sure you test on a testing server first\n\n\nIf you\'d like to create more commands to endpoints to this bot feel free to make a Pull Request [here](https://github.com/Kile/Pylon-stats)',
        'thumbnail': {'url':'https://cdn.discordapp.com/attachments/757169610599694356/816638492603580426/pylon_cloud.png'},
        'color': 0x426BE4
    })
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed.from_dict({
        'title': 'Pylon-stats commands',
        'description': '`p.find_key` explains how to find your Pylon api key\n\n`p.key <key>` saves your key\n\n`p.stats <optional_server_id>` Gives you Pylon stats about the given server provided you have permission\n\n`p.help` Displays this message\n\n`p.endpoints` Shows the Pylon API endpoints\n\n`p.info` Get some infos about this bot',
        'color': 0x426BE4,
        'thumbnail': {'url': 'https://cdn.discordapp.com/avatars/816460731654209596/00beaa4c6b5d09fb498b8bb02bce9762.png?size=1024'}
    })
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed=discord.Embed.from_dict({
        'title': 'Pylon-stats info',
        'description': 'This bot uses the Pylon API to get infos about some Pylon stats on a server Pylon is on. It also provides recources to create your own api calls by giving you a list of endpoints with `p.endpoints`. Sadly this is not possible to do in the Pylon editor because Pylon blocks `fetch` requests to it\'s own API. Please contribute to improve functionaility of this bot [here](https://github.com/kile/pylon-stats)',
        'color': 0x426BE4,
        'thumbnail': {'url': 'https://cdn.discordapp.com/avatars/816460731654209596/00beaa4c6b5d09fb498b8bb02bce9762.png?size=1024'}
    })
    await ctx.send(embed=embed)

@bot.command()
async def stats(ctx, guild_id:int=None):
    if guild_id is None:
        try:
            guild_id = ctx.guild.id
        except:
            return await ctx.send('You either need to provide a guild id or use this command in a guild!')
    
    key = keys.find_one({'_id': ctx.author.id})
    if key is None:
        return await ctx.send('No key registered yet! Register a key with `p.key <key>`. If you don\'t know where to get your key, use `p.find_key` for an instruction')
    session = aiohttp.ClientSession()
    headers = {'accept': '*/*',
    "accept": "/",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "authorization": f"{key['key']}",
    "content-type": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
    }
    body = None

    response = ''
    async with session.get(f'https://pylon.bot/api/guilds/{guild_id}/stats', headers=headers, json=body) as r:
        if not r.status == 200:
            error = await r.text()

            embed = discord.Embed.from_dict({
                'title': 'An error occured while handeling your request',
                'description': str(error) + '\n\n(Check if your key is valid)',
                'color': 0xFF0000
            })
            await ctx.send(embed=embed)
            await session.close()

        response = await r.json()
    results = response[len(response)-1]
    embed=discord.Embed.from_dict({
        'title': f'Pylon scrip stats on guild {guild_id}',
        'description': f"**Data from:** {d.fromtimestamp(results['date']).strftime('%b %d %Y %H:%M:%S')}\n\n**CPU time:** {results['cpuMs']} ms\n**Execution time:** {results['executionMs']} ms\n**Host function calls:** {results['hostFunctionCalls']}\n**Fetch requests:** {results['fetchRequests']}\n**KV operations:** {results['kvOperations']}\n**Discord cache requests:** {results['discordCacheRequests']}\n**Discord api requests:** {results['discordApiRequests']}\n**Events:** {results['events']}\n**Average cpu time:** {results['cpuMsAvg']} ms\n**Average execution time:** {results['executionMsAvg']} ms",
        'color':0x426BE4,
        'thumbnail': {'url':'https://cdn.discordapp.com/attachments/757169610599694356/816638492603580426/pylon_cloud.png'}
    })
    await ctx.send(embed=embed)
    await session.close()

bot.load_extension('jishaku')
bot.run(config['token'])
