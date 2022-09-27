from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import requests

title_list = []
author_list = []
abstract_list = []
tag_list = []
complete_version_list = []
article_link = []

def geraExcel():
    print('Arquivo em xlsx sendo gerado.')
    df = pd.DataFrame({
        'Titles': title_list,
        'Authors': author_list,
        'Abstract': abstract_list,
        'Tags': tag_list,
        'Complete Version': complete_version_list
    })

    df.to_excel('artigos.xlsx', index=False)
    print('Arquivo gerado.')

def getInfo(url):
    n = 0
    for i in url:
        source = requests.get(i).text
        soup = BeautifulSoup(source, 'html.parser')
        if soup.find_all(id = 'articleTitle'):
            title = soup.find_all(id = 'articleTitle')
            for item in title:
                title_list.append(item.find('h3').text)
        else:
            title_list.append('Title not found.')

        if soup.find_all(id = 'authorString'):
            author = soup.find_all(id = 'authorString')
            for item in author:
                author_list.append(item.find('em').text)
        else:
            author_list.append('Author not found.')

        if soup.find_all(id = 'articleAbstract'):
            background = soup.find_all(id = 'articleAbstract')
            for item in background:
                abstract_list.append(item.find('div').text)
        else:
            abstract_list.append('Abstract not found.')

        if soup.find_all(id = 'articleSubject'):
            tags = soup.find_all(id = 'articleSubject')
            for item in tags:
                tag_list.append(item.find('div').text)
        else:
            tag_list.append('Tags not found.')

        if soup.find_all(id = 'articleFullText'):
            pdf = soup.find_all(id = 'articleFullText')
            for item in pdf:
                complete_version_list.append(item.find('a').attrs['href'])
        else:
            complete_version_list.append('Pdf not found.')
        n+=1
        print(f'Artigos raspados: {n} de {len(url)}.')
    geraExcel()

def getArticlesWithCovers(cover_magazines):
    size = len(cover_magazines)
    sites_scraped = 0
    for i in cover_magazines:
        source = requests.get(i).text
        soup = BeautifulSoup(source, 'html.parser')
        try:
            title = soup.find_all('div', {'class': 'tocTitle'})
            for link in title:
                article_link.append(link.find('a').attrs['href'])
        except:
            None
        sites_scraped+=1
    print(f'Revistas com cover raspadas: {sites_scraped} de {size}.\n',
    'Todas revistas com cover foram raspadas!\nVoltando a executar módulo de raspagem das revistas...')

def getArticles(magazines):
    size = len(magazines)
    sites_scraped = 0
    
    cover_magazines = []
    for i in magazines:
        source = requests.get(i).text
        soup = BeautifulSoup(source, 'html.parser')
        try:
            title = soup.find_all('div', {'class': 'tocTitle'})
            for link in title:
                article_link.append(link.find('a').attrs['href'])
        except:
            None
        if soup.find(id = 'issueCoverImage'):
            for link in soup.find(id = 'issueCoverImage'):
                cover_magazines.append(link.attrs['href'])
        sites_scraped+=1
    print('Tamanho da cover_magazines', len(cover_magazines))
    if len(cover_magazines) != 0 :
        print('Começando a raspar as revistas nas quais apresentam foto.')
        getArticlesWithCovers(cover_magazines)
    
    print(f'Revistas raspadas: {sites_scraped} de {size}')
    print('Todas revistas foram raspadas!\nIniciando módulo para raspar os dados dos artigos...') 
    getInfo(article_link)

def getMagazines(url):
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    page.is_visible('div.tile-body')
    condition = page.url
    try:
        next_page = page.locator("text=>").nth(1).get_attribute('href')
        last_page = page.locator("text=/.*\\>\\>.*/").get_attribute('href')
    except:
        next_page_exists = False
    magazines = []
    while condition != None:
        url = page.inner_html('#issues')
        soup = BeautifulSoup(url, 'html.parser')
        if next_page_exists != False:
            if last_page == page.url:
                previous_page = page.locator("text=<").nth(1).get_attribute('href')
                for all_links in soup.find_all('a'):
                    if all_links.attrs['href'] != previous_page:
                        magazines.append(all_links.attrs['href'])
                condition = None
            else:
                next_page = page.locator("text=>").nth(1).get_attribute('href')
                for all_links in soup.find_all('a'):
                    if all_links.attrs['href'] != next_page:
                        magazines.append(all_links.attrs['href'])
                page.locator("text=>").nth(1).click()
        else:
            for all_links in soup.find_all('a'):
                magazines.append(all_links.attrs['href'])
                condition = None
    page.close()
    print('Todos os links das revistas foram raspados.')
    getArticles(magazines)

with sync_playwright() as p:
    getMagazines('http://www.periodicos.ulbra.br/index.php/ic/issue/archive')
