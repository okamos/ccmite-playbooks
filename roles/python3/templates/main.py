import discord
import os
import time

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
        m = message.content[l:]
        if all(ord(r) < 128 for r in m) and len(m) >= 3 and len(m) <= 16:
            c = client.get_channel(618319969163280404)
            await c.send("新規ユーザー(" + m + ")への対応をしてください http://ccmite.com:8084/ccadmin/user.php?name=" + m)
            await message.channel.send("ありがとうございます :heart: ホワイトリスト追加までしばしお待ちください。")
        else:
            await message.channel.send("プロフィール名はアルファベットと数字、アンダースコアしか使えないよ")

@client.event
async def on_member_join(member):
    time.sleep(2)
    c = client.get_channel(608700399880503313)
    await c.send(member.name + "さん初めまして、 まずは <#611445694015995904>, <#611450466391556116> をご覧ください。その後に<@!659708908562022402>にプロフィール名を伝えてください")

client.run(os.environ['DISCORD_BOT_API_TOKEN'])
