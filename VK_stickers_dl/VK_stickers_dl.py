import requests
import string, random
import os, sys, time
import httplib2

import _thread
from threading import Thread
from multiprocessing import Process

# https://vk.com/sticker/1-1-512
# https://vk.com/sticker/1-21920-512

# [+] Valid: https://vk.com/sticker/G2U.png
#  https://vk.com/sticker/1-1-512

def vk_stickers_dl_V1():
    THREAD_AMOUNT = int(1)
    INVALID = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]

    def scrape_pictures(thread):
        for sticker_Id in range(1, 21921):

            url = 'https://vk.com/sticker/'
            url += '1-' + (str(sticker_Id)) + '-512' + '.png'
            print(url)

            filename = url.rsplit('/', 1)[-1]

            h = httplib2.Http('.cache' + thread)
            response, content = h.request(url)
            out = open(filename, 'wb')
            out.write(content)
            out.close()

            file_size = os.path.getsize(filename)
            if file_size in INVALID:
                print("[-] Invalid: " + url)
                os.remove(filename)
            else:
                print("[+] Valid: " + url)

    for thread in range(1, THREAD_AMOUNT + 1):
        thread = str(thread)
        try:
            _thread.start_new_thread(scrape_pictures, (thread,))
        except:
            print('Error starting thread ' + thread)
    print('Succesfully started ' + thread + ' threads.')

    while True:
        time.sleep(1)
##############################################################################################
##############################################################################################
def vk_stickers_dl_V2():
    dir = 'C:\\Users\\designer\\Dropbox\\ПК\\Desktop\\python39\\Vk_stickers\\data\\'
    def vk_dl_1():
        for i in range(1, 5001):
            URL = f'https://vk.com/sticker/1-{i}-512'
            r = requests.get(url=URL)
            with open(f'{dir}{i}.png', 'wb') as file:
                file.write(r.content)
            print(r.url)
    
    def vk_dl_2():
        for i in range(5000, 10001):
            URL = f'https://vk.com/sticker/1-{i}-512'
            r = requests.get(url=URL)
            with open(f'{dir}{i}.png', 'wb') as file:
                file.write(r.content)
            print(r.url)
    
    def vk_dl_3():
        for i in range(10000, 15001):
            URL = f'https://vk.com/sticker/1-{i}-512'
            r = requests.get(url=URL)
            with open(f'{dir}{i}.png', 'wb') as file:
                file.write(r.content)
            print(r.url)
    
    def vk_dl_3():
        for i in range(15000, 20001):
            URL = f'https://vk.com/sticker/1-{i}-512'
            r = requests.get(url=URL)
            with open(f'{dir}{i}.png', 'wb') as file:
                file.write(r.content)
            print(r.url)
    
    def vk_dl_4():
        for i in range(20000, 25001):
            URL = f'https://vk.com/sticker/1-{i}-512'
            r = requests.get(url=URL)
            with open(f'{dir}{i}.png', 'wb') as file:
                file.write(r.content)
            print(r.url)
            
    def vk_dl_5():
        for i in range(25000, 30001):
            URL = f'https://vk.com/sticker/1-{i}-512'
            r = requests.get(url=URL)
            with open(f'{dir}{i}.png', 'wb') as file:
                file.write(r.content)
            print(r.url)
    
        thread1 = Process(target=vk_dl_1)
        thread2 = Process(target=vk_dl_2)
        thread3 = Process(target=vk_dl_3)
        thread4 = Process(target=vk_dl_4)
        thread5 = Process(target=vk_dl_5)
        
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
    
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()

if __name__ == '__main__':
    # vk_stickers_dl_V1()
    
    # vk_stickers_dl_V2()