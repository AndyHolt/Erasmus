#!/usr/local/bin/python
"""
Get a Bible passage from Bible Gateway.
"""
# Author: Andy Holt
# Date: Sat 03 Oct 2015 18:35

import requests
from bs4 import BeautifulSoup
import re
import click

@click.command()
@click.option('-p', '--passage', default='Genesis 1:1',
              help='Bible passage to get.')
@click.option('-v', '--version', default='ESVUK', help='Translation(s) to get.')
def bible_scraper_cli(passage, version):
    """Get a Bible passage from BibleGateway.com.

    Get's PASSAGE in translation VERSION where VERSION may be a semi-colon
    separated list of versions within a string.

    bible_scraper_cli provides a command line interface to bible_scraper"""
    bible_scraper(passage, version)

def bible_scraper(passage, version):
    """Get a Bible passage from BibleGateway.com.

    Get's PASSAGE in translation VERSION where VERSION may be a semi-colon
    separated list of versions within a string."""

    # parse version and passage names for output filenames
    versions_list = re.split(r';', version)
    passage_name = re.sub(r'([1-3]*\s*[A-Za-z]{1,3})[A-Za-z]*\s*',
                          r'\1',
                          passage, flags=re.UNICODE)
    passage_name = re.sub(r':', r'_', passage_name, flags=re.UNICODE)
    passage_name = re.sub(r'\s', r'', passage_name, flags=re.UNICODE)

    # get page html code from biblegateway.com
    options = {'search': passage, 'version': version}
    url = 'https://www.biblegateway.com/passage/'
    r = requests.get(url, options)

    # parse html and extract the bible text
    page_html = BeautifulSoup(r.text, "html.parser")
    translations_long_passage_list = page_html.find_all(class_="passage-text")

    loopcount = 0
    for translation in translations_long_passage_list:
        passage = translation.find_all("p")

        # prepare list for paragraph texts
        paragraph_text = []

        # for each paragrah (except last one, which is just copyright statement),
        # reformat
        for paragraph in passage[:-1]:
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
        filename = passage_name + versions_list[loopcount] + '.txt'
        loopcount += 1
        with open(filename, 'a') as f:
            for paragraph in paragraph_text[:-1]:
                f.write(paragraph.encode('utf8'))
                f.write('\n')
                f.write('\n')
            f.write(paragraph_text[-1].encode('utf8'))

if __name__ == '__main__':
    bible_scraper_cli()
