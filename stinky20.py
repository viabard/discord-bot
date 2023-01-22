from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

import bs4, requests, time, random
import subprocess
import qrcode, qrcode.image.svg
import cairosvg
import asyncio


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print("stinky 2.0 is ready for ascention")

@bot.command()
async def ascii(ctx, num_col="90", mode="simple"):
    """
    -ascii [columns] [mode (simple/complex)]
    example: -ascii 25 complex
    """
    print(f"ascii called by '{ctx.message.author.name}' on '{time.asctime()}'")
    #print(ctx.message.content)
    if len(ctx.message.attachments) > 0:
        await ctx.message.attachments[0].save("./ASCII-generator/temp.png")
        if len(ctx.message.content.split(' ')) != 1:
            os.chdir("./ASCII-generator")
            output = subprocess.run(["python3", "img2txt.py", "--input", "temp.png", "--num_cols" ,num_col, "--mode", mode])
            os.chdir("..")
            if output.returncode == 0:
                mes = await ctx.send(f"**{ctx.message.author.name}** here's ur {ctx.message.attachments[0].filename}")
                with open("./ASCII-generator/data/output.txt", 'r') as f:
                    fi = f.read()
                try:
                    await ctx.send(f"```{fi}```")
                except:
                    await discord.Message.delete(ctx.message)
                    await mes.edit(content=f"**{ctx.message.author.name}** the text was too big to send...")
            else:
                await ctx.send(f"**{ctx.message.author.name}** something went wrong, try again - look at -help ascii")
        else:
            tries = 0
            while True:
                if tries >= 10:
                    await discord.Message.delete(ctx.message)
                    await ctx.send(f"**{ctx.message.author.name}**, I tried 90 to 40 for column size and that was still too big to send (you should try a smaller column size manually...)")
                os.chdir("./ASCII-generator")
                output = subprocess.run(["python3", "img2txt.py", "--input", "temp.png", "--num_cols" ,num_col, "--mode", mode])
                os.chdir("..")
                with open("./ASCII-generator/data/output.txt", 'r') as f:
                    fi = f.read()
                if len(f"```{fi}```") > 2000:
                    tries += 1
                    num_col = str(int(num_col) - 5)
                    continue
                else:
                    await ctx.send(f"```{fi}```")
                    break
    else:
        await ctx.send("Attach an image to a *-ascii* message")


@bot.command()
async def sus(ctx):
    print(f"sus called by '{ctx.message.author.name}' on '{time.asctime()}'")
    if ctx.message.author.voice != None:
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        #print(voice, dir(voice))
        if voice == None:
            vc= await channel.connect()
            vc.play(discord.FFmpegPCMAudio("sus" + str(random.randrange(3) + 1)+ ".mp3"))
            while vc.is_playing():
                await asyncio.sleep(1)
            # disconnect after the player has finished
            vc.stop()
            await vc.disconnect()
        else:
            await ctx.send("Already being sussy ")
    else:
        await ctx.send("Ur not in voice... kinda sussy...")


@bot.command()
async def lol(ctx):
    print(f"lol called by '{ctx.message.author.name}' on '{time.asctime()}'")
    if ctx.message.author.voice != None:
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        #print(voice, dir(voice))
        if voice == None:
            vc= await channel.connect()
            vc.play(discord.FFmpegPCMAudio("laugh" + str(random.randrange(2) + 1)+ ".mp3"))
            while vc.is_playing():
                await asyncio.sleep(1)
            # disconnect after the player has finished
            vc.stop()
            await vc.disconnect()
        else:
            await ctx.send("Already being SUPER FUNNY ")
    else:
        await ctx.send("Ur not in voice... kinda haha...")

