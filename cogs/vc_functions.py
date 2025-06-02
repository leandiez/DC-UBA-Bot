# DISCORD
import discord
from discord.ext import commands

# OS IMPORTS
import os
from dotenv import load_dotenv

class VcFunctions(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        #self.category_id = int(os.getenv("CATEGORY_ID"))

    @commands.command()
    async def get_voice_configuration(self, ctx):
        # TODO devuelve toda la configuracion de voz
        print("OK")
        return

    @commands.command()
    async def enable_voice_creator(self, ctx):
        # TODO habilita la funcion del bot para que cree canales nuevos dentro de una category seteada.
        # PRE - tener seteada una o varias categories donde escuchar, caso contrario devuelve mensaje pidiendo configurar con otro comando
        # POST - setea bool de configuracion a true para indicar que la funcion esta activa
        return
    
    @commands.command()
    async def disable_voice_creator(self, ctx):
        # TODO deshabilita la funcion del bot para que cree canales nuevos dentro de una category seteada.
        # PRE - true
        # POST - setea bool de configuracion a false para indicar que la funcion esta apagada
        return

    @commands.command()
    async def setup_new_voice_category(self, ctx, category: int):
        # PRE - recibe la categoria por parametro del comando
        # TODO / POST - guarda el ID de la categoria a agregarle al BOT en una lista dentro de la DB (Mongo?)
        return
    
    @commands.command()
    async def setup_delete_voice_category(ctx, category: int):
        # PRE - recibe la categoria por parametro del comando
        # TODO / POST - borra el ID de la categoria a agregarle al BOT en una lista dentro de la DB (Mongo?)
        return


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None:  # Si el usuario entra a un canal
            category = after.channel.category
            #if category and category.id == self.category_id:
            if category:
                all_occupied = await self.all_channels_occupied(category.voice_channels)
                
                if all_occupied:
                    new_channel_number = await self.get_next_channel_number(category)
                    await member.guild.create_voice_channel(name=f"sala de estudio {new_channel_number}", category=category)

        if before.channel is not None:  # Si el usuario sale de un canal
            category = before.channel.category
            if category:
                free_channels = await self.free_channels_list(category.voice_channels)
                
                if len(free_channels) > 1:
                    await free_channels[-1].delete()

    async def get_next_channel_number(self, category: discord.CategoryChannel) -> int:
        """Encuentra el siguiente número disponible para un canal de estudio"""
        existing_numbers = []

        for channel in category.voice_channels:
            if "sala de estudio" in channel.name:
                parts = channel.name.split()
                if parts[-1].isdigit():  # Si el último elemento del nombre es un número
                    existing_numbers.append(int(parts[-1]))

        return max(existing_numbers, default=0) + 1  # Siguiente número disponible

    async def all_channels_occupied(self, channels: list[discord.VoiceChannel]) -> bool:
        return all(len(channel.members) > 0 for channel in channels)

    async def free_channels_list(self, channels: list[discord.VoiceChannel]) -> list[discord.VoiceChannel]:
        return [channel for channel in channels if len(channel.members) == 0]

async def setup(client: commands.Bot) -> None:
    await client.add_cog(VcFunctions(client))
    print(f"Module vc_functions.py was loaded succesfully.")