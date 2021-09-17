import json
import discord
import requests as requests

client = discord.Client()

# tokenにトークンを入力
token = {
    "Authorization": "token"}
response = requests.get(
    "https://api.switch-bot.com/v1.0/devices", headers=token)
devices = json.loads(response.text)
# nameに温湿度計の名前を入力
device_id = [device['deviceId'] for device in devices['body']
             ['deviceList'] if "name" in device['deviceName']]
url = "https://api.switch-bot.com/v1.0/devices/" + device_id[0] + '/status'
response = requests.get(url, headers=token)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!tem'):
        response = requests.get(url, headers=token)
        tem = response.text[130:134]
        counter = 0
        tmp = await message.channel.send("温度:%s℃" % tem)
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!hum'):
        response = requests.get(url, headers=token)
        hum = response.text[113:115]
        counter = 0
        tmp = await message.channel.send("湿度:%s%%" % hum)
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

# tokenにDiscordのトークンを入力
client.run('token')