@bot.command()
async def detect(ctx, message=None):
    """Attach an image to a -detect message..."""
    print(f"Detect called by '{ctx.message.author.name}' on '{time.asctime()}'")
    if len(ctx.message.attachments) > 0:
        await ctx.send("Detecting objects in **" + ctx.message.author.name + "**'s image...")
        #print(ctx.message.attachments[0])
        await ctx.message.attachments[0].save("detected.png")
        subprocess.run(["rm", "-r", "runs/detect/exp"])
        out = subprocess.run(["python3", "yolov5/detect.py", "--source", "detected.png", "--weights", "yolov5/weights/yolov5s_old.pt", "--conf", "0.25"], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
        out = out.stdout.decode("utf-8")
        out = out.split('\n')[-4]
        await discord.Message.delete(ctx.message)
        try:
            await ctx.send("**"+ctx.message.author.name + f"**'s image detected... **{str(' '.join(out.split(' ')[4:-2]))[:-1]}** *(no boxes == nothing/false negative)*",file=discord.File("runs/detect/exp/detected.png"))
        except:
            await ctx.send("**"+ctx.message.author.name + "**'s image was probably too large, couldn't send...")
    elif message!=None:
        message = str(message)
        if message.endswith(".png") or message.endswith(".jpg") or message.endswith(".jpeg") or message.endswith(".gif") and ' ' not in message:
            await ctx.send("```Getting image from " + message + "```")
            os.system("wget " + message + " -O detected.png")
            await ctx.send("Detecting objects in **" + ctx.message.author.name + "**'s image...")
            subprocess.run(["rm", "-r", "runs/detect/exp"])
            out = subprocess.run(["python3", "yolov5/detect.py", "--source", "detected.png", "--weights", "yolov5/weights/yolov5s_old.pt", "--conf", "0.25"], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
            print(out)
            if out.returncode == 0:
                out = out.stdout.decode("utf-8")
                out = out.split('\n')[-4]
                await discord.Message.delete(ctx.message)
                try:
                    await ctx.send("**"+ctx.message.author.name + f"**'s image detected... **{str(' '.join(out.split(' ')[4:-2]))[:-1]}** *(no boxes == nothing/false negative)*\nIf it isn't your image, the link was probably broken 🤔",file=discord.File("runs/detect/exp/detected.png"))
                except:
                    await ctx.send("**"+ctx.message.author.name + "**'s image was probably too large, couldn't send...")
            else:
                await ctx.send("**"+ctx.message.author.name + "** ur link probably doesn't exist smh")
        else:
            await ctx.send("Links must end with either .png .jpg .jpeg .gif")
    else:
        await ctx.send("Attach an image to a *-detect* message, or give a link to an image...")

@bot.command()
async def stinky(ctx):
    """
    uh oh
    """
    print(f"Stinky called by '{ctx.message.author.name}' on '{time.asctime()}'")
    await ctx.send("uh oh")

@bot.command(pass_context=True)
async def cowsay(ctx, message="You forgot to put a message in. Uhoh stinky, haha, funny poop, lallalalallala\nMake sure your message has quotes around it if there are spaces..."):
    """-cowsay "message here", a 'cow' says ur message
    """
    print(f"Cowsay called by '{ctx.message.author.name}' on '{time.asctime()}'")
    counter = -1
    for word in message.split(' '):
        if word.startswith('-'):
            counter += 1
    if counter >= len(message.split(' ')) - 1:
        await ctx.send('stop trying to break things')
    else:
        cows = [x for x in os.listdir("/home/pi/.cowsay") if x.endswith(".cow")]
        #print(cows)
        print(f"-f /home/pi/.cowsay/{random.choice(cows)}")
        options = {0: '', 1: "-b", 2: "-d", 3: "-g", 4: "-p", 5: "-s", 6: "-t", 7: "-w", 8: "-y", 9: f"/home/pi/.cowsay/{random.choice(cows)}"}
        r = random.randrange(9)+1
        if r == 9:
            output = subprocess.run(["cowsay", "-f", options.get(9), message], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
            output = output.stdout.decode("utf-8")
        else:
            output = subprocess.run(["cowsay", options.get(r), message], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
            output = output.stdout.decode("utf-8")
        try:
            await ctx.send("```"+output+"```")
        except:
            await ctx.send("Sorry, but the cow was too large for discord to handle... sadge")

@bot.command()
async def dsay(ctx, message="You forgot to put a message in. Uhoh stinky, haha, funny poop, lallalalallala\nMake sure your message has quotes around it if there are spaces..."):
    """-dsay "message here"
    """
    print(f"Dsay called by '{ctx.message.author.name}' on '{time.asctime()}'")
    output = subprocess.run(["cowsay", "-f", "dragon-and-cow", message], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    output = output.stdout.decode("utf-8")
    await ctx.send("```"+output+"```")

@bot.command()
async def fortune(ctx):
    """gives a fortune from a cow"""
    print(f"Fortune called by '{ctx.message.author.name}' on '{time.asctime()}'")
    fortune = subprocess.run(["fortune"], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    fortune = fortune.stdout.decode("utf-8")
    output = subprocess.run(["cowsay", fortune], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    output = output.stdout.decode("utf-8")
    await ctx.send("```"+output+"```")

@bot.command()
async def qr(ctx, message):
    """-qr "information here" """
    print(f"QR called by '{ctx.message.author.name}' on '{time.asctime()}'")
    await discord.Message.delete(ctx.message)
    img = qrcode.make(message, image_factory=qrcode.image.svg.SvgFillImage)
    img.save("temp.svg")
    cairosvg.svg2png(url="temp.svg", write_to="temp.png")
    await ctx.send(file=discord.File("temp.png"))

@bot.command()
async def roll(ctx):
    """
    -roll int (defulat 1 to 100)
    """
    print(f"Roll called by '{ctx.message.author.name}' on '{time.asctime()}'")
    message = ctx.message.content.split(' ')
    number = 0
    try:
        number = int(message[1])
        print(" they specified " + str(number) + ".")
    except:
        print(" they didn't specify.")
    if(number>0):
        await ctx.send("**" + ctx.message.author.name + "** rolled **" + str(random.randint(1, number)) + "** *(d" + str(number) + ")*")
    else:
        await ctx.send("**" + ctx.message.author.name+ "** rolled **" + str(random.randint(0,100)) +"**")



@bot.command()
async def diagonal(ctx):
    """
    -diagonal messagewithnospaces integer
    """
    print(f"Diagonal called by '{ctx.message.author.name}' on '{time.asctime()}'")
    try:
        m = ctx.message.content.split(' ')
        string = m[1]
        k = int(m[2])
        counter = 0
        switch = 1
        zigzags = []
        message = ""
        for i in range(k):
            zigzags.append("")

        if k == 1:
            await ctx.send("```" + string + "```")
        else:
            for i in range(len(string)):
                for j in range(k):
                    if (counter+j)/2 % (k-1) == counter%(k-1):
                        #print((i+j)/2 % (k-1))
                        zigzags[j] += string[i]
                    else:
                        zigzags[j] += ' '
                if switch == 1:
                    counter += 1
                else:
                    counter -= 1
                if counter % (k-1) == 0:
                    if switch == 1:
                        switch = 0
                    else:
                        switch = 1

            for i in range(k):
                if i == 0:
                    message += "```"
                message+=zigzags[i] + "\n"
            await ctx.send(message + "```")
    except:
        await ctx.send("```Usage: -diagonal messagewithnospaces integer\nExample: -diagonal hahafart 3```")


load_dotenv('token.env')
bot.run(os.environ["api_token"])