# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 19:11:00 2020

@author: sshamsie
"""

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


def bach(wik, page):
    hd_bach = ['#', 'Original run', 'Bachelor', 'Winner', 'Runner(s)-up', 'Proposal', 'Still together', 'Relationship notes']
    cols = ['season', 'dates', 'bachelor', 'winner', 'runner-up', 'proposal', 'together', 'notes']
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
        
        try:
            if headings[:8] == hd_bach:
                with open('iso_3166-1_alpha-2_codes.txt', 'w', encoding='utf-8') as fo:
                    for tr in t.find_all('tr'):
                        tds = tr.find_all('td')
                        if not tds:
                            continue
                        data.append([td.text.strip() for td in tds[:8]])
        except:
            data = None

        if data is not None:
            bachelors = pd.DataFrame(data, columns = cols)
            bachelors = bachelors[bachelors['season'].apply(lambda x: x.isnumeric())]
            return bachelors


def cont(wik, page):
    hd_cont = ['Name', 'Age', 'Hometown']
    cols = ['name', 'age', 'hometown', 'occupation', 'result']
    data = []
    contestants = pd.DataFrame(columns = cols)
    
    for p in page:
        url = wik + p.replace(' ', '_')
        req = urllib.request.urlopen(url)
        article = req.read().decode()
        data = []
        contestants = pd.DataFrame(columns = cols)

        with open('ISO_3166-1_alpha-2.html', 'w', encoding='utf-8') as fo:
            fo.write(article)

        html = open('ISO_3166-1_alpha-2.html', encoding='utf-8').read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')

        for t in tables:
            ths = t.find_all('th')
            headings = [th.text.strip() for th in ths]

            try:
                if headings[:3] == hd_cont:
                    with open('iso_3166-1_alpha-2_codes.txt', 'w', encoding='utf-8') as fo:
                        for tr in t.find_all('tr'):
                            tds = tr.find_all('td')
                            if not tds:
                                continue
                            data.append([td.text.strip() for td in tds[:5]])
            except:
                data = None

            if data is not None:
                df = pd.DataFrame(data, columns = cols)
                df['season'] = p.split(' ')[3].split(')')[0]
                contestants = contestants.append(df)
    return contestants

#create dataframes            
wik = 'https://en.wikipedia.org/wiki/'
bach_home = 'The Bachelor (American TV series)'
bach_seasons = ['The Bachelor (season {})'.format(s) for s in list(range(1,25))]


cont = cont(wik, pages[1:])
