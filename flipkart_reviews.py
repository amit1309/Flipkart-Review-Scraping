# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 18:40:46 2019

@author: amit
"""

from requests import get
import bs4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
import time
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

flipkart_url = 'https://www.flipkart.com/honor-band-5/p/itmfggx9g4dpep7j?pid=SBNFGGX96QYXNW5R&srno=s_1_1&otracker=search&otracker1=search&lid=LSTSBNFGGX96QYXNW5RXXO1FU&fm=SEARCH&iid=0c55e23a-e3d8-40a4-91ac-c8bbdc04d306.SBNFGGX96QYXNW5R.SEARCH&ppt=sp&ppn=sp&ssid=6p9cw8cz1zsu6olc1568562917258&qH=19e879f085370a38'
browser = webdriver.Chrome()

browser.get(flipkart_url)
comment_title = []
comment_text = []
comment_rating = []
first_iteration = True

while True:
    try:
        if first_iteration:
            all_reviews_button = browser.find_element_by_css_selector('#container > div > div.t-0M7P._3GgMx1._2doH3V > div._3e7xtJ > div._1HmYoV.hCUpcT > div._1HmYoV._35HD7C.col-8-12 > div._1HmYoV._35HD7C > div:nth-child(7) > div > a > div > span')
            all_reviews_button.click()
            time.sleep(2)
            read_more_button = browser.find_elements_by_class_name('_1EPkIx')
            [item.click() for item in read_more_button]
            first_iteration = False
        else:
            next_page_button = browser.find_element_by_link_text('NEXT')
            next_page_button.click()
            time.sleep(2)
            read_more_button = browser.find_elements_by_class_name('_1EPkIx')
            [item.click() for item in read_more_button]
        soup_obj = bs4.BeautifulSoup(browser.page_source)
        intermediate_titles = [item.get_text() for item in soup_obj.find_all('p', class_='_2xg6Ul')]
        comment_title.extend(intermediate_titles)
        intermediate_text = [item.get_text() for item in soup_obj.find_all('div', class_='qwjRop')]
        regex_obj = re.compile(r'READ MORE')
        intermediate_text = [regex_obj.sub('', text).strip() for text in intermediate_text]
        comment_text.extend(intermediate_text)
        intermediate_ratings = [np.float(item.get_text()) for item in soup_obj.find_all('div', class_='hGSR34 E_uFuv')]
        comment_rating.extend(intermediate_ratings)
    except NoSuchElementException:
        print("END")
        browser.quit()
        break


updated_text = []
for item in comment_text:
    item = item.lower()
    updated_text.extend(item.split())
updated_text = [item for item in updated_text if item not in STOPWORDS]
updated_text = [re.sub(r'[^a-zA-Z]', '', item) for item in updated_text]
updated_text = [item for item in updated_text if item!='']

ngram_text = []
for index in range(len(updated_text)-1):
    ngram_text.append('_'.join(updated_text[index: index+3]))


word_cloud_data = WordCloud(width = 4000, height = 4000,
                stopwords = STOPWORDS).generate(' '.join(ngram_text))
plt.figure(figsize=(10,10), facecolor='k')
plt.imshow(word_cloud_data, interpolation='bilinear')
len(comment_text)






