"""Module responsible for capture news in Brazilian Camara News Site"""
import os
import json
from datetime import datetime
import boto3
from bs4 import BeautifulSoup
from lib.data import Notice
from lib.scraping import scrap

PAGE = 'https://www.camara.leg.br/noticias/ultimas'

QUEUE_URL = 'https://' + \
    os.getenv('AWS_REGION', 'us-west-1') + \
    '.queue.amazonaws.com/' + \
    os.getenv('AWS_ACCOUNT_ID', '') + \
    '/update-camara-new-content-' + \
    os.getenv('ENVIRONMENT', 'development')


def invoke_update_section_function(payloads):
    """Invoke sns to retrieve dou section information"""
    sqs_client = boto3.client('sqs')
    delay_seconds = 0

    for payload in payloads:
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"id": str(payload)}),
            DelaySeconds=delay_seconds
        )
        delay_seconds += 1


def get_all_notices_in_page(soup):
    """"Collect Brazil Camara News Information"""
    notices = []
    results = soup.findAll('div', href=False, attrs={
                           'class': 'l-lista-noticias__item'})

    for result in results:
        data = Notice()
        title = result.find('a', href=True)
        date = result.find('span', href=False, attrs={
            'class': 'g-chamada__data'}).text

        data.title = title.text
        data.url = title.href
        data.date = datetime.strptime(date, '%d-%m-%Y')
        data.createdAt = datetime.today().replace(microsecond=0)
        data.updatedAt = datetime.today().replace(microsecond=0)
        notices.append(data)

    return notices


def check_if_notice_is_new(notice):
    """"Check if notice is present in database"""
    try:
        notice = Notice.objects.get(
            title=notice.title, date=notice.date)
    except Notice.DoesNotExist:
        notice = False

    return notice


def handler(event, _):
    """Lambda function entry point"""
    print(event)

    driver = scrap(PAGE)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    notices = get_all_notices_in_page(soup)

    news = []
    if len(notices) > 0:
        for notice in notices:
            new = check_if_notice_is_new(notice)
            if new is not False:
                news.push(new)

    total_news = len(news)
    if total_news > 0:
        payloads = Notice.objects.insert(news, load_bulk=False)
        invoke_update_section_function(payloads)

    return "Success" + str(total_news) + "news inserted"


if __name__ == "__main__":
    handler('Testing as script', '')
