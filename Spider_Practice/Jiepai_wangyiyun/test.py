import re

import requests
from bs4 import BeautifulSoup


def get_page_detail(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pattern, html)
    if result:
        print('ok的')
if __name__ == '__main__':
    url = 'https://temai.snssdk.com/article/feed/index?id=2972709&subscribe=5568158065&source_type=6&content_type=2&create_user_id=2690&classify=10&adid=__AID__&tt_group_id=6433679416896045313'
    html = get_page_detail(url)
    parse_page_detail(html, url)