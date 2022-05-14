# ______ ___________ _____ _      _____ _____ _____ 
# | ___ \____ |  _  \  ___| |    |  ___|_   _|  ___|
# | |_/ /   / / | | | |__ | |    | |__   | | | |__ 
# |    /    \ \ | | |  __|| |    |  __|  | | |  __|
# | |\ \.___/ / |/ /| |___| |____| |___  | | | |___
# \_| \_\____/|___/ \____/\_____/\____/  \_/ \____/

import os
import discord 
import datetime
from discord.ext import commands

import mysql.connector

token = "..." #discord bot tokeninizi girin

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), intents=intents)

@client.event
async def on_ready():
    print(f'The bot logged in as, {client.user}')

@client.event 
async def on_message(message):
    if message.content.startswith('gimmesql') and str(message.author.id) == '931766021902180382': #kendi discord idni gir
        await message.channel.send(' veritabanına ait yedek çıkarılıyor...')
        con = mysql.connector.connect(host='localhost', user='root', passwd='...', db='...')
        cur = con.cursor()

        cur.execute("SHOW TABLES")
        data = ""
        tables = []
        for table in cur.fetchall():
            tables.append(table[0])

        for table in tables:
            data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

            cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
            data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

            cur.execute("SELECT * FROM `" + str(table) + "`;")
            for row in cur.fetchall():
                data += "INSERT INTO `" + str(table) + "` VALUES("
                first = True
                for field in row:
                    if not first:
                        data += ', '
                    data += '"' + str(field) + '"'
                    first = False


                data += ");\n"
            data += "\n\n"

        now = datetime.datetime.now()
        filename = str("/backup_" + now.strftime("%Y-%m-%d_%H:%M") + ".sql")

        if not os.path.exists(filename):
            with open(filename, 'w'): pass

        FILE = open(filename,"w")
        FILE.writelines(data)
        FILE.close()
        await message.author.send(' veritabanı yedeğiniz', file=discord.File(filename))

client.run(token)
