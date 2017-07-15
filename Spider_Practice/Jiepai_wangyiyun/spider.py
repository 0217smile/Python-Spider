import json
import os
import re
from hashlib import md5
from json.decoder import JSONDecodeError
from pathlib import Path

import pymongo
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from config import *
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def _create_dir(name):
    """
    根据传入的目录名创建一个目录，这里用到了 python3.4 引入的 pathlib 库。
    """
    directory = Path(name)
    if not directory.exists():
        directory.mkdir()
    return directory

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
        # 另一种方法：urls = [item.get('article_url') for item in data.get('data') if item.get('article_url')]
    except JSONDecodeError:
        pass

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错')
        return None

def parse_page_detail(html, url, root_dir):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pattern, html)
    if result:#是这种图集才创建文件夹。
        dir_name = re.sub(r'[\\/:*?"<>|]', '', title)
        download_dir = _create_dir(root_dir / dir_name)
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image, save_dir=download_dir)
            return {
                'title': title,
                'url': url,
                'images': images
            }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def download_image(url, save_dir):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content, save_dir)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

def save_image(content, save_dir):
    #file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    file_name = '{0}.{1}'.format(md5(content).hexdigest(), 'jpg')
    save_path = save_dir / file_name
    if not os.path.exists(save_path):
        with open(save_path, 'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    root_dir = _create_dir(SAVE_PATH)  # 保存图片的根目录
    html =get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url, root_dir)
            # if result:
            #     save_to_mongo(result)

if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START, GROUP_STOP + 1)]
    pool = Pool()
    pool.map(main, groups)