from operator import index
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

title_list = []
author_list = []
abstract_list = []
tag_list = []
complete_version_list = []
date_list = []

def genCharts():
    '''
    dict = df.to_dict()

    '''
    pass

def genFile():
    def genExcel():
        print('Arquivo em xlsx sendo gerado.')
        df.to_excel('article.xlsx', index=False)

    def genCsv():
        df.to_csv('article.csv', sep=';')

    def genJson():
        df.to_json('article.json')

    df = pd.DataFrame({
            'Titles': title_list,
            'Authors': author_list,
            'Abstract': abstract_list,
            'Tags': tag_list,
            'Complete Version': complete_version_list,
            'Date': date_list
        })

    file_type = int(input('Select an option\n'
    '1 - Excel (article.xlsx)\n'
    '2 - CSV (article.csv)\n'
    '3 - JSON (article.json\n'))

    if file_type == 1:
        genExcel()
    elif file_type == 2:
        genCsv()
    elif file_type == 3:
        genJson()
    else:
        print('Invalid option, please try again and select a valid option.')
        genFile()
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
            title_list.append('Title not found')

        if soup.find_all(id = 'authorString'):
            author = soup.find_all(id = 'authorString')
            for item in author:
                author_list.append(item.find('em').text)
        else:
            author_list.append('Author not found')

        if soup.find_all(id = 'articleAbstract'):
            background = soup.find_all(id = 'articleAbstract')
            for item in background:
                abstract_list.append(item.find('div').text)
        else:
            abstract_list.append('Abstract not found')

        if soup.find_all(id = 'articleSubject'):
            tags = soup.find_all(id = 'articleSubject')
            for item in tags:
                tag_list.append(item.find('div').text)
        else:
            tag_list.append('Tags not found')

        if soup.find_all(id = 'articleFullText'):
            pdf = soup.find_all(id = 'articleFullText')
            for item in pdf:
                complete_version_list.append(item.find('a').attrs['href'])
        else:
            complete_version_list.append('Pdf not found')

        if soup.find_all(id = "breadcrumb"):
            date = soup.find_all(id = "breadcrumb")
            for item in date:
                w = item.find(string=re.compile("v"))
                x = w.find("(") + 1
                y = w.find(")")
                date_list.append(w[x:y])

        n+=1
        print(f'Artigos raspados: {n} de {len(url)}.')
    genFile()

def getArticles(magazines):
    def getArticlesWithCovers(cover_magazines):
        for i in cover_magazines:
            source = requests.get(i).text
            soup = BeautifulSoup(source, 'html.parser')
            try:
                title = soup.find_all('div', {'class': 'tocTitle'})
                for link in title:
                    article_link.append(link.find('a').attrs['href'])
            except:
                print('Oops, something is wrong. Please, contact someone who might know.')

    article_link = []
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
            if soup.find_all('td', {'class': 'tocArticleTitleAuthors'}):
                title = soup.find_all('div', {'class': 'tocTitle'})
                for link in title:
                    try:
                        article_link.append(link.find('a').attrs['href'])
                    except:
                        None
                    #print('Oops, something is wrong. Please, contact someone who might know.')
        if soup.find(id = 'issueCoverImage'):
            for link in soup.find(id = 'issueCoverImage'):
                cover_magazines.append(link.attrs['href'])
        
        sites_scraped+=1
        print(f'Revistas raspadas: {sites_scraped} de {len(magazines)}')

    getArticlesWithCovers(cover_magazines)
    
    print('Todas revistas foram raspadas!\nIniciando m??dulo para raspar os dados dos artigos...') 
    getInfo(article_link)

def getMagazines(url):
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.is_visible('div.issues')
    condition = page.url
    try:
        print('Verificando se a p??gina cont??m sucessores.')
        next_page = page.locator("text=>").nth(1).get_attribute('href')
        last_page = page.locator("text=/.*\\>\\>.*/").get_attribute('href')
        next_page_exists = True
    except:
        next_page_exists = False
        print('P??gina n??o cont??m sucessores.')
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
    getMagazines('http://www.periodicos.ulbra.br/index.php/acta/issue/archive')

'''
SITES QUE FORAM REALIZADOS OS TESTES:

- http://www.periodicos.ulbra.br/index.php/acta/issue/archive

- http://www.periodicos.ulbra.br/index.php/ic/issue/archive
'''