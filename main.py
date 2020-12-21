import requests
import re
from bs4 import BeautifulSoup as bs
from operator import itemgetter
from multiprocessing import Process, Queue
from time import time

def turn_into_soup(url):
    source_code = requests.get(url).text
    return bs(source_code, 'html.parser')

def spider(url):
    list_of_links = []
    soup = turn_into_soup(url)
    content_list = soup.find('ul', class_='content-list content-list_posts shortcuts_items')
    post_links = content_list.find_all('a', class_='post__title_link')
    for a in post_links:
        list_of_links.append(a['href'])
    return list_of_links

def parser(url):
    soup = turn_into_soup(url)
    content_list = soup.find('div', class_='post__body post__body_full')
    words_from_site = re.split(r'[-\s]', content_list.get_text().lower())
    return words_from_site

def clean_up_list(word_list, prepositions, symbols):
    clean_word_list = []
    for word in word_list:
        for symbol in symbols:
            word = word.replace(symbol, "")
        if len(word) > 1:
            clean_word_list.append(word)
    for index in reversed(range(len(clean_word_list))):
        if clean_word_list[index] in prepositions:
            clean_word_list.pop(index)
    return clean_word_list

def create_dict(clean_word_list):
    word_count = {}
    for word in clean_word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

#def get_key(dict, value):
#    for k, v in dict.items():
#        if v == value:
#            return k

# dict = create_dict(clean_up_list(parser('https://habr.com/ru/company/englishdom/blog/508116/'), prepositions, symbols))

def main():
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    symbols = '-`!@#$%^&*()–_+=\'";:/?,.<>\\~[]{}«»∙…1234567890qwertyuiopasdfghjklzxcvbnm'
    prepositions = ['без', 'безо', 'близ', 'в', 'во', 'вместо', 'вне', 'для', 'до',
                    'за', 'из', 'изо', 'из-за', 'из-под', 'к', 'ко', 'кроме', 'между',
                    'меж', 'на', 'над', 'надо', 'о', 'об', 'обо', 'от', 'ото', 'перед',
                    'передо', 'пред', 'предо', 'пo', 'под', 'подо', 'при', 'про', 'ради',
                    'с', 'со', 'сквозь', 'среди', 'у', 'через', 'чрез', 'и', 'не', 'то', 'же', 'a', 'но']

    MAIN_URL = 'https://habr.com/ru/all/'

    start = time()

    links_from_all_pages = []
    links_from_all_pages += spider(MAIN_URL)
    for page in range(2, 51):
        links_from_all_pages += spider(MAIN_URL + 'page' + str(page) + '/')
        print(str(page) + ' page done')     # 80 sec
    print(f"\nAll links was scraped by {time() - start} s.\n")
    #exit()

    test_words = []
    n = 1
    for i in links_from_all_pages:
        test_words += parser(i)
        print(n, "link from all", len(links_from_all_pages))
        n += 1
    print()
    dict = create_dict(clean_up_list(test_words, prepositions, symbols))
    sorted_word_list = sorted(dict.items(), key=itemgetter(1))
    print(sorted_word_list[-10:-1]) # 1354
    # nn = get_key(dict, max(dict.values())) # выводит первое встреченное многоповторяющееся слово
    # print(nn)


if __name__ == '__main__':
    main()
