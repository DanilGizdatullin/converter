# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:21:32 2015

@author: Daniel
"""
import requests
from ebooklib import epub
import os
#from PIL import Image
#from StringIO import StringIO

def FromJsonToEpub(url, directory, id):
    #  url - link to an article in json format,
    #  directory - directory for the new epub file
    r = requests.get(url, verify=False)
    data = r.json()
    
    #  title - article title on meduza usually consists of 2 titles
    try:
        title = data['root']['title'] + u' ' + data['root']['second_title']
        file_name = data['root']['second_title']
    except KeyError:
        title = data['root']['title']
        file_name = title
    
    #  Author - author of the article,
    #  if not specified, the default is Unknown
    try:
        author = data['root']['authors'][0][0]
    except IndexError:
        author = u'Unknown'
    
    #  store our epub book in book variable
    book = epub.EpubBook()
    
    #  set metadata
    #  id,например, тоже модно передавать как параметр функции
    book.set_identifier('id'+str(id))
    book.set_title(title)
    book.set_language('ru')
    book.add_author(author)
    
    # create chapter
    c1 = epub.EpubHtml(title='Paper', file_name='chap1.xhtml', lang='ru')
    c1.content=data['root']['content']['body']
    
    # add chapter
    book.add_item(c1)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())


    # basic spine
    book.spine = ['nav', c1]
    
    # remove if file already exists
    try:
        os.remove(directory + 'test_book.epub')
    except WindowsError:
        print("Directory does not exsist")        
        
    # write to the file
    epub.write_epub(directory + file_name +'.epub', book, {})
    
FromJsonToEpub('https://meduza.io/api/v3/feature/2015/03/11/ya-gotov-prinyat-lyuboy-rezhim-esli-razum-i-telo-budut-svobodny','C://AOT//',1)
#FromJsonToEpub('https://meduza.io/api/v3/shapito/2015/03/27/akula-ubila-morskuyu-vydru-olivku','C://AOT//',1)
#FromJsonToEpub('https://meduza.io/api/v3/feature/2015/03/27/layk-na-sher-natyanu','C://AOT//',5)