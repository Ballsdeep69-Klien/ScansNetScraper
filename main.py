#imports
import discord
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from webserver import keep_alive
from io import BytesIO
import shutil

#variables
scraping = False
client = discord.Client()
commands = ["@datappting#0390", "!read", "<@887588197243170877>","!test","!add", "!full ","!raw"]

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
  print(key)
  if lim < 5:
    return redscrap(base, "Error")
  if(key == "asurascans"):
    output = scrapimgs(base,filename,3,1)
  elif(key == "flamescans"):
    output = scrapimgs(base,filename,1,6)
  elif(key == "reset-scans"):
    output = scrapreset(base,filename)
  elif(key == "kumascans"):
    output = scrapimgs(base,filename,1,19)
  else:
    output = scrapimgs(base,filename,1,0)
  return output

def scrapimgs(base, filename,start,end):
    soup = BeautifulSoup(requests.get(base).text, 'html.parser')
    imgs = soup.find_all("img")
    lim = int(len(imgs))-end
    output = []
    print("scraping")
    for i in range(start,lim):
        imageurl = imgs[i]["src"]
        filename1 = filename+str(i)+"."+imageurl.split(".")[-1]
        im = Image.open(BytesIO(requests.get(imageurl).content))
        width, height = im.size
        factor = 0.6
        if(height*factor<width):
          r = requests.get(imageurl, stream = True)
          if r.status_code == 200:
              # Set decode_content value to True, otherwise the   downloaded image file's size will be zero.
              r.raw.decode_content = True
    
              # Open a local file with wb ( write binary ) permission.
              with open(filename1,'wb') as f:
                  shutil.copyfileobj(r.raw, f)
                  print('Image sucessfully Downloaded: ',filename1)
                  output.append(filename1)
        else:
          for j in range(int(height/width/factor)):
            name = filename1.split(".")[0]+"p"+str(int(j+1))+"."+imageurl.split(".")[-1]
            print(name)
            im1 = im.crop((0, j*width*factor, width, (j+1)  *width*factor))
            im1.save(name)
            output.append(name)
          j = height/width/factor
          im = im.crop((0, int(width*factor*int(j)), width, height))
          name = filename1.split(".")[0]+"p"+str(int(j+1))+"."+imageurl.split(".")[-1]
          print(name)
          im.save(name)
          output.append(name)
    print(output)
    return output

def scrapflame(base, filename,):
    soup = BeautifulSoup(requests.get(base).text, 'html.parser')
    imgs = soup.find_all("img")
    lim = int(len(imgs))-7
    output = []
    imageurl = imgs[1]["src"]
    r = requests.get(imageurl, stream=True)
    filename1 = filename+"1"+"."+imageurl.split(".")[-1]
    if r.status_code == 200:
      with open(filename1, 'wb') as f:
          r.raw.decode_content = True
          shutil.copyfileobj(r.raw, f)
          print("downloaded" + filename1)
      output.append(filename1)
    else:
      print('Failed')
    for i in range(2,lim):
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







# on start, say bot is online
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  
#on message
@client.event
async def on_message(message):
  #global variables
  global links
  global scraping
  keysCh = client.get_channel(892629646284296213)
  summoned = False
  #ping pong function
  if client.user.mentioned_in(message):
    summoned = True
    await message.channel.send("Pong!")
    return

  #don't read bot messages
  if(message.author == client.user):
    return

  #is it being summoned?
  for i in commands:
    if(message.content.startswith(i)):
      summoned = True
  if (summoned == False):
    return

  #new channel create function
  if(message.content.startswith("!read new ")):
    await message.guild.create_text_channel(message.content[9:],category=message.channel.category)
    return
  if(message.content.startswith("!add ")):
    link = message.content.split(" ")[-1]
    abr = message.content[5:-len(message.content.split(" ")[-1])-1]
    name = link.split("/")[3].split("-")[0]
    for i in range(1,len(link.split("/")[3].split("-"))-2):
      name += " "+link.split("/")[3].split("-")[i]
    link = link[0:-len(link.split("-")[-1])]
    scans = link.split("/")[2].split(".")[-2]
    file = open("Keys/Key.txt","a")
    key.append([abr,name,link,scans])
    file.write(str("\n"+abr+","+name+","+link+","+scans))
    file.close()
    await keysCh.send(abr+" - "+name+" (from "+scans+")")
    return


  #key specific functions
  for i in key:
    if(message.content.startswith("!full "+i[0])):
      await message.channel.send(i[1])
    if(message.content.startswith("!read "+i[0])):
      tempurl = message.content[7+len(i[0]):]
      x = await message.channel.send(i[2]+tempurl+"/")
      # await mainChannel.send(x.jump_url)
      for j in links:
        if(i[0] == j[0] and message.content[7+len(i[0]):] == j[1] ):
            embed=discord.Embed(title=i[0]+" ch:"+j[1], url=j[2], description="Read: "+i[1]+"\nChapter: "+j[1]+" \n [Read now]("+j[2]+")")
            await message.channel.send(embed = embed)
            return
      if(scraping == True):   #don't scrap if already scraping
        await message.channel.send("currently unavailable")
        return

      #start scraping
      await x.pin() 
      scraping = True
      urls = redscrap(i[2]+tempurl+"/","Data/"+i[0]+tempurl+"p",i[3])

      #update links
      file = open("Keys/links.txt", "a")
      links.append([i[0],message.content[7+len(i[0]):],x.jump_url])
      file.write("\n"+i[0]+","+message.content[7+len(i[0]):]+","+"https://discord.com/channels/"+str(x.guild.id)+"/"+str(x.channel.id)+"/"+str(x.id))
      file.close()

      #allow other scraping and send files
      scraping = False
      for j in urls:
        await message.channel.send(file=discord.File(j))
        os.remove(j)
      embed=discord.Embed(title=i[0]+" ch:"+message.content[7+len(i[0]):], url=x.jump_url, description="Read: "+i[1]+"\nChapter: "+message.content[7+len(i[0]):]+" \n [Read now]("+x.jump_url+")")
      await message.channel.send(embed = embed)
      return
    if(message.content.startswith("!test "+i[0])):
      print("test")


keep_alive()
client.run(os.getenv("token"))
