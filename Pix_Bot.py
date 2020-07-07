import os
import random
import discord
from dotenv import load_dotenv
import pymongo
from discord.ext import commands

client = pymongo.MongoClient("mongodb+srv://Sonus:ComboWombo34@4b-dev-storage.exriz.gcp.mongodb.net/discord?retryWrites=true&w=majority")
db = client['discord']
collection = db["Pix-Bot Log"]


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready(): # event handler (create another @client.event to check for a new event)
    print(f'{bot.user} has connected to Discord!')


# retrieve an item command
@bot.command(name='pull')
async def art_pull(ctx, img):
    result = collection.find_one({"name" : img })
    if result == None:
        await ctx.send('Cannot find requested item')
    else:
        await ctx.send(result['link'])

# add a new item command
@bot.command(name = 'add')
async def art_add(ctx, img, fileName):
    post = {'name':img, 'link':fileName}
    collection.insert_one(post)
    await ctx.send('Image added')

# delete command
@bot.command(name = 'delete')
async def art_delete(ctx, img):
    result = collection.find_one({"name": img})
    if result == None:
        await ctx.send('Cannot find requested item')
    else:
        collection.delete_one(result)
        await ctx.send('Item deleted')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)