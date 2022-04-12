import discord
import os
from keep_alive import keep_alive
import image_creator
# from discord.ext import tasks
import asyncio
import time
client = discord.Client()

async def send_stats(channel_id):
  await image_creator.api_request()
  date = image_creator.draw_stats()
  embedVar = discord.Embed(title="Sprawozdanie z COVID-19", description="Poniższe statystyki zawierają dane odnośnie ilości przypadków COVID-19 w Polsce jak i ilości wykonanych testów.", color=0x4c73b1)
  file = discord.File("stats.png", filename="stats.png")
  embedVar.set_image(url="attachment://stats.png")
  embedVar.add_field(name="Dane z dnia:", value=date, inline=False)
  embedVar.set_author(name="Kubx0404",icon_url="https://media.discordapp.net/attachments/939546516052389908/939546556607135744/Steam_Awatar.png?width=671&height=671")
  await client.get_channel(channel_id).send(file=file, embed=embedVar)

async def send_stats_without_request(channel_id):
  date = image_creator.draw_stats()
  embedVar = discord.Embed(title="Sprawozdanie z COVID-19", description="Poniższe statystyki zawierają dane odnośnie ilości przypadków COVID-19 w Polsce jak i ilości wykonanych testów.", color=0x4c73b1)
  file = discord.File("stats.png", filename="stats.png")
  embedVar.set_image(url="attachment://stats.png")
  embedVar.add_field(name="Dane z dnia:", value=date, inline=False)
  embedVar.set_author(name="Kubx0404",icon_url="https://media.discordapp.net/attachments/939546516052389908/939546556607135744/Steam_Awatar.png?width=671&height=671")
  await client.get_channel(channel_id).send(file=file, embed=embedVar)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$photo'):
    image_creator.draw_stats()
    await message.channel.send(file=discord.File('stats.png'))
    
  if msg.startswith('$stats'):
    await send_stats_without_request(message.channel.id)


# async def check_time():
#   time_object = time.gmtime()
#   utc_time = time.strftime("%H:%M", time_object)
#   if utc_time == "10:00":
#     await send_stats(938934504003883029)
#     await send_stats_without_request(941834684185317386)

# async def while_fun():
#   await client.wait_until_ready()
#   while True:
#     await check_time()
#     await asyncio.sleep(60)
# client.loop.create_task(while_fun())


my_secret = os.environ['TOKEN']

keep_alive()
client.run(my_secret)