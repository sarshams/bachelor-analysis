# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 19:11:00 2020

@author: sshamsie
"""
#import statements
import pandas as pd
import wikipedia
from bs4 import BeautifulSoup
import urllib.request
import numpy as np
import re


'''
this function gets lead data from wikipedia
@params - wiki title, subpage, heading
@returns - pandas df of leads
'''


def get_lead_data(wik, page, head):
    cols = ['season', 'dates', 'bachelor', 'winner',
            'runner-up', 'proposal', 'together', 'notes']
    leads = pd.DataFrame(columns=cols)
    url = wik + page.replace(' ', '_')
    req = urllib.request.urlopen(url)
    article = req.read().decode()
    data = []

    with open('ISO_3166-1_alpha-2.html', 'w', encoding='utf-8') as fo:
        fo.write(article)

    html = open('ISO_3166-1_alpha-2.html', encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    for t in tables:
        ths = t.find_all('th')
        headings = [th.text.strip() for th in ths]
        print(headings[:8])

        try:
            if headings[:8] == head:
                with open('iso_3166-1_alpha-2_codes.txt', 'w', encoding='utf-8') as fo:
                    for tr in t.find_all('tr'):
                        tds = tr.find_all('td')
                        if not tds:
                            continue
                        data.append([td.text.strip() for td in tds[:8]])
                ret_df = pd.DataFrame(data, columns=cols)
                leads = leads.append(ret_df, sort=True)

        except:
            ret_df = pd.DataFrame(columns=cols)

    leads = leads[leads['season'].apply(lambda x: x.isnumeric())]

    return leads


'''
this function gets contestant data
@params - wiki title, subpage, heading
@returns - pandas df of contestants
'''


def get_contestant_data(wik, page, head):
    cols = ['name', 'age', 'hometown', 'occupation', 'result']
    contestants = pd.DataFrame(columns=cols + ['season'])

    for p in range(len(page)):
        url = wik + page[p].replace(' ', '_')
        req = urllib.request.urlopen(url)
        article = req.read().decode()
        data = []

        with open('ISO_3166-1_alpha-2.html', 'w', encoding='utf-8') as fo:
            fo.write(article)

        html = open('ISO_3166-1_alpha-2.html', encoding='utf-8').read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')

        for t in tables:
            ths = t.find_all('th')
            headings = [th.text.strip() for th in ths]

            try:
                if headings[:3] == head:
                    with open('iso_3166-1_alpha-2_codes.txt', 'w', encoding='utf-8') as fo:
                        for tr in t.find_all('tr'):
                            tds = tr.find_all('td')
                            if not tds:
                                continue
                            data.append([td.text.strip() for td in tds[:5]])
                    ret_df = pd.DataFrame(data, columns=cols)
                    ret_df['season'] = page[p].split(' ')[3].split(')')[0]
                    contestants = contestants.append(ret_df, sort=True)

            except:
                ret_df = pd.DataFrame(columns=cols + ['season'])
                contestants = contestants.append(ret_df, sort=True)

    return contestants

    '''
    this function cleans numeric data for contestant age
    @params - subpage
    @returns - pandas df of age
    '''
    def clean_age(page):
        keys = ['year-old', 'year old', 'years-old', 'years old']
        cols = ['season', 'age']
        ages = pd.DataFrame(columns=cols)
        data = []

        for p in page:
            content = wikipedia.WikipediaPage(title=p).summary
            kw = [k for k in keys if k in content]
            season = p.split(' ')[3].split(')')[0]

            if len(kw) != 0:
                if '-' in kw[0]:
                    age = content[content.index(
                        kw[0])-3:content.index(kw[0])+4].split('-')[0]
                    data.append([season, age])
                    ret_df = pd.DataFrame(data, columns=cols)
                else:
                    age = content[content.index(
                        kw[0])-3:content.index(kw[0])+4].split(' ')[0]
                    data.append([season, age])
                    ret_df = pd.DataFrame(data, columns=cols)
            else:
                age = None
                data.append([season, age])
                ret_df = pd.DataFrame(data, columns=cols)

        return ages

    '''
    this function cleans hyperlinks that have copied over
    @params - a row in the df
    @returns - string
    '''
    def remove_brackets(d):
        return d.apply(lambda x: x.str.replace(r"\[.*\]", ""))

#text data and parameters          
wiki = 'https://en.wikipedia.org/wiki/'
bach_home = 'The Bachelor (American TV series)'
bach_seasons = ['The Bachelor (season {})'.format(s) for s in list(range(1,25))]
ette_home = 'The Bachelorette'
ette_seasons = ['The Bachelorette (season {})'.format(s) for s in list(range(1,16))]
bach_cols = ['#', 'Original run', 'Bachelor', 'Winner', 'Runner(s)-up', 'Proposal', 'Still together', 'Relationship notes']
ette_cols = ['#', 'Original run', 'Bachelorette', 'Winner', 'Runner-up', 'Proposal', 'Still together', 'Relationship notes']
contestant_cols = ['Name', 'Age', 'Hometown']