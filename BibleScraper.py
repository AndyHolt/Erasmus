#!/usr/bin/python
"""
Get a Bible passage from Bible Gateway.
"""
# Author: Andy Holt
# Date: Sat 03 Oct 2015 18:35

import requests
from bs4 import BeautifulSoup
import re

passage = 'Galatians 3:1-4:7'
version = 'ESVUK'

# get page html code from biblegateway.com
options = {'search': passage, 'version': version}
url = 'https://www.biblegateway.com/passage/'
r = requests.get(url, options)

# parse html and extract the bible text
page_html = BeautifulSoup(r.text, "html.parser")
passage_html_long = page_html.find(class_="passage-text")
passage_html = passage_html_long.find_all("p")

# prepare list for paragraph texts
paragraph_text = []

# for each paragrah (except last one, which is just copyright statement),
# reformat
for paragraph in passage_html[:-1]:
    # remove crossreferences
    # [todo] - add crossreferences as optional paratext element
    [c.decompose() for c in paragraph.find_all("sup", class_="crossreference")]

    # remove footnotes
    # [todo] - add footnotes as optional paratext element
    [f.decompose() for f in paragraph.find_all("sup", class_="footnote")]

    # latexify chapter numbers
    for c in paragraph.find_all(class_="chapternum"):
        chap_no = c.string
        ltx_chap_no = re.sub(r'([0-9]+)\s',
                             r'\\cn{\1}',
                             chap_no,
                             flags=re.UNICODE)
        c.string = ltx_chap_no

    # latexify verse numbers
    for v in paragraph.find_all(class_="versenum"):
        verse_no = v.string
        ltx_verse_no = re.sub(r'([0-9]+)\s',
                              r'\\vn{\1}',
                              verse_no,
                              flags=re.UNICODE)
        v.string = ltx_verse_no

    # extract text from html
    paragraph_text.append(paragraph.get_text())


# save to file
# f = open('gal3_16esvuk.html', 'w')
# f.write(passage_text.encode('utf8'))
# f.close
with open('gal3_16esvuk.html', 'a') as f:
    for paragraph in paragraph_text[:-1]:
        f.write(paragraph.encode('utf8'))
        f.write('\n')
        f.write('\n')
    f.write(paragraph_text[-1].encode('utf8'))
