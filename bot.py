from discord import Intents
from dotenv import load_dotenv
from discord.ext import commands
from os import getenv


exts =  ["cogs.theme_quiz"]

class MlscBot(commands.Bot):
  def __init__(self, command_prefix: str, intents: Intents, **kwargs):
    super().__init__(command_prefix, intents=intents, **kwargs)
  
  async def setup_hook(self) -> None:
    for ext in exts:
      await self.load_extension(ext)

    print("Loaded all Cogs .....")

    await self.tree.sync()
  
  async def on_ready(self):
    print("MLSC Bot is running ......")

  async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Oops! The command `{ctx.invoked_with}` does not exist. Use `!help` to see the list of available commands.")
        else:
            await ctx.send("An error occurred while processing your command. Please try again.")
            raise error

if __name__ == "__main__":
  bot = MlscBot(command_prefix='!', intents=Intents.all())
  load_dotenv()
  bot.run(getenv("DISCORD_TOKEN"))