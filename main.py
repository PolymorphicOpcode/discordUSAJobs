import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # Ensure channel ID is an integer

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/fetchJobs'):
        await message.channel.send('Grabbing those jobs for you. Please wait...')
        try:
            # Call the external Python script
            result = subprocess.run(['python', 'usajobsMain.py'], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Process the output
                jobs = result.stdout.strip().split("\n")
                if jobs:
                    for job in jobs:
                        await message.channel.send(job)
                else:
                    await message.channel.send("No job listings found.")
            else:
                await message.channel.send(f'Error occurred: {result.stderr}')
        except Exception as e:
            await message.channel.send(f'An error occurred: {str(e)}')

client.run(TOKEN)