#imports
import discord
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
# from webserver import keep_alive
from io import BytesIO

#variables
client = discord.Client()
commands = ["@datappting#0390", "!read", "<@887588197243170877>","!test","!add"]

file = open("Keys/Key.txt", "r")
key = file.read().split("\n")
file.close()
file = key
key = []
for x in file:
  key.append(x.split(','))

file = open("Keys/links.txt", "r")
links = file.read().split("\n")
file.close()
file = links
links = []
for x in file:
  links.append(x.split(','))


#methods

def redscrap(base, filename,key):
  print(filename)
  soup = BeautifulSoup(requests.get(base).text, 'html.parser')
  lim = int(len(soup.find_all("img")))
  if lim < 5:
    return redscrap(base, "Error")
  if(key == "a"):
    output = scrapimgs(base,filename,3,1)
  elif(key == "f"):
    output = scrapimgs(base,filename,1,1)
  elif(key == "r"):
    output = scrapreset(base,filename)
  else:
    output = scrapimgs(base,filename,1,0)
  return output

def scrapimgs(base, filename,start,end):
    soup = BeautifulSoup(requests.get(base).text, 'html.parser')
    imgs = soup.find_all("img")
    lim = int(len(imgs))-end
    output = []
    for i in range(start,lim):
        imageurl = imgs[i]["src"]
        filename1 = filename+str(i)+"."+imageurl.split(".")[-1]
        im = Image.open(BytesIO(requests.get(imageurl).content))
        width, height = im.size
        factor = 0.6
        if(height*factor<width):
          output.append(filename1)
        else:
          for j in range(int(height/width/factor)):
            im1 = im.crop((0, j*width*factor, width, (j+1)  *width*factor))
            im1.save(filename1[0:-4]+"."+str(j)+".jpg")
            print("got image" + str(j))
            output.append(filename1[0:-4]+"."+str(j)+".jpg")
          j = height/width/factor
          im = im.crop((0, int(width*factor*int(j)), width, height))
          name = filename1[0:-4]+"."+str(int(j+1))+".jpg"
          im.save(name)
          output.append(name)
    return output
    # await message.channel.send(file=discord.File("Data/ORV55p1."+str(int(height/width))+".jpeg"))
    # return lim


def scrapreset(base, filename):
    soup = BeautifulSoup(requests.get(base).text, 'html.parser')
    imgs = soup.find_all("img")
    lim = int(len(imgs))
    output = []
    for i in range(1,lim):
        imageurl = imgs[i]["data-src"]
        filename1 = filename+str(i)+"."+imageurl.split(".")[-1]
        im = Image.open(BytesIO(requests.get(imageurl).content))
        width, height = im.size
        factor = 0.6
        if(height*factor<width):
          output.append(filename1)
        else:
          for j in range(int(height/width/factor)):
            im1 = im.crop((0, j*width*factor, width, (j+1)  *width*factor))
            im1.save(filename1[0:-4]+"."+str(j)+".jpg")
            print("got image" + str(j))
            output.append(filename1[0:-4]+"."+str(j)+".jpg")
          j = height/width/factor
          im = im.crop((0, int(width*factor*int(j)), width, height))
          name = filename1[0:-4]+"."+str(int(j+1))+".jpg"
          im.save(name)
          output.append(name)
    return output
























@client.event
async def on_ready():
  mainChannel = client.get_channel(889404717732601856)
  print("We have logged in as {0.user}".format(client))
  await mainChannel.send("Bot is once again online")
  

@client.event
async def on_message(message):
  mainChannel = client.get_channel(889404717732601856)
  summoned = False
  if client.user.mentioned_in(message):
    summoned = True
    await mainChannel.send("Bot was pinged")
    await message.channel.send("Pong!")

  for i in commands:
    # print(i)
    if(message.content.startswith(i)):
      # print(message)
      await mainChannel.send("Bot was summoned")
      summoned = True
  # print("message")
  if (summoned == False):
    return
  print()
  if(message.author == client.user):
    # print("part 1")
    return

  for i in key:
    if(message.content.startswith("!full "+i[0])):
      await message.channel.send(i[1])
    if(message.content.startswith("!read "+i[0])):
      await message.channel.send(i[2]+message.content[10:]+"/")
      for j in links:
        if("Data/"+i[0]+message.content[10:]+"p" == j):
          for inti in len(range(j[1:])/3):
            await message.channel.send(j[inti] +" "+j[inti+1]+" "+j[inti+3])
          for inti in len(range(j[1:])%3):
            await message.channel.send(j[-inti-1])
          return
      urls = redscrap(i[2]+message.content[10:]+"/","Data/"+i[0]+message.content[10:]+"p",i[3])
      for i in urls:
        await message.channel.send(file=discord.File(i))
        os.remove(i)
    if(message.content.startswith("!test "+i[0])):
      print("test")
  if(message.content.startswith("!read new")):
    await message.guild.create_text_channel(message.content[9:],category=message.category)


# keep_alive()
client.run(os.getenv("token"))

#https://flamescans.org/omniscient-readers-viewpoint-chapter-73/
#await create_text_channel(name, *, overwrites=None, category=None, reason=None, **options)






