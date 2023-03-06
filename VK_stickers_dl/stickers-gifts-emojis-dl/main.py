from bs4 import BeautifulSoup as BS
from datetime import datetime
from pprint import pprint
import requests
import shutil
import json
import os, sys, time

import _thread
from threading import Thread
from multiprocessing import Process

BASE_URL = 'https://vkclub.su'
dir = 'path\\to\\your\\download\\dir'
###############################################################################

def get_html(URL):
    r = requests.get(url=URL)
    html = BS(r.text, 'lxml')
    return html

def get_pagination(URL):
    html = get_html(URL)
    pagination = int(html.select('.pagination > a')[-1].text)
    return pagination

    
def get_sticker_pack_urls():
    if not os.path.exists(f'{dir}\\data'):
        os.mkdir(f'{dir}\\data')
            
    last_page = get_pagination('https://vkclub.su/ru/stickers/')
    
    sticker_pack_url_list = []
    for page in range(0, last_page):
        print(f'{"-" * 10} Collect page {page+1} / {last_page} {"-" * 10}')
        
        STICKERS_URL = f'{BASE_URL}/ru/stickers/?sortby=alphabet&page={page}'
        
        html = get_html(STICKERS_URL)
        sticker_pack = html.select('.collections_list_item')
    
        for n in range(len(sticker_pack)):
            sticker_pack_title = html.select('.textsblock > .title > a')[n]['title'].replace(': ', '-')[11:]
        
            if os.path.exists(f'{dir}\\Вк Стикеры\\{sticker_pack_title}'):
                break
            else:
                sticker_pack_url = BASE_URL + html.select('.textsblock > .title > a')[n]['href']
                sticker_pack_url_list.append(sticker_pack_url)
                print(sticker_pack_title)
        
    # save to file
    with open(f'{dir}\\data\\sticker_pack_url_list.json', "w", encoding="utf-8") as f:
        json.dump(sticker_pack_url_list, f, ensure_ascii=False, indent=4)
    
    print("-" * 20)
    print(f'Saved in "{dir}\data\sticker_pack_url_list.json" ')


def dl_stickers():
    if not os.path.exists(f'{dir}\\Вк Стикеры'):
        os.mkdir(f'{dir}\\Вк Стикеры')
    
    with open(f"{dir}\\data\\sticker_pack_url_list.json", encoding='utf-8') as file:
        sticker_links = json.load(file)
    
    for link in sticker_links:
        html = get_html(link)
        
        sticker_item = html.select('.stickers_list_item')
        sticker_pack_title = html.select('.collection_info > div > h3')[0].text[22:].replace(': ', '-')
        print(f'Загружается - {sticker_pack_title}')
        
        if not os.path.exists(f'{dir}\\Вк Стикеры\\{sticker_pack_title}'):
            os.mkdir(f'{dir}\\Вк Стикеры\\{sticker_pack_title}')
            print(f'[INF] Создана папка для: {sticker_pack_title}')
            
        for n in range(len(sticker_item)):
            sticker_link = BASE_URL + html.select('.stickers_list_item > a > img')[n]['src']
            sticker_name = sticker_link.split('_')[-1]
            
            r = requests.get(sticker_link)
            sticker_image = open(f'{dir}\\Вк Стикеры\\{sticker_pack_title}\\{sticker_name}', 'wb')
            sticker_image.write(r.content)
            sticker_image.close()
            print(f'[sticker] {sticker_pack_title} {sticker_name}')


def dl_gifts():
    if not os.path.exists(f'{dir}\\Вк Подарки'):
        os.mkdir(f'{dir}\\Вк Подарки')
        
    last_page = get_pagination('https://vkclub.su/ru/gifts/')
    for page in range(0, last_page):
        
        GIFTS_URL = f'{BASE_URL}/ru/gifts/?sortby=date&page={page}'
        html = get_html(GIFTS_URL)
        
        gifts = html.select('.giftcat_list_item')
        print(f'{"-" * 10} Collect gifts, page {page + 1} / {last_page} {"-" * 10}')
        for n in range(len(gifts)):
            gift_link = BASE_URL + html.select('.image > img')[n]['src']
            gift_name = gift_link.split('/')[-1]
            
            r = requests.get(gift_link)
            gift_image = open(f'{dir}\\Вк Подарки\\{gift_name}', 'wb')
            gift_image.write(r.content)
            gift_image.close()
            
            total_gifts = int(f'{int(len(gifts)) * int(last_page)}')
            print(f'[gift] {total_gifts - (total_gifts - n) } / {total_gifts}')
            

def dl_emojis():
    if not os.path.exists(f'{dir}\\Вк Емоджи'):
        os.mkdir(f'{dir}\\Вк Емоджи')    
    
    url = 'https://vkclub.su/ru/emojis/'
    html = get_html(url)
    
    emoji_pack_urls_list = []
    emoji_pack_urls = html.select('.emojicats_list_item > div > div > a')
    
    for url in emoji_pack_urls:
        emoji_pack_urls_list.append(url['href'])
    
    for emoji in emoji_pack_urls_list:
        EMOJIS_URL = f'{BASE_URL}{emoji}'
    
        html = get_html(EMOJIS_URL)
        emojis = html.select('.emojicat_list_item')
        for e, emoji in enumerate(emojis):
            emoji_link = 'https:' + emoji.select('div > div > a > img')[0]['data-image']
            emoji_code = emoji.select('div > div > a > img')[0]['alt'][0]
            emoji_group = html.select('.emojicat_list_item > div > div > a')[0]['href'].split('/')[-3]
            
            r = requests.get(emoji_link)
            emoji_image = open(f'{dir}\\Вк Емоджи\\{emoji_code.replace("*", "-")} {emoji_group}-{e+1}.png', 'wb')
            emoji_image.write(r.content)
            emoji_image.close()
            print(f'[emoji] {emoji_code} {emoji_group}-{e+1}')
        
if __name__ == "__main__":
    # if not os.path.exists(f'{dir}\\data\\sticker_pack_url_list.json'):
    #     get_sticker_pack_urls()

    thread_stickers = Process(target=dl_stickers)
    thread_gifts = Process(target=dl_gifts)
    thread_emojis = Process(target=dl_emojis)
    
    thread_stickers.start()
    thread_gifts.start()
    thread_emojis.start()
    
    thread_stickers.join()
    thread_gifts.join()
    thread_emojis.join()