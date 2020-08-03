import requests
from bs4 import BeautifulSoup
import sys

def get_data(languages, word):
    url = "https://context.reverso.net/translation/" + languages + '/' + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    timeout = 5
    try:
        result = requests.get(url, timeout=timeout, headers = headers)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Something wrong with your internet connection")
    src = result.content
    soup = BeautifulSoup(src,'html.parser')

    translated_sentences = [x.text.strip() for x in soup.find_all('span', {'class':'text'}) if '\n' in x.text]
    translated_words =[x.text.strip() for x in soup.find_all(['div', 'a'], {"class": ['translation']}) if '\n' in x.text]
    processed_word = translated_words[1:]
    return processed_word, translated_sentences

def printing(wCollection, language, quantity = (5,10)):
    result = []
    print(language, 'Translations:')
    result.append(language + " Translations:")
    if len(wCollection[0]) < quantity[0]:
        for i in wCollection[0]:
            print(i)
            result.append(i)
    else:
        for i in range(quantity[0]):
            print(wCollection[0][i])
            result.append(wCollection[0][i])
    print()
    print(language, 'Examples:')
    result.append(language + ' Examples:')
    counter = 0
    if len(wCollection[1]) / 2 < quantity[1]:
        for i in wCollection[1]:
            counter += 1
        if counter % 2 == 0:
            print()
    else:
        for i in range(quantity[1]):
            counter += 1
            print(wCollection[1][i])
            result.append(wCollection[1][i])
            if counter % 2 == 0:
                print()

    return result


args = sys.argv


yourLanguage = args[1]
translateLanguage = args[2]
word = args[3]



languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
             'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

if (translateLanguage != 'all') and (translateLanguage not in languages):
    print("Sorry, the program doesn't support {}".format(translateLanguage))


save_to_file = open(word+'.txt', 'w+', encoding='utf-8')

if translateLanguage == 'all':
    for language in languages:
        if language == yourLanguage:
            continue
        languagesTranslation = yourLanguage +"-"+ language
        translation = get_data(languagesTranslation.lower(), word)

        if len(translation[0]) == 0 and len(translation[1]) == 0:
            print("Sorry, unable to find {}".format(word))
            break
        result = printing(translation, language, (1,2))
        for i in result:
            save_to_file.write(i+'\n')
else:
    languagesTranslation = yourLanguage +"-"+ translateLanguage
    translation = get_data(languagesTranslation.lower(), word)
    if len(translation) == 0:
            print("Sorry, unable to find {}".format(word))
    else:
        result = printing(translation, translateLanguage, (1,2))
        for i in result:
            save_to_file.write(i+'\n')
    save_to_file.close()

