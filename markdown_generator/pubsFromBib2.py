#!/usr/bin/env python

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# the bib file is generated automatically by Zotero
with open('Papers.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

writer = BibTexWriter()

with open('../_pages/publications_list.md', 'wb') as md_file:
    sorted_entries =  sorted(bib_database.entries,key=lambda x: x['year'], reverse=True)


    for bib_item in sorted_entries:
        if 'booktitle' in bib_item:
            venue = u', {}'.format(bib_item['booktitle']).replace('{','').replace('}','')
        elif bib_item['journal']:
            venue = u', {}'.format(bib_item['journal'])
        else:
            venue = u''

        if 'pages' in bib_item:
            pages = u', {}'.format(bib_item['pages'])
        else:
            pages = u''

        if 'file' in bib_item:
            pdf_link = u' [PDF]({})'.format(bib_item['file'].split(':')[1])
        else:
            pdf_link = u''

        # create bibtex file
        db = BibDatabase()
        db.entries = [bib_item]
        bib_file = 'bib/{0}.bib'.format(bib_item['ID'])
        bib_link = u' [bib]({})'.format(bib_file)
        with open('publications/{0}'.format(bib_file), 'wb') as bib:
            bib.write(writer.write(db).encode('UTF-8'))

        md_file.write(u"- {0} *{1}* ({2}){3}{4} {5} {6}\n".format(bib_item['author'],bib_item['title'].replace('{','').replace('}',''),
                                                                                                                            bib_item['year'],
                                                                                                                            venue,
                                                                                                                            pages,
                                                                                                                            pdf_link,
                                                                                                                            bib_link).encode('UTF-8'))
