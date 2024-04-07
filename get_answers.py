import json
with open('words_dictionary.json','r') as f:
    freq_dict = json.load(f)

freq_list = [(word,freq_dict[word]) for word in freq_dict]
freq_list.sort(key=lambda x: x[1], reverse=True)
keyword_answers = [(word, freq) for word, freq in freq_list if len(word) == 6]
scope = 3000
keyword_answers = keyword_answers[:scope]

if __name__ == '__main__':
    with open('keyword_answers.txt', 'w') as f:
        for word, freq in keyword_answers:
            f.write(word+'\n')