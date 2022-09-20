from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def getInfo(html):
    title_list = []
    authour_list = []
    background_list = []
    tag_list = []
    complete_version_list = []
    pass

def getArticles(html):
    articles = []
    pass

def getMagazines(html):
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(html)
    page.is_visible('div.tile-body')
    condition = page.url
    next_page = page.locator("text=>").nth(1).get_attribute('href')
    last_page = page.locator("text=/.*\\>\\>.*/").get_attribute('href')
    magazines = []
    while condition != None:
        html = page.inner_html('#issues')
        soup = BeautifulSoup(html, 'html.parser')
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
        
    return magazines

with sync_playwright() as p:
    print(getMagazines('http://www.periodicos.ulbra.br/index.php/acta/issue/archive'))



'''
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False, slow_mo = 1000)
    page = browser.new_page()
    page.goto('http://www.periodicos.ulbra.br/index.php/acta/issue/archive')
    html = page.inner_html('#issues')
    soup = BeautifulSoup(html, 'html.parser')
    Magazines = []
    next_page = page.locator("text=>").nth(1).get_attribute('href')
    for all_links in soup.find_all('a'):
        if all_links.attrs['href'] != next_page:
            Magazines.append(all_links.attrs['href'])
        
    print(Magazines)
'''
