import discord
from discord.ext import commands
import asyncio
import random as rd

# Quiz questions and answers
EASY_QUESTIONS = ["What is 2 + 2?", "What is the capital of France?", "What is the color of the sky?", "What is the square root of 16?",
                  "Who wrote 'To Kill a Mockingbird'?", "What is 15 x 15?", "What is the chemical symbol for Gold?", "Solve: 12 * (3 + 2) / 6"]
EASY_ANSWERS = ["4", "paris", "blue", "4", "harper lee", "225", "au", "10"]

MEDIUM_QUESTIONS = [
    "What is the square root of 49?", "Who painted the Mona Lisa?", "What is the smallest prime number?",
    "What is the capital of Australia?", "What is 25 x 25?", "What is the chemical symbol for Iron?",
    "What is the largest ocean on Earth?", "Who wrote the play 'Hamlet'?", "What is the boiling point of water in Celsius?",
    "What planet is known as the Red Planet?"
]

MEDIUM_ANSWERS = [
    "7", "leonardo da vinci", "2", "canberra", "625", "fe",
    "pacific", "william shakespeare", "100", "mars"
]

HARD_QUESTIONS = [
    "What is the square root of 144?", "Who developed the theory of general relativity?", "What is the capital of Iceland?",
    "What is the chemical symbol for Mercury?", "Solve: 18 * (5 + 2) / 3", "Which planet has the most moons in the solar system?",
    "What is the powerhouse of the cell?", "What is the value of Pi (up to 3 decimal places)?", "Who wrote the novel '1984'?",
    "What is the national animal of Scotland?"
]

HARD_ANSWERS = [
    "12", "albert einstein", "reykjavik", "hg", "42", "saturn",
    "mitochondria", "3.142", "george orwell", "unicorn"
]

# Role assignment helper functions
async def assign_role(ctx, role_name):
    """Assign a role to the user."""
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        try:
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention}, you have been assigned the '{role_name}' role!")
        except discord.Forbidden:
            await ctx.send("I don't have permission to assign roles. Please contact an admin.")
    else:
        await ctx.send(f"The '{role_name}' role does not exist. Please contact an admin to create it.")


def check_role(ctx, role_name):
    """Check if the user has the required role."""
    role = discord.utils.get(ctx.author.roles, name=role_name)
    return role is not None

# Role names
EASY_ROLE = "Easy"
MEDIUM_ROLE = "Medium"
HARD_ROLE = "Hard"
WINNER_ROLE = "Winner"


# Quiz classes
class Easy_Quiz(commands.Cog):
    """Easy-Quiz Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="easy-quiz")
    async def quiz(self, ctx):
        """Start a quiz with the user"""
        user = ctx.author
        easy_score = 0
        already_asked_questions = []
        no_of_questions = min(10, len(EASY_QUESTIONS))  # Prevent index errors if there are fewer than 10 questions.

        if not EASY_QUESTIONS:
            await ctx.send("No questions are available for the Easy Quiz.")
            return

        await ctx.send(f"{user.mention}, check your DM for the quiz!")

        for _ in range(no_of_questions):
            # Select a random question
            available_questions = [q for q in EASY_QUESTIONS if q not in already_asked_questions]
            if not available_questions:
                break

            question = rd.choice(available_questions)
            correct_answer = EASY_ANSWERS[EASY_QUESTIONS.index(question)]
            already_asked_questions.append(question)

            await user.send(f"**Question:** {question}")

            def check(msg):
                return msg.author == user and isinstance(msg.channel, discord.DMChannel)

            try:
                response = await self.bot.wait_for("message", check=check, timeout=10)
                if response.content.strip().lower() == correct_answer:
                    easy_score += 1
                    await user.send("Correct!")
                else:
                    await user.send(f"Wrong! The correct answer was: {correct_answer}")
            except asyncio.TimeoutError:
                await user.send("You ran out of time!")

        await user.send(f"Quiz finished! Your total score is: {easy_score}")
        await ctx.send(f"{user.mention}, your quiz is complete! Check your DM for your score.")
        if easy_score == no_of_questions:
            await assign_role(ctx, MEDIUM_ROLE)


class Medium_Quiz(commands.Cog):
    """Medium-Quiz Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="medium-quiz")
    async def quiz(self, ctx):
        """Start a quiz with the user"""
        user = ctx.author
        medium_score = 0
        already_asked_questions = []
        no_of_questions = min(5, len(MEDIUM_QUESTIONS))  # Prevent index errors if there are fewer than 5 questions.

        if not check_role(ctx, MEDIUM_ROLE):
            await ctx.send(
                "You don't have access to the Medium Quiz. Score full marks in the Easy Quiz first!"
            )
            return

        await ctx.send(f"{user.mention}, check your DM for the quiz!")

        for _ in range(no_of_questions):
            available_questions = [q for q in MEDIUM_QUESTIONS if q not in already_asked_questions]
            if not available_questions:
                break

            question = rd.choice(available_questions)
            correct_answer = MEDIUM_ANSWERS[MEDIUM_QUESTIONS.index(question)]
            already_asked_questions.append(question)

            await user.send(f"**Question:** {question}")

            def check(msg):
                return msg.author == user and isinstance(msg.channel, discord.DMChannel)

            try:
                response = await self.bot.wait_for("message", check=check, timeout=20)
                if response.content.strip().lower() == correct_answer:
                    medium_score += 1
                    await user.send("Correct!")
                else:
                    await user.send(f"Wrong! The correct answer was: {correct_answer}")
            except asyncio.TimeoutError:
                await user.send("You ran out of time!")

        await user.send(f"Quiz finished! Your total score is: {medium_score}")
        await ctx.send(f"{user.mention}, your quiz is complete! Check your DM for your score.")
        if medium_score == no_of_questions:
            await assign_role(ctx, HARD_ROLE)


class Hard_Quiz(commands.Cog):
    """Hard-Quiz Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hard-quiz")
    async def quiz(self, ctx):
        """Start a quiz with the user"""
        user = ctx.author
        hard_score = 0
        already_asked_questions = []
        no_of_questions = min(3, len(HARD_QUESTIONS))  # Prevent index errors if there are fewer than 3 questions.

        if not check_role(ctx, HARD_ROLE):
            await ctx.send(
                "You don't have access to the Hard Quiz. Score full marks in the Medium Quiz first!"
            )
            return

        await ctx.send(f"{user.mention}, check your DM for the quiz!")

        for _ in range(no_of_questions):
            available_questions = [q for q in HARD_QUESTIONS if q not in already_asked_questions]
            if not available_questions:
                break

            question = rd.choice(available_questions)
            correct_answer = HARD_ANSWERS[HARD_QUESTIONS.index(question)]
            already_asked_questions.append(question)

            await user.send(f"**Question:** {question}")

            def check(msg):
                return msg.author == user and isinstance(msg.channel, discord.DMChannel)

            try:
                response = await self.bot.wait_for("message", check=check, timeout=30)
                if response.content.strip().lower() == correct_answer:
                    hard_score += 1
                    await user.send("Correct!")
                else:
                    await user.send(f"Wrong! The correct answer was: {correct_answer}")
            except asyncio.TimeoutError:
                await user.send("You ran out of time!")

        await user.send(f"Quiz finished! Your total score is: {hard_score}")
        await ctx.send(f"{user.mention}, your quiz is complete! Check your DM for your score.")
        if hard_score == no_of_questions:
            await assign_role(ctx, WINNER_ROLE)


async def setup(bot):
    await bot.add_cog(Easy_Quiz(bot))
    await bot.add_cog(Medium_Quiz(bot))
    await bot.add_cog(Hard_Quiz(bot))
