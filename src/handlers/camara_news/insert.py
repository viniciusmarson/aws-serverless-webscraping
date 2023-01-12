"""Module responsible for capture news in Brazilian Camara News Site"""
from datetime import datetime
from bs4 import BeautifulSoup
from lib.data import Notice
from lib.queue import send_payloads_to_queue
from lib.scrape import scrape

PAGE = 'https://www.camara.leg.br/noticias/ultimas'


def get_all_notices_in_page(soup):
    """"Collect Brazil Camara News Information"""
    notices = []
    results = soup.findAll('article', href=False, attrs={
                           'class': 'g-chamada chamada--ultimas'})

    for result in results:
        notice = Notice()
        title = result.find('a', href=True)
        notice.title = title.text.strip()
        notice.url = title['href']

        date = result.find('span', attrs={'class': 'g-chamada__data'}).text
        notice.date = datetime.strptime(date, '%d/%m/%Y %H:%M')
        notice.createdAt = datetime.today().replace(microsecond=0)
        notice.updatedAt = datetime.today().replace(microsecond=0)
        notices.append(notice)

    return notices


def check_if_notice_is_new(notice):
    """"Check if notice is present in database"""
    try:
        notice = Notice.objects.get(
            title=notice.title, date=notice.date)
    except Notice.DoesNotExist:
        notice = True

    return notice


def handler(event, _):
    """Lambda function entry point"""
    print(event)

    driver = scrape(PAGE)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    notices = get_all_notices_in_page(soup)

    news = []
    for notice in notices:
        if check_if_notice_is_new(notice) is True:
            news.append(notice)

    total_news = len(news)
    if total_news > 0:
        payloads = Notice.objects.insert(news, load_bulk=False)
        send_payloads_to_queue("camara-notices-to-update", payloads)

    return f"Success {str(total_news)} news inserted"


if __name__ == "__main__":
    handler('Testing as script', '')
