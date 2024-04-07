import random
from get_answers import freq_list
import re
import os
import multiprocessing as mp
from tqdm import tqdm
with open('keyword_answers.txt','r') as f:
    keyword_answers = f.read().split('\n')

hints = freq_list[:5000]

def generate_keyword_game(difficulty = 'normal'):
    keyword = random.choice(keyword_answers)
    
    hint_list = []
    for letter in keyword:
        hint = get_hint(letter, difficulty).replace(letter,'_',1)
        hint_list.append([hint, 0])

    padding_len = max(word.find('_') for word, _ in hint_list)
    hint_list = [['*'*(padding_len - word.find('_')) + word, _] for word, _ in hint_list]
    return keyword, hint_list


def get_hint(letter, difficulty='init'):
    if not os.path.isfile(f'candidates/letter_hint_{letter}.txt'):
        candidates = [[word,0] for word,_ in hints if letter in word]
        for candidate in tqdm(candidates):
            word = candidate[0]
            freq = len(re.findall(word.replace(letter,'.',1), ''.join([word for word, _ in hints])))
            candidate[1] = freq
        candidates.sort(key=lambda x: x[1], reverse=True)
        with open(f'candidates/letter_hint_{letter}.txt','w') as f:
            f.write('\n'.join([word for word, _ in candidates]))
    else:
        with open(f'candidates/letter_hint_{letter}.txt','r') as f:
            candidates = f.read().split('\n')
    if difficulty == 'easy':
        return random.choice(candidates[len(candidates)//8:])
    elif difficulty == 'normal':
        return random.choice(candidates[len(candidates)//20:len(candidates)//8])
    elif difficulty == 'hard':
        return random.choice(candidates[10:len(candidates)//20])
    elif difficulty == 'random':
        return random.choice(candidates)
    elif difficulty == 'init':
        return

def format_game(hint_list):
    output = ""
    for word, num in hint_list:
        for letter in word:
            if letter == '*':
                output += ":black_large_square: "
            elif letter == '_':
                output += ":blue_square: "
            elif letter == '?':
                output += ":red_square: "
            else:
                output += f":regional_indicator_{letter}: "
        output += f" {str(num)}\n"
    return output

def make_guess(guess,hint_list,keyword):
    # guess: [number, letter]
    correct = False
    guessed = False
    num, letter = guess
    num -= 1

    if '_' not in hint_list[num][0] and '?' not in hint_list[num][0]:
        guessed = True
        return hint_list, correct, guessed
    hint_list[num][1] += 1
    if letter == keyword[num]:
        hint_list[num][0] = hint_list[num][0].replace('_', letter).replace('?', letter)
        correct = True
    else:
        hint_list[num][0] = hint_list[num][0].replace('_', '?')
    return hint_list, correct, guessed


if __name__ == '__main__':
    # keyword, hint_list = generate_keyword_game()
    # print(keyword)
    # print(format_game(hint_list))
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        print(letter)
        print(get_hint(letter))