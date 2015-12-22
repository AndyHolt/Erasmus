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

def generate_polyglot(passage, version):
    """Generate a polyglot LaTeX file of PASSAGE in VERSIONS.
    
    Requires files of correct name with content to be placed in the
    directory. These should be generated using BibleScraper.py.
    """
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
            'no_of_translations': len(version_list)}

    input_files = [passage_name + v + '.txt' for v in version_list]

    # get the texts from the input files
    # [todo] - first check the files exist?
    translations = []
    for index, file in enumerate(input_files):
        with codecs.open(file, mode='r', encoding='utf-8') as f:
            translation = {'name': version_list[index],
                           'text': f.read()}
        translations.append(translation)

    # create LaTeX document
    polyglot_renderer = jinja2.Environment(block_start_string = '%{',
                                           block_end_string = '%}',
                                           variable_start_string = '%{{',
                                           variable_end_string = '%}}',
                                           loader = jinja2.FileSystemLoader('.'))

    template = polyglot_renderer.get_template('polyglot_template.tex')

    with codecs.open(meta['filename'], mode='w', encoding='utf-8') as f:
        f.write(template.render(meta=meta, translations = translations))

if __name__ == '__main__':
    generate_polyglot_cli()
