import discord
from discord.ext import commands
import random as rd
import asyncio
from datetime import datetime, timedelta

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
EASY_ATTEMPTED = "easy-attempted"
MEDIUM_ATTEMPTED = "medium-attempted"
HARD_ATTEMPTED = "hard-attempted"

# Sample questions and answers
EASY_QUIZ = {
    "What is 2 + 2?": "4",
    "What is the capital of France?": "paris",
    "What is the color of the sky?": "blue",
    "What is the square root of 16?": "4",
    "Who wrote 'To Kill a Mockingbird'?": "harper lee",
    "What is 15 x 15?": "225",
    "What is the chemical symbol for Gold?": "au",
    "Solve: 12 * (3 + 2) / 6": "10"
}

MEDIUM_QUIZ = {
    "What is the square root of 49?": "7",
    "Who painted the Mona Lisa?": "leonardo da vinci",
    "What is the smallest prime number?": "2",
    "What is the capital of Australia?": "canberra",
    "What is 25 x 25?": "625",
    "What is the chemical symbol for Iron?": "fe",
    "What is the largest ocean on Earth?": "pacific",
    "Who wrote the play 'Hamlet'?": "william shakespeare",
    "What is the boiling point of water in Celsius?": "100",
    "What planet is known as the Red Planet?": "mars"
}
HARD_QUIZ = {
    "What is the square root of 49?": "7",
    "Who painted the Mona Lisa?": "leonardo da vinci",
    "What is the smallest prime number?": "2",
    "What is the capital of Australia?": "canberra",
    "What is 25 x 25?": "625",
    "What is the chemical symbol for Iron?": "fe",
    "What is the largest ocean on Earth?": "pacific",
    "Who wrote the play 'Hamlet'?": "william shakespeare",
    "What is the boiling point of water in Celsius?": "100",
    "What planet is known as the Red Planet?": "mars"
}

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
        no_of_questions = min(10, len(EASY_QUIZ))  # Prevent index errors if there are fewer than 10 questions.

        attempted_role = discord.utils.get(ctx.guild.roles, name="easy-attempted")
        if attempted_role in user.roles:
            await ctx.send(f"{user.mention}, you have already attempted the Easy Quiz and cannot retake it.")
            return
        
        if not EASY_QUIZ:
            await ctx.send("No questions are available for the Easy Quiz.")
            return

        await ctx.send(f"{user.mention}, check your DM for the quiz!")

        try:
            dm_channel = await user.create_dm()

            for _ in range(no_of_questions):
                available_questions = [q for q in EASY_QUIZ if q not in already_asked_questions]
                if not available_questions:
                    await dm_channel.send("No more questions available.")
                    break

                question = rd.choice(available_questions)
                correct_answer = EASY_QUIZ[question]
                already_asked_questions.append(question)

                # Send the question to DMs
                await dm_channel.send(f"**Question:** {question}")
                timer_message = await dm_channel.send("Time remaining: 10 seconds")

                # Check the answer from the user
                def check(msg):
                    return msg.author == user and msg.channel == dm_channel

                question_end_time = datetime.now() + timedelta(seconds=10)
                answered = False

                async def update_timer():
                    while datetime.now() < question_end_time:
                        remaining_time = int((question_end_time - datetime.now()).total_seconds())
                        await timer_message.edit(content=f"Time remaining: {remaining_time} seconds")
                        await asyncio.sleep(1)

                async def check_answer():
                    nonlocal answered
                    try:
                        response = await self.bot.wait_for("message", check=check, timeout=10)
                        if response.content.strip().lower() == correct_answer:
                            nonlocal easy_score
                            easy_score += 1
                            await dm_channel.send("Correct!")
                        else:
                            await dm_channel.send(f"Wrong! The correct answer was: {correct_answer}")
                        answered = True
                    except asyncio.TimeoutError:
                        pass

                timer_task = asyncio.create_task(update_timer())
                answer_task = asyncio.create_task(check_answer())

                await asyncio.wait([timer_task, answer_task], return_when=asyncio.FIRST_COMPLETED)

                if not answered:
                    await dm_channel.send(f"Time's up! The correct answer was: {correct_answer}")

            # Send final score to the 'easy-quiz' channel
            easy_quiz_channel = discord.utils.get(ctx.guild.channels, name="easy-quiz")
            if easy_quiz_channel:
                await easy_quiz_channel.send(f"{user.mention}, your Easy Quiz is complete! Your total score is: {easy_score}")

            # Assign new role if the user scores perfectly
            if easy_score == no_of_questions:
                await assign_role(ctx, MEDIUM_ROLE)
            else:
                await assign_role(ctx, EASY_ATTEMPTED)

        except discord.Forbidden:
            await ctx.send(f"{user.mention}, I cannot DM you. Please make sure your DMs are open.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

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
        no_of_questions = min(10, len(MEDIUM_QUIZ))  # Prevent index errors if there are fewer than 10 questions.

        attempted_role = discord.utils.get(ctx.guild.roles, name="medium-attempted")
        if attempted_role in user.roles:
            await ctx.send(f"{user.mention}, you have already attempted the Quiz and cannot retake it.")
            return

        if not MEDIUM_QUIZ:
            await ctx.send("No questions are available for the Medium Quiz.")
            return
        
        if not check_role(ctx, MEDIUM_ROLE):
            await ctx.send(
                "You don't have access to the Medium Quiz. Score full marks in the Easy Quiz first!"
            )
            return

        await ctx.send(f"{user.mention}, check your DM for the quiz!")

        try:
            dm_channel = await user.create_dm()

            for _ in range(no_of_questions):
                available_questions = [q for q in MEDIUM_QUIZ if q not in already_asked_questions]
                if not available_questions:
                    await dm_channel.send("No more questions available.")
                    break

                question = rd.choice(available_questions)
                correct_answer = MEDIUM_QUIZ[question]
                already_asked_questions.append(question)

                # Send the question to DMs
                await dm_channel.send(f"**Question:** {question}")
                timer_message = await dm_channel.send("Time remaining: 10 seconds")

                # Check the answer from the user
                def check(msg):
                    return msg.author == user and msg.channel == dm_channel

                question_end_time = datetime.now() + timedelta(seconds=10)
                answered = False

                async def update_timer():
                    while datetime.now() < question_end_time:
                        remaining_time = int((question_end_time - datetime.now()).total_seconds())
                        await timer_message.edit(content=f"Time remaining: {remaining_time} seconds")
                        await asyncio.sleep(1)

                async def check_answer():
                    nonlocal answered
                    try:
                        response = await self.bot.wait_for("message", check=check, timeout=10)
                        if response.content.strip().lower() == correct_answer:
                            nonlocal medium_score
                            medium_score += 1
                            await dm_channel.send("Correct!")
                        else:
                            await dm_channel.send(f"Wrong! The correct answer was: {correct_answer}")
                        answered = True
                    except asyncio.TimeoutError:
                        pass

                timer_task = asyncio.create_task(update_timer())
                answer_task = asyncio.create_task(check_answer())

                await asyncio.wait([timer_task, answer_task], return_when=asyncio.FIRST_COMPLETED)

                if not answered:
                    await dm_channel.send(f"Time's up! The correct answer was: {correct_answer}")

            # Send final score to the 'medium-quiz' channel
            medium_quiz_channel = discord.utils.get(ctx.guild.channels, name="medium-quiz")
            if medium_quiz_channel:
                await medium_quiz_channel.send(f"{user.mention}, your Medium Quiz is complete! Your total score is: {medium_score}")

            # Assign new role if the user scores perfectly
            if medium_score == no_of_questions:
                await assign_role(ctx, HARD_ROLE)
            else:
                await assign_role(ctx, MEDIUM_ATTEMPTED)

        except discord.Forbidden:
            await ctx.send(f"{user.mention}, I cannot DM you. Please make sure your DMs are open.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

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
        no_of_questions = min(10, len(HARD_QUIZ))  # Prevent index errors if there are fewer than 10 questions.

        attempted_role = discord.utils.get(ctx.guild.roles, name="hard-attempted")
        if attempted_role in user.roles:
            await ctx.send(f"{user.mention}, you have already attempted the Quiz and cannot retake it.")
            return

        if not HARD_QUIZ:
            await ctx.send("No questions are available for the Medium Quiz.")
            return
        
        if not check_role(ctx, HARD_ROLE):
            await ctx.send(
                "You don't have access to the Medium Quiz. Score full marks in the Easy Quiz first!"
            )
            return

        await ctx.send(f"{user.mention}, check your DM for the quiz!")

        try:
            dm_channel = await user.create_dm()

            for _ in range(no_of_questions):
                available_questions = [q for q in HARD_QUIZ if q not in already_asked_questions]
                if not available_questions:
                    await dm_channel.send("No more questions available.")
                    break

                question = rd.choice(available_questions)
                correct_answer = HARD_QUIZ[question]
                already_asked_questions.append(question)

                # Send the question to DMs
                await dm_channel.send(f"**Question:** {question}")
                timer_message = await dm_channel.send("Time remaining: 10 seconds")

                # Check the answer from the user
                def check(msg):
                    return msg.author == user and msg.channel == dm_channel

                question_end_time = datetime.now() + timedelta(seconds=10)
                answered = False

                async def update_timer():
                    while datetime.now() < question_end_time:
                        remaining_time = int((question_end_time - datetime.now()).total_seconds())
                        await timer_message.edit(content=f"Time remaining: {remaining_time} seconds")
                        await asyncio.sleep(1)

                async def check_answer():
                    nonlocal answered
                    try:
                        response = await self.bot.wait_for("message", check=check, timeout=10)
                        if response.content.strip().lower() == correct_answer:
                            nonlocal hard_score
                            hard_score += 1
                            await dm_channel.send("Correct!")
                        else:
                            await dm_channel.send(f"Wrong! The correct answer was: {correct_answer}")
                        answered = True
                    except asyncio.TimeoutError:
                        pass

                timer_task = asyncio.create_task(update_timer())
                answer_task = asyncio.create_task(check_answer())

                await asyncio.wait([timer_task, answer_task], return_when=asyncio.FIRST_COMPLETED)

                if not answered:
                    await dm_channel.send(f"Time's up! The correct answer was: {correct_answer}")

            # Send final score to the 'medium-quiz' channel
            hard_quiz_channel = discord.utils.get(ctx.guild.channels, name="Hard-quiz")
            if hard_quiz_channel:
                await hard_quiz_channel.send(f"{user.mention}, your Medium Quiz is complete! Your total score is: {medium_score}")

            # Assign new role if the user scores perfectly
            if hard_score == no_of_questions:
                await assign_role(ctx, HARD_ROLE)
            else:
                await assign_role(ctx, HARD_ATTEMPTED)

        except discord.Forbidden:
            await ctx.send(f"{user.mention}, I cannot DM you. Please make sure your DMs are open.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Easy_Quiz(bot))
    await bot.add_cog(Medium_Quiz(bot))
    await bot.add_cog(Hard_Quiz(bot))