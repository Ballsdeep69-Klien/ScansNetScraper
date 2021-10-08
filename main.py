import discord
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

client = discord.Client()
commands = ["@datappting#0390", "!read", "<@887588197243170877>","!test","!add", "!full"]

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

def redscrap(base, filename,key):
  print(filename)
  soup = BeautifulSoup(requests.get(base).text, 'html.parser')
  lim = int(len(soup.find_all("img")))
  if lim < 5:
    return redscrap(base, "Error")
  if(key == "a"):
    output = scrap5img(base,filename,3,1)
  elif(key == "f"):
    output = scrap5img(base,filename,1,1)
  else:
    output = scrap5img(base,filename)
  return output

def scrap5img(base, filename,start,end):
    soup = BeautifulSoup(requests.get(base).text, 'html.parser')
    imgs = soup.find_all("img")
    lim = int(len(imgs))-end
    output = []
    links.append([filename])
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
    file = open("Keys/links.txt", "a")
    file.write("\n"+filename)
    file.close()
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
    if(message.content.startswith(i)):
      await mainChannel.send("Bot was summoned")
      summoned = True
  if(message.author == client.user):
    if(message.attachments == []):
      return
    else:
      file = open("Keys/links.txt", "a")
      file.write(","+str(message.attachments[-1]))
      file.close()
      links[-1].append(str(message.attachments[-1]))
      
  if summoned == False:
    return
  
  for i in key:
    if(message.content.startswith("!full "+i[0])):
      await message.channel.send(i[1])
    if(message.content.startswith("!read "+i[0])):
      msg = await message.channel.send(i[2]+message.content[10:]+"/")
      await msg.pin()
      for j in links:
        if("Data/"+i[0]+message.content[7+len(i[0]):]+"p" == j[0]):
          for inti in j[1:]:
            await message.channel.send(inti)
          # for inti in range(int(len(j[1:])/3)):
          #   await message.channel.send(j[3*inti] +" "+j[3*inti+1]+" "+j[3*inti+2])
          # for inti in range(len(j[1:])%3):
          #   await message.channel.send(j[-inti-1])
          return
      urls = redscrap(i[2]+message.content[10:]+"/","Data/"+i[0]+message.content[10:]+"p",i[3])
      for i in urls:
        await message.channel.send(file=discord.File(i))
        os.remove(i)
    if(message.content.startswith("!test "+i[0])):
      print(links)
      # await message.channel.send(i[2]+message.content[10:]+"/")
      # urls = scrap5img(i[2]+message.content[10:]+"/","Data/"+i[0]+message.content[10:]+"p")
      # for i in urls:
      #   await message.channel.send(file=discord.File(i))
  if(message.content.startswith("!read new")):
    await message.guild.create_text_channel(message.content[9:],category=message.category)
    return
  if(message.content.startswith("!add ")):
    mainChannel = client.get_channel(892629646284296213)
    x = message.content[5:]
    file = open("Keys/Key.txt", "a")
    file.write("\n"+x)
    file.close()
    x = x.split(',')
    key.append(x)
    await mainChannel.send(x[0]+" - "+x[1])




# keep_alive()
client.run(os.getenv("token"))

#https://flamescans.org/omniscient-readers-viewpoint-chapter-73/
#await create_text_channel(name, *, overwrites=None, category=None, reason=None, **options)






