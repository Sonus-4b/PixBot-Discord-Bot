import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready(): # event handler (create another @client.event to check for a new event)
    print(f'{bot.user} has connected to Discord!')

@bot.command(name = 'pull')
async def pull_img(ctx, img):
    file_list = drive.ListFile({'q': f"title contains '{img}' and trashed=false"}).GetList()
    file_id = file_list[0]['id']  # get the file ID
    file = drive.CreateFile({'id': file_id})
    file_name = f'{img}.png'
    file.GetContentFile(file_name)
    await ctx.send(file=discord.File(file_name))

@bot.command(name = 'add')
async def add_image(ctx, img):
    await save(img)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)