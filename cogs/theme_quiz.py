import discord
from discord.ext import commands
from asyncio import TimeoutError
import asyncio
import random as rd

# Quiz questions will eventually go into database

EASY_QUESTIONS = ["What is 2 + 2?", "What is the capital of France?", "What is the color of the sky?", "What is the square root of 16?",
             "Who wrote 'To Kill a Mockingbird'?", "What is 15 x 15?", "What is the chemical symbol for Gold?","Solve: 12 * (3 + 2) / 6"]
EASY_ANSWERS = ["4","paris","blue","4","harper lee","225","au","10"]

MEDIUM_QUESTIONS = [
    "What is the square root of 49?",
    "Who painted the Mona Lisa?",
    "What is the smallest prime number?",
    "What is the capital of Australia?",
    "What is 25 x 25?",
    "What is the chemical symbol for Iron?",
    "What is the largest ocean on Earth?",
    "Who wrote the play 'Hamlet'?",
    "What is the boiling point of water in Celsius?",
    "What planet is known as the Red Planet?"
]

MEDIUM_ANSWERS = [
    "7",                # Square root of 49
    "leonardo da vinci", # Mona Lisa painter
    "2",                # Smallest prime number
    "canberra",         # Capital of Australia
    "625",              # 25 x 25
    "fe",               # Chemical symbol for Iron
    "pacific",          # Largest ocean
    "william shakespeare", # Author of Hamlet
    "100",              # Boiling point of water
    "mars"              # Red Planet
]

HARD_QUESTIONS = [
    "What is the square root of 144?",
    "Who developed the theory of general relativity?",
    "What is the capital of Iceland?",
    "What is the chemical symbol for Mercury?",
    "Solve: 18 * (5 + 2) / 3",
    "Which planet has the most moons in the solar system?",
    "What is the powerhouse of the cell?",
    "What is the value of Pi (up to 3 decimal places)?",
    "Who wrote the novel '1984'?",
    "What is the national animal of Scotland?"
]

HARD_ANSWERS = [
    "12",                   # Square root of 144
    "albert einstein",      # General relativity
    "reykjavik",            # Capital of Iceland
    "hg",                   # Chemical symbol for Mercury
    "42",                   # Solve: 18 * (5 + 2) / 3
    "saturn",               # Most moons in the solar system
    "mitochondria",         # Powerhouse of the cell
    "3.142",                # Value of Pi
    "george orwell",        # Author of 1984
    "unicorn"               # National animal of Scotland
]


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
        no_of_questions = 10
        


        for _ in range(no_of_questions):
                #Select A random question
                while True:
                    easy_quiz = discord.utils.get(ctx.guild.channels, name="easy-quiz")
                    if not easy_quiz:
                        await ctx.send("The 'easy-quiz' channel does not exist. Please create it or contact an admin.")
                        return
                    random_question  = rd.randint(0,len(EASY_QUESTIONS)-1)
                    question = EASY_QUESTIONS[random_question]
                    correct_answer = EASY_ANSWERS[random_question]
                    if question not in already_asked_questions:
                        already_asked_questions.append(EASY_QUESTIONS[random_question])
                        break
                    
                    
                await easy_quiz.send(f"**Question:** {question}")
                await ctx.send(f"{user.mention}, check your Easy-Quiz channel for the question!")

                def check(msg):
                    return msg.author == user and msg.channel == easy_quiz
                    
                try:
                            response = await self.bot.wait_for("message", check=check, timeout=30)
                            if response.content.strip().lower() == correct_answer:
                                easy_score += 1
                                await easy_quiz.send("Correct!")
                            else:
                                easy_score -= 1
                                await easy_quiz.send(f"Wrong! The correct answer was: {correct_answer}")
                except asyncio.TimeoutError:
                                easy_score -= 1
                                await easy_quiz.send("You ran out of time! -1 point.")
                    
                

        await user.send(f"Quiz finished! Your total score is: {easy_score}")
        await ctx.send(f"{user.mention}, your quiz is complete! Check your DM for your score.")


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
        no_of_questions = 5
        


        for _ in range(no_of_questions):
                #Select A random question
                while True:
                    medium_quiz = discord.utils.get(ctx.guild.channels, name="medium-quiz")
                    if not medium_quiz:
                        await ctx.send("The 'easy-quiz' channel does not exist. Please create it or contact an admin.")
                        return

                    random_question  = rd.randint(0,len(MEDIUM_QUESTIONS)-1)
                    question = MEDIUM_QUESTIONS[random_question]
                    correct_answer = MEDIUM_ANSWERS[random_question]
                    if question not in already_asked_questions:
                        already_asked_questions.append(question)
                        break
                    
                    
                await medium_quiz.send(f"**Question:** {question}")
                await ctx.send(f"{user.mention}, check your Easy-Quiz channel for the question!")

                def check(msg):
                    return msg.author == user and msg.channel == medium_quiz
                    
                try:
                            response = await self.bot.wait_for("message", check=check, timeout=30)
                            if response.content.strip().lower() == correct_answer:
                                medium_score += 1
                                await medium_quiz.send("Correct!")
                            else:
                                medium_score -= 1
                                await medium_quiz.send(f"Wrong! The correct answer was: {correct_answer}")
                except asyncio.TimeoutError:
                                medium_score -= 1
                                await medium_quiz.send("You ran out of time! -1 point.")
                    
                

        await user.send(f"Quiz finished! Your total score is: {medium_score}")
        await ctx.send(f"{user.mention}, your quiz is complete! Check your DM for your score.")


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
        no_of_questions = 3
        


        for _ in range(no_of_questions):
                #Select A random question
                while True:
                    hard_quiz = discord.utils.get(ctx.guild.channels, name="hard-quiz")
                    if not hard_quiz:
                        await ctx.send("The 'easy-quiz' channel does not exist. Please create it or contact an admin.")
                        return
                    random_question  = rd.randint(0,len(HARD_QUESTIONS)-1)
                    question = HARD_QUESTIONS[random_question]
                    correct_answer = HARD_ANSWERS[random_question]
                    if question not in already_asked_questions:
                        already_asked_questions.append(question)
                        break
                    
                    
                await hard_quiz.send(f"**Question:** {question}")
                await ctx.send(f"{user.mention}, check your Easy-Quiz channel for the question!")

                def check(msg):
                    return msg.author == user and msg.channel == hard_quiz
                    
                try:
                            response = await self.bot.wait_for("message", check=check, timeout=30)
                            if response.content.strip().lower() == correct_answer:
                                hard_score += 1
                                await hard_quiz.send("Correct!")
                            else:
                                hard_score -= 1
                                await hard_quiz.send(f"Wrong! The correct answer was: {correct_answer}")
                except asyncio.TimeoutError:
                                hard_score -= 1
                                await hard_quiz.send("You ran out of time! -1 point.")
                    
                

        await user.send(f"Quiz finished! Your total score is: {hard_score}")
        await ctx.send(f"{user.mention}, your quiz is complete! Check your DM for your score.")



async def setup(bot):
    await bot.add_cog(Easy_Quiz(bot))
    await bot.add_cog(Medium_Quiz(bot))
    await bot.add_cog(Hard_Quiz(bot))
