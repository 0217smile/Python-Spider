import requests
import os
from hashlib import md5

from requests.exceptions import RequestException



def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+'\picture', md5(content).hexdigest(), 'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def main():
    url = 'http://g-search3.alicdn.com/img/bao/uploaded/i4/i4/TB1zUfNRFXXXXaMXVXXXXXXXXXX_!!0-item_pic.jpg'
    download_image(url)

if __name__ == '__main__':
    main()