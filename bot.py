import discord
import pickle
from utils import generate_keyword_game, format_game, make_guess
TOKEN = pickle.load(open('token.pkl','rb')) #not gonna show my token to ya :)

class KeywordBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content == '$play-keyword':
            await message.reply("Choose your difficulty: easy, normal, hard or random")
            def is_difficulty(msg):
                if msg.content.lower() == '!quit':
                    return True
                return msg.content.lower() in ['easy','normal','hard','random'] and msg.author == message.author
            difficulty = await self.wait_for('message', check=is_difficulty, timeout=600)
            if difficulty.content == '!quit':
                return await message.reply('Quit session.')
            difficulty = difficulty.content.lower()
            keyword, hint_list = generate_keyword_game(difficulty)
            print(keyword)
            await message.reply("enter your guess in the format of <number> <letter>, where the number represents which letter you are guessing (1-6, top to bottom).\n eg. \"1 a\"")
            await message.reply(format_game(hint_list))

            def is_guess(msg):
                guess = msg.content.lower()
                if guess == '!quit':
                    return True
                try:
                    num, letter = guess.split(' ')
                    num = int(num)
                    return num > 0 and num <= 6 and letter in 'abcdefghijklmnopqrstuvwxyz' and msg.author == message.author
                except:
                    return False
            guesses = 0
            while any(i in ''.join([word for word,_ in hint_list]) for i in ['_','?']):
                guesses += 1
                guess = await self.wait_for('message', check=is_guess, timeout=600)
                if guess.content == '!quit':
                    return await message.reply('Quit session.')
                guess = guess.content.lower().split(' ')
                guess[0] = int(guess[0])
                hint_list, correct, guessed = make_guess(guess, hint_list, keyword)
                if guessed:
                    await message.reply("You have already guessed that letter correctly!")
                elif correct:
                    await message.reply("**Correct** letter!")
                else:
                    await message.reply("**Incorrect** letter!")
                await message.reply(format_game(hint_list))

            return await message.reply(f"End of game. You made **{guesses}** guesses; the minimum number of guesses is 6.")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = KeywordBot(intents=intents)
client.run(TOKEN)