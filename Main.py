import discord
import asyncio

__authors__ = ['RexRex600, electric-blue-green']

# Initialising the discord client
test = discord.Client()

# Opening the MuteList log
file = open('MuteList.txt', 'r')

# Processing the MuteList file and loading the mute list from the file
mute_list = []
mute_list = file.read().split(',')

# Initialising the list of commands and valid chats for command-based joining
commands = ['join', 'shutdown', 'leave', 'smashcapitalism', 'mute', 'unmute', 'lableme']
chats = ['rocketleague', 'menofwar', 'minecraft', 'paradox', 'politicalmachine', 'ksp', 'gta', 'civ']


# Logging client login details
@test.event
async def on_ready():
    print('Logged in as')
    print(test.user.name)
    print(test.user.id)
    print('------')


# Commands function
@test.event
async def on_message(message):
    # Invoking global variables
    global mute_list
    global file
    contents = message.content
    # Checking for the command character
    if contents[0] == '!':
        # Logging the command and the author for moderation purposes
        print("command: ", contents, "author: ", message.author)
        # Processing the command for parsing
        contents = contents[1::]
        contents = contents.split(' ')
        if contents[0] in commands:
            # Join channel command - adds role
            if contents[0] == 'join' and contents[1] in chats:
                role = message.server.roles
                for i in role:
                    if i.name == contents[1].lower():
                        await test.add_roles(message.author, i)
                await test.send_message(message.channel, message.author.name+' joined #'+contents[1])
            # Leave channel command - removes role
            elif contents[0] == 'leave' and contents[1] in chats:
                role = message.server.roles
                for i in role:
                    if i.name == contents[1].lower():
                        await test.remove_roles(message.author, i)
                await test.send_message(message.channel, message.author.name+' left #'+contents[1])
            # Generic text response command
            elif contents[0] == 'smashcapitalism':
                await test.send_message(message.channel, ':bomb: SMASH CAPITALISM :bomb:')
            # Admin Command - shuts down the bot (atm restricted to rexrex600 because I have local access and am able to restart the bot
            elif contents[0] == 'shutdown' and message.author.name == 'rexrex600':
                file.close()
                await test.delete_message(message)
                await test.close()
            # The general case of someone other than me trying to shut down the bot - 'Fuck off'
            elif contents[0] == 'shutdown' and message.author.name != 'rexrex600':
                await test.send_message(destination=message.channel, content='Fuck off', tts=True)
            # Mute command
            elif contents[0] == 'mute' and message.author.permissions_in(message.channel).kick_members is True:
                member_list = test.get_all_members()
                target_user = [i for i in member_list if i.name in contents[1]][0]
                file = open('MuteList.txt', 'r')
                mute_list = file.read().split(',')
                mute_list = [i for i in mute_list if i != '']
                if target_user.id not in mute_list:
                    file.close
                    mute_list.append(target_user.id)
                    file = open('MuteList.txt', 'w')
                    dump_str = ''
                    for i in mute_list:
                        dump_str += i + ','
                    file.write(dump_str)
                else:
                    await test.send_message(message.author, 'user is already muted')
                file.close()
            # Unmute command
            elif contents[0] == 'unmute' and message.author.permissions_in(message.channel).kick_members is True:
                member_list = test.get_all_members()
                target_user = [i for i in member_list if i.name in contents[1]][0]
                file = open('MuteList.txt', 'r')
                mute_list = file.read().split(',')
                mute_list = [i for i in mute_list if i != '']
                if target_user.id in mute_list:
                    file.close()
                    mute_list.remove(target_user.id)
                    file = open('MuteList.txt', 'w')
                    dump_str = ''
                    for i in mute_list:
                        dump_str += i + ','
                    file.write(dump_str)
                else:
                    await test.send_message(message.author, 'user is not muted')
                file.close()
            #Returns command list - UPDATE AFTER NEW COMMANDS ADDED
            elif contents[0] == 'commands':
                await test.send_message(message.channel, 'My Commands are: !join, !leave, !mute, !unmute, !smashcapitalism')
            # elif contents[0] == 'lableme':
            #     await test.add_roles(test.create_role(server = message.server, name = contents[1], permissions = discord.Permissions.none(), colour = (contents[2], contents[3], contents[4]), hosit = True, ))
        else:
            await test.send_message(destination=message.channel, content='Invalid Command')
        await test.delete_message(message)
    if message.author.id in mute_list:
        await test.delete_message(message)


@test.event
async def on_member_join(member):
    test.send_message(member.server, member.name + " joined the server")

@test.event
async def on_member_remove(member):
    test.send_message(member.server, member.name + " left the server")

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(test.login(str(input('Enter token: \n'))))
    loop.run_until_complete(test.connect())
except Exception:
    loop.run_until_complete(test.close())
finally:
    loop.close()
