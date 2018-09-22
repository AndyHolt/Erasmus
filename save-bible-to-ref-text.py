#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Get the whole bible from Bible gateway and save to text files.

Each text file is to take a format that can be read into assoc list in Elisp for
easy use to generate the candidates for the helm-bible source.
"""
# Author: Andy Holt
# Date: Sat 22 Sep 2018 13:09

import os
from BibleScraper import bible_scraper

translation = 'ESVUK'

books_chapters_list = [['Genesis', 50], ['Exodus', 40], ['Leviticus', 27],
                       ['Numbers', 36], ['Deuteronomy', 34], ['Joshua', 24],
                       ['Judges', 21], ['Ruth', 4], ['1 Samuel', 31],
                       ['2 Samuel', 24], ['1 Kings', 22], ['2 Kings', 25],
                       ['1 Chronicles', 29], ['2 Chronicles', 36], ['Ezra', 10],
                       ['Nehemiah', 13], ['Esther', 10], ['Job', 42],
                       ['Psalms', 150], ['Proverbs', 31], ['Ecclesiastes', 12],
                       ['Song of Songs', 8], ['Isaiah', 66], ['Jeremiah', 52],
                       ['Lamentations', 5], ['Ezekiel', 48], ['Daniel', 12],
                       ['Hosea', 14], ['Joel', 3], ['Amos', 9], ['Obadiah', 1],
                       ['Jonah', 4], ['Micah', 7], ['Nahum', 3],
                       ['Habakkuk', 3], ['Zephaniah', 3], ['Haggai', 2],
                       ['Zechariah', 14], ['Malachi', 4],
                       ['Matthew', 28], ['Mark', 16], ['Luke', 24],
                       ['John', 21], ['Acts', 28], ['Romans', 16],
                       ['1 Corinthians', 16], ['2 Corinthians', 13],
                       ['Galatians', 6], ['Ephesians', 6], ['Philippians', 4],
                       ['Colossians', 4], ['1 Thessalonians', 5],
                       ['2 Thessalonians', 3], ['1 Timothy', 6],
                       ['2 Timothy', 4], ['Titus', 3], ['Philemon', 1],
                       ['Hebrews', 13], ['James', 5], ['1 Peter', 5],
                       ['2 Peter', 3], ['1 John', 5], ['2 John', 1],
                       ['3 John', 1], ['Jude', 1], ['Revelation', 22]]

# Make directory for storing all the files in
os.chdir('/Users/adh/Bible/helm-bible')
os.mkdir('ESV')
os.chdir('ESV')

for bk_index, book in enumerate(books_chapters_list):
    for chap in range(1, book[1]+1):
        if book[0] == 'Psalms':
            pad = 3
        else:
            pad = 2
        passage = book[0] + " " + str(chap).zfill(pad)
        book_no = str(bk_index+1).zfill(2)
        bible_scraper(passage, translation, 'referenced-text', verbose=True, book_no=book_no)
