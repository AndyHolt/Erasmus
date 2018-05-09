#!/usr/local/bin/python
"""
Get whole Bible from Bible gateway and save in text files.

"""
# Author: Andy Holt
# Date: Wed 30 Dec 2015 00:39

import os
from BibleScraper import bible_scraper

translation = 'NIVUK'

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

# for testing!
# books_chapters_list = [['Genesis', 50], ['Exodus', 40], ['Leviticus', 27],
#                        ['Numbers', 36], ['Deuteronomy', 34],
#                        ['Matthew', 28], ['Mark', 16]]

for bk_index, book in enumerate(books_chapters_list):
    dir_name = str(bk_index+1).zfill(2) + "_" + book[0]
    os.chdir('/Users/adh/Bible/NIV/')
    os.mkdir(dir_name)
    os.chdir(dir_name)
    for chap in range(1, book[1]+1):
        if book[0] == 'Psalms':
            pad = 3
        else:
            pad = 2
        passage = book[0] + str(chap).zfill(pad)
        bible_scraper(passage, translation, 'text', verbose=True)
