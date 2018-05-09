#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Create a polyglot LaTeX document from bible passage txt files.

Get Bible passages from txt files (e.g. created by BibleScraper) and produce a
polyglot document for processing by LaTeX.
"""
# Author: Andy Holt
# Date: Tue 22 Dec 2015 13:54

import re
import datetime
import codecs
import jinja2
import click

@click.command()
@click.option('-p', '--passage', default='Genesis 1:1',
              help='Bible passage to use.')
@click.option('-v', '--version', default='ESVUK', help='Translation(s) to use.')
def generate_polyglot_cli(passage, version):
    """Generate a polyglot LaTeX file of PASSAGE in VERSIONS.

    Requires files of correct name with content to be placed in the
    directory. These should be generated using BibleScraper.py.

    generate_polyglot_cli provides a command line interface to generate_polyglot"""
    generate_polyglot(passage, version)

def generate_polyglot(passage, version):
    """Generate a polyglot LaTeX file of PASSAGE in VERSIONS.
    
    Requires files of correct name with content to be placed in the
    directory. These should be generated using BibleScraper.py.
    """
    if verbose:
        # print('Constructing polyglot...')
        print 'Constructing polyglot...'

    version_list = re.split(r';', version)
    passage_name = re.sub(r'([1-3]*\s*[A-Za-z]{1,3})[A-Za-z]*\s*',
                          r'\1',
                          passage, flags=re.UNICODE)
    passage_name = re.sub(r':', r'_', passage_name, flags=re.UNICODE)
    passage_name = re.sub(r'\s', r'', passage_name, flags=re.UNICODE)

    # get metadata based on inputs
    meta = {'filename': passage_name + 'Polyglot.tex',
            'passagename': passage,
            'datestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'no_of_translations': len(version_list),
            'translations': version_list}

    input_files = [passage_name + v + '.txt' for v in version_list]

    # get alignments from file
    alignments_file_name = passage_name + "-".join(version_list) + '.aln'
    with open(alignments_file_name, 'r') as f:
        alignments = f.readlines()
    # strip '\n' from alignment strings
    for index, aln in enumerate(alignments):
        alignments[index] = re.sub(r'\n', '', aln)

    # get the texts from the input files
    # [todo] - first check the files exist?
    trans_split_regexp = '|'.join(['(\\\\vn\{' + r + '\})' for r in alignments])

    # get text from input files
    translations = []
    for index, file in enumerate(input_files):
        with codecs.open(file, mode='r', encoding='utf-8') as f:
            # split translation into aligned paragraphs
            a_translation = re.split(trans_split_regexp,
                                     f.read())
            # remove None values caused by regexp
            # [todo] - find way of not creating Nones in regexp split?
            a_translation = filter(None, a_translation)

            # if any new-paragraph-verses are also starts of verses, re-attach
            # '\begin{verse}' to the correct verse
            for index, substr in enumerate(a_translation):
                if re.search(r'\\begin\{verse\}\n$', substr):
                    a_translation[index] = re.sub(r'\\begin\{verse\}\n$',
                                                  '', substr)
                    a_translation[index+1] = ('\\begin{verse}\n'
                                              + a_translation[index+1])

            # reattach verse numbers to their paragraphs (split off by regexp
            # split)
            # print a_translation
            for vn in range(len(a_translation) / 2):
                a_translation[vn+1] = (a_translation[vn+1]
                                               + a_translation[vn+2])
                a_translation.pop(vn+2)
            translations.append(a_translation)

    aligned_paragraphs = zip(*translations)

    # create LaTeX document
    polyglot_renderer = jinja2.Environment(block_start_string = '%{',
                                           block_end_string = '%}',
                                           variable_start_string = '%{{',
                                           variable_end_string = '%}}',
                                           trim_blocks = True,
                                           lstrip_blocks = True,
                                           keep_trailing_newline = True,
                                           loader = jinja2.FileSystemLoader('.'))

    template = polyglot_renderer.get_template('polyglot_template.tex')

    if verbose:
        # print('Writing to ' + meta['filename'] + '...')
        print 'Writing to ' + meta['filename'] + '...'

    with codecs.open(meta['filename'], mode='w', encoding='utf-8') as f:
        f.write(template.render(meta=meta,
                                aligned_paragraphs = aligned_paragraphs))

    if verbose:
        # print('Done.')
        print 'Done.'

if __name__ == '__main__':
    generate_polyglot_cli()
