#!/usr/bin/python
"""
Get a Bible passage from Bible Gateway.
"""
# Author: Andy Holt
# Date: Sat 03 Oct 2015 18:35

import requests
from bs4 import BeautifulSoup
import re

passage = 'Genesis 1:1'
version = 'ESVUK'

# get page html code from biblegateway.com
options = {'search': passage, 'version': version}
url = 'https://www.biblegateway.com/passage/'
r = requests.get(url, options)

# parse html and extract the bible text
page_html = BeautifulSoup(r.text, "html.parser")
passage_html_long = page_html.find(class_="passage-text")
passage_html = passage_html_long.find("p")

# remove crossreferences
[c.decompose() for c in passage_html.find_all("sup", class_="crossreference")]

# latexify chapter numbers
for c in passage_html.find_all(class_="chapternum"):
    chap_no = c.string
    ltx_chap_no = re.sub(r'([0-9]+)\s',
                         r'\\cn{\1}',
                         chap_no,
                         flags=re.UNICODE)
    c.string = ltx_chap_no

# latexify verse numbers
for v in passage_html.find_all(class_="versenum"):
    verse_no = v.string
    ltx_verse_no = re.sub(r'([0-9]+)\s',
                          r'\\vn{\1}',
                          verse_no,
                          flags=re.UNICODE)
    v.string = ltx_verse_no

# extract text from html
passage_text = passage_html.get_text()

# save to file
f = open('gal3_16esvuk.html', 'w')
f.write(passage_text.encode('utf8'))
f.close
