#! /usr/bin/env python

"""
copyright 2010 Marcin Magnus

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from Bio import Entrez
import pdb
import commands
import os
import sys
import re
import cStringIO
import optparse
##
VERSION='0.01'

def dotting(s):
    """ change ' ' into . """
    return s.replace(' ','.')

def underline(s):
    """ change ' ' into _ """
    return s.replace(' ','_')

def upper(s):
    """ upper s, e.g. marcin -> MAGNUS"""
    return s.upper()

def clean_string(s):
    """
    execute operations to clean up a given string
    """
    s=s.replace('..','.') # Magnus..Marcin -> Marcin.Magnus
    s=s.replace('-.','-') # Magnus-.student -> Magnus-student
    return s

def get_title_via_pmid(pmid,v=0):
    """
    GET:
    - pmid of a publication, e.g. 17123955
    - v(erbose) 
    DO:
    - use biopython to get summary dict 
{'DOI': '10.1261/rna.283207', 'Title': 'Conversion of pre-RISC to holo-RISC by Ago2 during assembly of RNAi complexes.', 'Source': 'RNA', 'PmcRefCount': 9, 'Issue': '1', 'SO': '2007 Jan;13(1):22-9', 'ISSN': '1355-8382', 'Volume': '13', 'FullJournalName': 'RNA (New York, N.Y.)', 'RecordStatus': 'PubMed - indexed for MEDLINE', 'ESSN': '1469-9001', 'ELocationID': '', 'Pages': '22-9', 'PubStatus': 'ppublish+epublish', 'AuthorList': ['Kim K', 'Lee YS', 'Carthew RW'], 'EPubDate': '2006 Nov 22', 'PubDate': '2007 Jan', 'NlmUniqueID': '9509184', 'LastAuthor': 'Carthew RW', 'ArticleIds': {'pii': 'rna.283207', 'medline': [], 'pubmed': ['17123955'], 'pmc': 'PMC1705758', 'pmcid': 'pmc-id: PMC1705758;', 'doi': '10.1261/rna.283207'}, u'Item': [], 'History': {'medline': ['2007/01/31 09:00'], 'pubmed': ['2006/11/25 09:00'], 'entrez': '2006/11/25 09:00', 'aheadofprint': '2006/11/22 00:00'}, 'LangList': ['English'], 'HasAbstract': 1, 'References': [], 'PubTypeList': ['Journal Article'], u'Id': '17123955'}

    RETURN:
    - formated title(string)
    !!
    need xclip - http://sourceforge.net/projects/xclip/
    """
    pmid=str(pmid)
    result = Entrez.esummary(db="pubmed", id=pmid)
    summary_dict=Entrez.read(result)[0]

    if v:print summary_dict

    titleOfpub=dotting(summary_dict['Title'].strip())
    title=upper(underline(summary_dict['AuthorList'][0].strip())+'.'+underline(summary_dict['AuthorList'][-1].strip()))+'-'+titleOfpub+'.'+pmid+'.'+str(summary_dict['PubDate'].split()[0])+'.'+upper(dotting(summary_dict['Source']))+'.pdf'
    title=clean_string(title)
    cmd='echo '+title + ' | xclip -selection clipboard'
    if v:print cmd
    os.system(cmd)

    return title

def get_title_via_doi(doi,v=0):
    """
    GET:
    - doi, e.g.
    - v(erbose) 
    DO:
    - search in pubmed a paper based on given doi,
    - get the paper, fetch pmid
    - get_title_via_pmid
    RETURN:
    - title(string)
    """
    doi=str(doi)
    if v:print doi
    result = Entrez.esearch(db="pubmed",term=doi) ## *need to be improved*
    out=Entrez.read(result)
    idlist = out["IdList"]
    return get_title_via_pmid(idlist[0])

def get_options():
    #
    usage="%prog [options] id"
    description="""
examples: pubmex.py -d  17123955, pumex.py -d 10.1038/embor.2008.212
"""
    version=VERSION
    #
    ### DEFAULT OPTIONS ###
    #
    version=VERSION
    #
    p = optparse.OptionParser(description=description,
                              version=version,
                              usage=usage)
    #
    p.add_option("--pubmed_id", "-p", action="store_true",
                help="pass PMID of the paper",metavar="PUBMED_ID",default='')
    p.add_option("--doi", "-d", action="store_true",
                help="pass DOI of the paper",metavar="DOI_ID",default='')
    #
    (options, arguments) = p.parse_args()
    ##print     (options, arguments)
    ##(<Values at 0xb7aab50c: {'doi': '', 'pubmed_id': True}>, ['17123955'])
    ##{'doi': '', 'pubmed_id': True} ['17123955']
    if len(arguments) > 0:
        pass
    else:
        p.print_help()
        sys.exit(1)
    return options,arguments

if '__main__'==__name__:
    options,arguments=get_options()
    if options.pubmed_id:
        print get_title_via_pmid(arguments[0])
    if options.doi:
        print get_title_via_doi(arguments[0])    
