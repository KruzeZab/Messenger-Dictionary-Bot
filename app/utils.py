import os, requests
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary


dictionary=PyDictionary()

def meanings(word):
    result = ''
    definitions = dictionary.meaning(word)
    if definitions:
        for key,value in definitions.items():
            for meaning in value: 
                result += f"{word}({key}): {meaning}\n\n"
    return result

def synonyms(word):
    result = ''
    syno = dictionary.synonym(word)
    if syno:
        result+=f'{word}(synonyms): '
        result += ', '.join(syno)
    return result
    

def antonyms(word):
    result = ''
    anto = dictionary.antonym(word)
    if anto:
        result+=f'{word}(antonyms): '
        result += ', '.join(anto)
    return result


def examples(word):
    result = ''
    re = requests.get(f'https://www.dictionary.com/browse/{word}')
    soup = BeautifulSoup(re.text, 'html.parser')
    examples = soup.find_all('span', class_='luna-example')
    if examples:
        result += f'{word}(examples):\n\n'
        for example in examples:
            result += example.text.capitalize()+'\n\n'
    return result
