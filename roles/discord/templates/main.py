import os
import time
import re
import json
import urllib.request
import discord
from discord.ext import tasks

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

path = '/home/{{ ansible_user }}/.latest_tweet_id'
url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {
    'screen_name': 'ccmite',
    'count': 3,
}
@tasks.loop(seconds=60)
async def loop():
    latest = ''
    texts = []
    if os.path.isfile(path):
        with open(path) as f:
            latest = f.read()

    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer {}'.format(os.environ.get('TWITTER_ACCESS_TOKEN')))
    with urllib.request.urlopen(req) as res:
        tweets = json.loads(res.read())
        for t in tweets:
            # run to latest tweet
            if latest == str(t['id']):
                break
            if len(t['entities']['user_mentions']) == 0:
                texts.append(t['text'])
        latest = tweets[0]['id']

    c = client.get_channel(711961465493651516)
    if os.path.isfile(path):
        for t in texts:
            await c.send(t)

    with open(path, mode='w') as f:
        f.write(str(latest))

loop.start()
client.run(os.environ['DISCORD_BOT_API_TOKEN'])