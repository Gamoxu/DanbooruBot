import nextcord
from nextcord.ui import *
from typing import *
from nextcord import SlashOption, InteractionMessage
from nextcord.ext import commands
from pybooru import Danbooru
from danbooru_commands import *
from os import environ
import asyncio


from dotenv import load_dotenv

load_dotenv()

token = environ["TOKEN"]

TESTING_GUILD_ID = 963979898962206771  # Replace with your guild ID

bot = commands.Bot()


@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')


@bot.slash_command(description="Searches Danbooru for most recent post with specified tags",)
async def findpost(
        interaction: nextcord.Interaction,
        tags: str = SlashOption(description="Tags for search",),
        safe: str = SlashOption(
        name="safe",
        choices={"sfw": " rating:general", "nsfw": " -rating:general",},
        required=False,)
        ,):
  if safe is None:
      safe = ""
  found_post = get_post_info(search_tags(tags+safe, False))
  embed = nextcord.Embed(title=tags+safe)
  embed.set_author(name=found_post[1], url=found_post[2])
  embed.set_image(url=found_post[0])
  await interaction.send(embed=embed)

@bot.slash_command(description="Loads 100 most recent Danbooru posts with specified tags!",)
async def searchposts(interaction: nextcord.Interaction,
                      tags: str = SlashOption(description="Tags for search",),
                      safe: str = SlashOption(
                          name="safe",
                          choices={"sfw": " rating:general", "nsfw": " -rating:general"},
                          required=False,
                          description="Show explicit content?",)
                      ,):
    fbutton = Button(label="Next Post", style=nextcord.ButtonStyle.secondary, emoji="▶️", row=1)
    bbutton = Button(label="Prev Post", style=nextcord.ButtonStyle.secondary, emoji="◀️", row=1)
    if safe is None:
        safe = ""
    post_list = get_posts(tags + safe, False)

    async def fbutton_callback(interaction):
        post_list.append(post_list.pop(0))
        found_post = get_post_info(post_list[0])
        embed = nextcord.Embed(title=tags + safe)
        embed.set_author(name=found_post[1], url=found_post[2])
        embed.set_image(url=found_post[0])
        await interaction.response.edit_message(embed=embed)

    fbutton.callback = fbutton_callback

    async def bbutton_callback(interaction):
        post_list.insert(0, post_list.pop())
        found_post = get_post_info(post_list[0])
        embed = nextcord.Embed(title=tags + safe)
        embed.set_author(name=found_post[1], url=found_post[2])
        embed.set_image(url=found_post[0])
        await interaction.response.edit_message(embed=embed)

    bbutton.callback = bbutton_callback

    view = View(timeout=None)
    view.add_item(bbutton)
    view.add_item(fbutton)
    found_post = get_post_info(post_list[0])
    embed = nextcord.Embed(title=tags+safe)
    embed.set_author(name=found_post[1], url=found_post[2])
    embed.set_image(url=found_post[0])
    await interaction.send(embed=embed, view=view)

@bot.slash_command(description="Loads 100 random Danbooru posts with specified tags!",)
async def randomposts(interaction: nextcord.Interaction,
                      tags: str = SlashOption(description="Tags for search",),
                      safe: str = SlashOption(
                          name="safe",
                          choices={"sfw": " rating:general", "nsfw": " -rating:general"},
                          required=False,
                          description="Show explicit content?",)
                      ,):
    fbutton = Button(label="Next Post", style=nextcord.ButtonStyle.secondary, emoji="▶️", row=1)
    bbutton = Button(label="Prev Post", style=nextcord.ButtonStyle.secondary, emoji="◀️", row=1)
    if safe is None:
        safe = ""
    post_list = get_posts(tags + safe, True)

    async def fbutton_callback(interaction):
        post_list.append(post_list.pop(0))
        found_post = get_post_info(post_list[0])
        embed = nextcord.Embed(title=tags + safe)
        embed.set_author(name=found_post[1], url=found_post[2])
        embed.set_image(url=found_post[0])
        await interaction.response.edit_message(embed=embed)

    fbutton.callback = fbutton_callback

    async def bbutton_callback(interaction):
        post_list.insert(0, post_list.pop())
        found_post = get_post_info(post_list[0])
        embed = nextcord.Embed(title=tags + safe)
        embed.set_author(name=found_post[1], url=found_post[2])
        embed.set_image(url=found_post[0])
        await interaction.response.edit_message(embed=embed)

    bbutton.callback = bbutton_callback

    view = View(timeout=None)
    view.add_item(bbutton)
    view.add_item(fbutton)
    found_post = get_post_info(post_list[0])
    embed = nextcord.Embed(title=tags+safe)
    embed.set_author(name=found_post[1], url=found_post[2])
    embed.set_image(url=found_post[0])
    await interaction.send(embed=embed, view=view)

answer = ""

@bot.slash_command()
async def guess(interaction: nextcord.Interaction):
    def is_response(m):
        if m.reference is not None:
            if m.reference.message_id == base_message.message_id:
                return True
        return False

    global answer
    random_post = get_post_info(search_tags("hatsune_miku rating:general", True))
    answer = random_post[3]

    answer = random_post[3]
    embed = nextcord.Embed(title="Name the character!")
    embed.set_author(name=random_post[1], url=random_post[2])
    embed.set_image(url=random_post[0])
    send_message = await interaction.send(embed=embed)
    base_message = send_message.fetch().original_message()
    try:
        guess = await bot.wait_for("message", check=is_response, timeout=30.0)
        await interaction.send("shit")
        guess = guess.content
        guess = guess.replace(" ", "_").lower()
    except asyncio.TimeoutError:
        return await interaction.send(f"Sorry, you took too long it was {answer}.")

    if answer.find(guess.replace(" ", "_").lower()) != -1:
        await interaction.send("You are right!")
    else:
        await interaction.send(f"You're dumb it's {answer}.")

bot.run(token)
