import requests
import bs4

LINK = 'https://habr.com/ru/all/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ym_uid=1647536201584406509; fl=ru; hl=ru; _ga=GA1.2.586896173.1647536202; visited_articles=481432:474622; _ym_d=1663510005; habr_web_home_feed=/all/; _ym_isad=2; _gid=GA1.2.1343103421.1663510006; _gat_gtag_UA_726094_1=1',
    'Host': 'habr.com',
    'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
KEYWORDS = {'дизайн', 'фото', 'web', 'python'}


def get_words(keywords):
    keywords_new = set()
    for i in keywords:
        keywords_new.add(i.title())
        keywords_new.add(i.title() + ' *')
        keywords_new.add(i.upper())
    KEYWORDS.update(keywords_new)


def get_article(articles):
    for article in articles:
        user = get_user(article)
        title = get_title(article)
        hubs = get_hubs(article)
        body = get_body(article)
        get_link(user, title, hubs, body, article)


def get_user(article):
    user_name = {article.find(class_='tm-user-info tm-article-snippet__author').text.strip()}
    return user_name


def get_title(article):
    title = article.find('h2').find('a').text.strip()
    title = set(''.join(title).split())
    return title


def get_hubs(article):
    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    hubs = {hub.find('a').text.strip() for hub in hubs}
    return hubs


def get_body(article):
    body = article.find(class_='tm-article-body tm-article-snippet__lead').text
    body = set(''.join(body).split())
    return body


def get_link(user, title, hubs, body, article):
    if user & KEYWORDS or title & KEYWORDS or hubs & KEYWORDS or body & KEYWORDS:
        href = article.find('h2').find('a').attrs['href']
        link = 'https://habr.com' + href
        title = article.find('h2').find('a').text.strip()
        datetime = article.find(class_='tm-article-snippet__meta-container').find('time')
        date = datetime.attrs['title'].split(',')
        print(f'{date[0]} - {title} - {link}')
        print()


if __name__ == '__main__':
    response = requests.get(LINK, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all(class_='tm-article-snippet')
    get_words(KEYWORDS)
    get_article(articles)
