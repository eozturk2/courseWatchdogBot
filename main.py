# bot.py
import discord
from ChromeDriverHandler import ChromeDriverHandler

BOT_TOKEN = "OTc4ODcwNTQ3MDc1MTgyNjQy.GJQXkS.Vh3iA02TqUZuVyzWDCf019My_voPTFmQkrrGNo"
BOT_GUILD = "Course Watchdog Mailer - Dev"

client = discord.Client()
courses = []
browser = ChromeDriverHandler()
start_ran = False


@client.event
async def on_ready():
    guild = None

    number = 0
    for guilde in client.guilds:
        if guilde.name == BOT_GUILD:
            guild = guilde
        number += 1

    if number <= 0:
        raise ConnectionError("Cannot connect to guild")
    if number > 1:
        raise ConnectionError("Bot is connected to more than one server!")

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    browser.initializeDriver()

    print("Successfully connected to VSB.")


@client.event
async def on_message(message):
    global courses

    if message.author == client.user:
        return

    if message.content == 'help':
        response = "Available (case-sensitive!) commands are:\n" \
                   "start ABCD 123,ABCD 124,ABCD 125 - loads courses into the system. (Does not activate scanning! " \
                   "You have to do that with one of the next commands!)\n" \
                   "all schedule - Searches VSB for all these courses at the same time, and makes a schedule for you " \
                   "with no conflicts and open seats\n" \
                   "single course - Searches VSB for these courses individually, and lets you know when a course is " \
                   "opened. Please note that this may result in conflicts.\n" \
                   "reset - Resets program to original state. After doing this, you will need to start over with " \
                   "entering courses.\n\n" \
                   "May the odds be ever in your favor..."

        await message.channel.send(response)

    if message.content[0:5] == "start":
        courses = message.content[6:].split(",")
        for course in courses:
            print(course)

    if message.content == "all schedule":
        x = await browser.allScheduleMode(courses, 'C:/Users/Eren/Desktop/')
        if x:
            await message.channel.send("The stars aligned and there is a schedule with all your wanted courses! "
                                       "Go register: https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")

        try:
            with open('C:/Users/Eren/Desktop/cap1.png', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        except Exception as e:
            print(str(e))
            await message.channel.send("Sorry, there was an error with sending the picture!")

        try:
            with open('C:/Users/Eren/Desktop/cap2.png', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        except Exception as e:
            print(str(e))
            await message.channel.send("Sorry, there was an error with sending the picture!")

    if message.content == "single course":
        call_count = await browser.singleCourseMode(courses, 'C:/Users/Eren/Desktop')

        for i in range(1, call_count + 1):
            with open('C:/Users/Eren/Desktop/cap' + str(i) + '_1.png', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
            with open('C:/Users/Eren/Desktop/cap' + str(i) + '_2.png', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)


client.run(BOT_TOKEN)
