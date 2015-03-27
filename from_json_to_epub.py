# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:21:32 2015

@author: Daniel
"""
import requests, json
from ebooklib import epub
from PIL import Image
from StringIO import StringIO

f = open('C://AOT//Body.txt','w')

url = 'https://meduza.io/api/v3/feature/2015/03/11/ya-gotov-prinyat-lyuboy-rezhim-esli-razum-i-telo-budut-svobodny'
url1 = 'https://meduza.io/api/v3/feature/2015/03/27/kogda-v-strane-idet-voyna-zakon-nelzya-ne-narushat'


r = requests.get(url, verify=False)
data = r.json()
print(data['root'].keys())
title = data['root']['title'] + u' ' + data['root']['second_title']

#print(data['root']['gallery'][0]['large_url'])

try:
    author = data['root']['authors'][0][0]
except IndexError:
    author = u'Unknown'
#print(type(data['root']['content']['body']))

#  ['root']['content']['body'] - лежит основной текст статьи
#  он представляет собой просто html файл

#f.write(data['root']['content']['body'].encode('utf8'))



f.close()
url_pic = 'https://meduza.io/image/attachments/images/000/006/937/small/CAn3yEzN254pD5ffe-r2ig.jpg'
response = requests.get(url_pic, verify = False)
img =Image.open(StringIO(response.content))

book = epub.EpubBook()

# set metadata
book.set_identifier('id1')
book.set_title(title)
book.set_language('ru')


book.add_author(author)
#book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')

# create chapter
c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='ru')
c1.content=data['root']['content']['body']


c2 = epub.EpubHtml(title='Intro1', file_name='chap_02.xhtml', lang='ru')
c2.content=data['root']['content']['body']
#c2 = epub.EpubImage()
#c2.content=img

# add chapter
book.add_item(c1)
book.add_item(c2)




# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
#style = 'BODY {color: white;}'
#nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
#book.add_item(nav_css)

# basic spine
book.spine = ['nav', c1,c2]

# write to the file
epub.write_epub('C://AOT//test1.epub', book, {})

book1 = epub.read_epub('C://AOT//test1.epub')
#for image in book1.get_items_of_type(epub.IMAGE_MEDIA_TYPES):
#    print image
#for i in book1.get_items():
#    print i
#print r.json()
