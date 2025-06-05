# DISCORD IMPORTS
import discord

# MONGODB IMPORTS
from typing import Literal
import motor.motor_asyncio
from pymongo.write_concern import WriteConcern
from collections import namedtuple

# ASYNC IMPORTS
import asyncio

# OS IMPORTS
import os

class MongoHandler:
    def __init__(self):
        self.client = None
        self.db = None
        self.vc_collection: motor.motor_asyncio.AsyncIOMotorCollection = None

    async def connect(self, db_name: str, collection_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DB_URL"))
        self.db = self.client[db_name]
        self.vc_collection = self.db[collection_name]

    async def add_vc(self, voice_channel: discord.VoiceChannel) -> bool:
        if not await self.is_configured(voice_channel):
            await self.vc_collection.insert_one({
                "type": "authorized_vc",
                "guild_id": voice_channel.guild.id,
                "name": voice_channel.name,
                "id": voice_channel.id
            })

            return True

        return False

    async def remove_vc(self, voice_channel: discord.VoiceChannel) -> bool:
        if await self.is_configured(voice_channel):
            await self.vc_collection.delete_one({
                "type": "authorized_vc",
                "guild_id": voice_channel.guild.id,
                "name": voice_channel.name,
                "id": voice_channel.id
            })

            return True
        
        return False

    async def is_configured(self, voice_channel: discord.VoiceChannel) -> bool:
        return await self.vc_collection.find_one({
            "type": "authorized_vc",
            "guild_id": voice_channel.guild.id,
            "name": voice_channel.name,
            "id": voice_channel.id
        }) is not None

# TEST

# FakeGuild = namedtuple("FakeGuild", ["id"])
# FakeVC = namedtuple("FakeVC", ["guild", "id", "name"])

# async def main():
#     mongo = MongoHandler()
#     await mongo.connect(db_name="dc_uba_bot", collection_name="vcs_config")

#     test_guild = FakeGuild(id=123)
#     test_vc = FakeVC(guild=test_guild, id=456, name="test")

#     await mongo.add_vc(test_vc)
#     print("Canal agregado.")

#     await asyncio.sleep(5)

#     await mongo.remove_vc(test_vc)
#     print("Canal eliminado.")

# asyncio.run(main())