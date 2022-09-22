from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import requests

title_list = []
author_list = []
abstract_list = []
tag_list = []
complete_version_list = []

def getInfo(url):
    l = len(url)
    n = 0
    for i in url:
        source = requests.get(i).text
        soup = BeautifulSoup(source, 'html.parser')
        try:
            title = soup.find_all(id = 'articleTitle')
            for item in title:
                title_list.append(item.find('h3').text)
        except:
            title_list.append('Title not found.')

        try:
            author = soup.find_all(id = 'authorString')
            for item in author:
                author_list.append(item.find('em').text)
        except:
            author_list.append('Author not found.')

        try:
            background = soup.find_all(id = 'articleAbstract')
            for item in background:
                abstract_list.append(item.find('div').text)
        except:
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
        print(f'Artigos raspados: {n} de {l}.')
    
    print('Arquivo em xlsx sendo gerado.')
    print('Title_list: ', len(title_list))
    print('Author_list: ', len(author_list))
    print('abstract_list: ', len(abstract_list))
    print('tag_list: ', len(tag_list))
    print('complete_version_list: ', len(complete_version_list))

    df = pd.DataFrame({
        'Titles': title_list,
        'Authors': author_list,
        'Abstract': abstract_list,
        'Tags': tag_list,
        'Complete Version': complete_version_list
    })

    df.to_excel('artigos.xlsx', index=False)
    print('Arquivo gerado.')

def getArticles(magazines):
    size = len(magazines)
    sites_scraped = 0
    article_link = []
    for i in magazines:
        source = requests.get(i).text
        soup = BeautifulSoup(source, 'html.parser')
        try:
            title = soup.find_all('div', {'class': 'tocTitle'})
            for link in title:
                article_link.append(link.find('a').attrs['href'])
        except:
            None
        sites_scraped+=1
        print(f'Revistas raspadas: {sites_scraped} de {size}')
    print('Todas revistas foram raspadas!\nIniciando módulo para raspar os dados dos artigos...') 
    getInfo(article_link)

def getMagazines(url):
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    page.is_visible('div.tile-body')
    condition = page.url
    next_page = page.locator("text=>").nth(1).get_attribute('href')
    last_page = page.locator("text=/.*\\>\\>.*/").get_attribute('href')
    magazines = []
    while condition != None:
        url = page.inner_html('#issues')
        soup = BeautifulSoup(url, 'html.parser')
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
    page.close()
    print('Todos os links das revistas foram raspados.')
    getArticles(magazines)

with sync_playwright() as p:
    getMagazines('http://www.periodicos.ulbra.br/index.php/acta/issue/archive')


