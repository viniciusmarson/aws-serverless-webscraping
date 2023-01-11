"""Module respinsible for update the notice information from Brazilian Camara News Site"""
import json
from datetime import datetime
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from lib.data import Notice
from lib.scraping import scrap

# Scraped URL example:
# https://www.camara.leg.br/noticias/933637-moveis-projetados-por-oscar-e-anna-niemeyer-foram-salvos-da-destruicao/


def handler(event, _):
    """Lambda function entry point"""

    print(event)
    body = json.loads(event['Records'][0]['body'])

    notice = Notice.objects.get(id=ObjectId(body['id']))
    driver = scrap(notice.url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    subtitle = soup.find('p', attrs={'class': 'g-artigo__descricao'})
    if subtitle:
        notice.subtitle = subtitle.text

    image_url = soup.find('img')
    if image_url:
        notice.image = image_url.src

    content_section = soup.find('div', attrs={'class': 'js-article-read-more'})

    notice.content = ''
    for paragraph in content_section.findAll('p'):
        notice.content += paragraph.text + '\n'

    notice.updatedAt = datetime.today().replace(microsecond=0)
    notice.save()

    return 'Success'
