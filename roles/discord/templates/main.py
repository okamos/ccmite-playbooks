import discord
import os
import time
import re

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        l = len(str(client.user.id)) + 5
        words = re.split('\s', message.content)
        print(words)
        if len(words[1]) >= 3 and len(words[1]) <= 16:
            c = client.get_channel(618319969163280404)
            await c.send("新規ユーザー(" + words[1] + ")への対応をしてください http://ccmite.com:8084/ccadmin/user.php?name=" + words[1])
            await message.channel.send("ありがとうございます :heart: ホワイトリスト追加までしばしお待ちください。")
        else:
            await message.channel.send("プロフィール名はアルファベットと数字、アンダースコアしか使えないよ")

@client.event
async def on_member_join(member):
    time.sleep(2)
    c = client.get_channel(608700399880503313)
    await c.send(member.name + "さん初めまして、 まずは <#611445694015995904>, <#611450466391556116> をご覧ください。その後に<@!659708908562022402>にプロフィール名を伝えてください")

client.run(os.environ['DISCORD_BOT_API_TOKEN'])
