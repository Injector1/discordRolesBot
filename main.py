import discord
from discord import utils
from config import Config

class Client(discord.Client):
    async def on_ready(self):
        print("Logged on as {}".format(self.user))
    
    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
    
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            if len([role for role in member.roles if role.id not in config.EXCTENTENTIONS]) <= config.MAX_ROLES:
                await member.add_roles(role)
            else:
                await message.remove_reaction(payload.emoji, member)
                print("ERROR, Too many roles")
        except KeyError as e:
            print("ERROR, KeyError")
        except Exception as e:
            print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            await member.remove_roles(role)
        except KeyError as e:
            print("ERROR, KeyError")
        except Exception as e:
            print(repr(e))
        pass


client = Client()
config = Config()
client.run(config.TOKEN)
