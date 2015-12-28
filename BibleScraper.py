#!/usr/local/bin/python
"""
Get a Bible passage from Bible Gateway.
"""
# Author: Andy Holt
# Date: Sat 03 Oct 2015 18:35

import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag as bs4Tag
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

    # prepare list for translation texts
    translation_texts = []

    # prepare list for first-verse-in-paragraph lists
    first_verse_in_paragraph = []

    for index, translation in enumerate(translations_long_passage_list):
        passage = translation.find_all("p")

        # prepare list for paragraph texts
        paragraph_text = []

        # prepare list for first-verse-in-paragraphs
        first_verse_this_translation = []

        # for each paragrah (except last one, which is just copyright statement),
        # reformat
        for paragraph in passage[:-1]:
            # remove crossreferences
            # [todo] - add crossreferences as optional paratext element
            ([c.decompose()
              for c in paragraph.find_all("sup", class_="crossreference")])

            # remove footnotes
            # [todo] - add footnotes as optional paratext element
            ([f.decompose()
              for f in paragraph.find_all("sup", class_="footnote")])

            # for each paragraph, put first verse number in list
            if (isinstance(paragraph.next_element.next_element, bs4Tag)
                and 'versenum' in paragraph.next_element.next_element['class']):
                first_verse_this_translation.append(
                    int(paragraph.next_element.next_element.string))

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

            # if paragraph is poetry, latexify it as poetry
            if 'poetry' in paragraph.parent['class']:
                # add \begin{verse} command as first thing in paragraph
                paragraph.contents[0].insert_before("\\begin{verse}\n")
                # add \end{verse} command as last thing in paragraph
                paragraph.contents[-1].insert_after(" \\\\\n\\end{verse}")
                # latexify linebreaks
                [br.replace_with(" \\\\\n") for br in paragraph.find_all("br")]
                # latexify indents
                # for indent in paragraph.find_all("span", class_="indent-1"):
                #     indent.contents[0].insert_before("\\vin ")
                for indt in paragraph.find_all("span", class_="indent-1-breaks"):
                    indt.replace_with("\\hspace{1.5em}")

            # extract text from html
            paragraph_text.append(paragraph.get_text())

        # append this translation to translation texts
        translation_texts.append(paragraph_text)

        # append this translation's first-verse-in-paragraphs to full list
        first_verse_in_paragraph.append(first_verse_this_translation)

    # find intersection of first-verse-in-paragraph lists
    alignment_verses = set(first_verse_in_paragraph[0])
    for aset in first_verse_in_paragraph[1:]:
        alignment_verses = alignment_verses.intersection(set(aset))
    print alignment_verses

    # write a file with verse numbers at which to align polyglot
    alignments_file_name = passage_name + "-".join(versions_list) + '.aln'
    with open(alignments_file_name, 'a') as f:
        for alignment_verse in alignment_verses:
            f.write(str(alignment_verse) + "\n")

    for index, translation in enumerate(translation_texts):
        # save to file
        filename = passage_name + versions_list[index] + '.txt'
        with open(filename, 'a') as f:
            for paragraph in translation[:-1]:
                f.write(paragraph.encode('utf8'))
                f.write('\n')
                f.write('\n')
            f.write(translation[-1].encode('utf8'))

if __name__ == '__main__':
    bible_scraper_cli()
