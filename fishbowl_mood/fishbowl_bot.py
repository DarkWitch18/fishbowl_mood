import discord
import random
from discord.ext import commands
from PIL import Image

# Define function to add fish
def add_fish(image, num_fish):
    fish_img = Image.open("fish.png").convert("RGBA")
    width_bg, height_bg = image.size
    max_fish_width = width_bg // 3.5
    max_fish_height = height_bg // 3.5
    fish_img.thumbnail((max_fish_width, max_fish_height))

    # Define bounding box for fish placement
    box_top_left = (300, 300)
    box_bottom_right = (1000, 1100)

    for _ in range(num_fish):
        x = random.randint(box_top_left[0], box_bottom_right[0] - fish_img.width)
        y = random.randint(box_top_left[1], box_bottom_right[1] - fish_img.height)
        image.paste(fish_img, (x, y), fish_img)

# Define function to add mood image
def add_mood_image(image, mood, position):
    mood_img = Image.open(f"{mood}.png")
    mood_img = mood_img.resize((1250, 1250))
    image.paste(mood_img, position, mood_img)

# Define intents
intents = discord.Intents.default()

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Define command to generate image
@bot.command()
async def fishbowl(ctx, energy_level: int, mood: str):
    # Validate inputs
    if energy_level < 1 or energy_level > 5:
        await ctx.send("Energy level must be between 1 and 5.")
        return
    if mood not in ["lurk", "fragile", "interact", "no_interact"]:
        await ctx.send("Invalid mood. Choose from: lurk, fragile, interact, no_interact")
        return

    # Load background image
    background_img = Image.open("fishbowl_kid.png").convert("RGBA")

    # Add fish based on energy level
    num_fish = energy_level
    add_fish(background_img, num_fish)

    # Add mood image
    add_mood_image(background_img, mood, (180, 80))

    # Save the final image
    output_path = "final_image.png"
    background_img.save(output_path)

    # Send the image to the Discord channel
    with open(output_path, 'rb') as file:
        picture = discord.File(file)
        await ctx.send(file=picture)

# Run the bot
bot.run('MTIzMzA1OTU4MzMyOTgzMzAxMQ.GIlwV-.WTDzKj_UWrLuvZ9ap-DvZVVdhr6lH5rMboSgxw')
