import requests
from bs4 import BeautifulSoup
import discord


with open('token', 'r') as file:
    token = file.read()

client = discord.Client()

@client.event
async def on_ready():
    print("Hi everyone! I'm {0.user} and I'm here to remind you how many time you wasted on League Of Legends <3".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$help'):
        await message.channel.send("To use me, simply type: $waste **Summoner's name**")

    if message.content.startswith('$waste'):
        arg = message.content.split()[1:]
        username = ' '.join(arg)
        username_prcs = ''.join(arg).lower()
        url = "https://wol.gg/stats/euw/" + username_prcs + '/'
        nb_days = nb_books = None
        r = requests.get(url)
        if r.status_code != 200:
            msg = ' '.join(['An error occured, please try again!\nURL:', url, '\nRequest status code :', str(r.status_code)])
        else :
            soup = BeautifulSoup(r.text, 'html.parser')
            if "An error has occured." in soup.h1:
                msg = 'An error occured, please try again!\nSummoner might not exist...'
            else:
                nb_days = soup.find(id = 'time-days').get_text()[:-4]
                nb_books = soup.find(id = 'fact-books').get_text()[0:-10]
                msg = ' '.join(['Wow', username + '!', 'You already wasted**', nb_days, '**days playing League of Legends! Instead, you could have read**', nb_books, '**books!'])
        await message.channel.send(msg)

client.run(token)
