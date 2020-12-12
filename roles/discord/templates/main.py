import os
import time
import re
import unicodedata
import json
import struct
import socket
import urllib.request
import discord
from discord.ext import tasks

client = discord.Client()
host = 'ccmite.com'


def unpack_varint(s):
    d = 0
    for i in range(5):
        b = ord(s.recv(1))
        d |= (b & 0x7F) << 7*i
        if not b & 0x80:
            break
    return d


def pack_varint(d):
    o = bytearray()
    while True:
        b = d & 0x7F
        d >>= 7
        o += struct.pack("B", b | (0x80 if d > 0 else 0))
        if d == 0:
            break
    return o


def pack_data(d):
    return pack_varint(len(d)) + d


def pack_port(i):
    return struct.pack('>H', i)


statusMsg = "%s %sが%sしました"
webdown = False
mcdown = False


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        for w in re.split(r'\s', message.content):
            if w.find(str(client.user.id)) >= 0:
                continue
            if len(w) == 0:
                continue
            nonNa = False
            for c in w:
                if unicodedata.east_asian_width(c) != 'Na':
                    nonNa = True
                    break
            if nonNa:
                continue
            if len(w) >= 3 and len(w) <= 16:
                c = client.get_channel(618319969163280404)
                await c.send(
                        "新規ユーザー(" + w +
                        ")への対応をしてください " +
                        "http://ccmite.com:8084/ccadmin/user.php?name=" + w)
                await message.channel.send(
                        "ありがとうございます" + message.author.name +
                        "さん :heart: ホワイトリスト追加までしばしお待ちください。")
            else:
                await message.channel.send("プロフィール名はアルファベットと数字、アンダースコアしか使えないよ")


@client.event
async def on_member_join(member):
    time.sleep(2)
    c = client.get_channel(608700399880503313)
    await c.send(
            member.name +
            "さん初めまして、 まずは <#611445694015995904>, <#611450466391556116> " +
            "をご覧ください。その後に<@!659708908562022402>にプロフィール名を伝えてください")

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

    req = urllib.request.Request('{}?{}'.format(
        url, urllib.parse.urlencode(params)))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer {}'.format(
        os.environ.get('TWITTER_ACCESS_TOKEN')))
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


@tasks.loop(seconds=60)
async def webLoop():
    global webdown
    c = client.get_channel(726728923315961937)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        try:
            s.connect((host, 80))
            req = 'GET / HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\n\r\n' % (host)
            s.send(req.encode('utf-8'))
            res = s.recv(15).decode('utf-8')
            s.close()
            if res == 'HTTP/1.1 200 OK':
                if webdown is True:
                    await c.send(statusMsg % (
                        ":white_check_mark:", "ウェブサーバー", "復帰"))
                webdown = False
            else:
                if webdown is False:
                    await c.send(statusMsg % (":x:", "ウェブサーバー", "ダウン"))
                webdown = True
        except socket.error:
            if webdown is False:
                await c.send(statusMsg % (":x:", "ウェブサーバー", "ダウン"))
            webdown = True


@tasks.loop(seconds=60)
async def mcLoop():
    global mcdown
    c = client.get_channel(726728923315961937)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        try:
            s.connect((host, 25565))
            s.send(pack_data(
                bytes("\x00\x00".encode('utf-8')) +
                pack_data(bytes(host.encode('utf-8'))) +
                pack_port(25565) + bytes("\x01".encode('utf-8'))))
            s.send(pack_data(bytes("\x00".encode('utf-8'))))

            unpack_varint(s)  # Packet length
            unpack_varint(s)  # Packet ID
            unpacked = unpack_varint(s)  # String length

            d = bytearray()
            while len(d) < unpacked:
                d += s.recv(1024)

            s.close()
            json.loads(d.decode('utf-8'))
            if mcdown is True:
                await c.send(statusMsg % (
                    ":white_check_mark:", "マインクラフトサーバー", "復帰"))
            mcdown = False
        except ValueError:
            if mcdown is False:
                await c.send(statusMsg % (":x:", "マインクラフトサーバー", "ダウン"))
            mcdown = True
        except socket.error:
            if mcdown is False:
                await c.send(statusMsg % (":x:", "マインクラフトサーバー", "ダウン"))
            mcdown = True


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    loop.start()
    webLoop.start()
    mcLoop.start()

client.run(os.environ['DISCORD_BOT_API_TOKEN'])
