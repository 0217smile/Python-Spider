# -*- coding:utf-8 -*-
'''
自己查看新浪微博API 尝试自动发微博，参看文章：http://www.jb51.net/article/83144.htm

具体做法，就是在浏览器打开：
https://api.weibo_spider.com/oauth2/authorize?client_id=1846308100&redirect_uri=https://api.weibo_spider.com/oauth2/default.html&response_type=code。
该方法会转到授权页面，授权之后会转到：
https://api.weibo_spider.com/oauth2/default.html&code=CODE，记录下该url中的CODE。

接着，调用https://api.weibo_spider.com/oauth2/access_token接口，获得返回的access_token:6adc0cd0c74d5d24e909fbab15120b2f
'''
import requests

APP_KEY = '1846308100'
APP_SECRET = 'd938da531c8cfded43172255f03d5201'
CALLBACK_URL = 'https://api.weibo_spider.com/oauth2/default.html'

def build_uri(url,endpoint):
    pass

def code_request():
    url_get_code = 'https://api.weibo_spider.com/oauth2/authorize'
    #构建URL参数,用params传递
    params={
        "client_id":APP_KEY,
        "redirect_uri": CALLBACK_URL,
        "response_type": 'code'
    }
    response = requests.get(url_get_code, params=params)
    print response.url
    print response.text
    # code =
    # return code

def token_request():
    url_get_token = "https://api.weibo_spider.com/oauth2/access_token"
    # 构建POST参数,
    code = 'd1e566ce6900ccb832933e954d900e1d'
    playload = {
        "client_id": APP_KEY,
        "client_secret": APP_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": CALLBACK_URL
    }

    response = requests.post(url_get_token, data=playload)
    #{"access_token": "2.00wNRM4GuEvwACfc2f519686jXf3bC", "remind_in": "157679999", "expires_in": 157679999,"uid": "5839578868"}
    data = response.json()
    return data['access_token'], data['expires_in']

def sendtext_request(access_token):
    url_post_a_text = "https://api.weibo_spider.com/2/statuses/update.json"
    playload = {
        "access_token": access_token,
        "status": "This is a text 0217smile@听歌把妹小星星"
    }
    response = requests.post(url_post_a_text, data=playload)
    print '微博发送成功'

def sendimg_request(access_token):
    url_post_pic = "https://upload.api.weibo_spider.com/2/statuses/upload.json"
    playload = {
        "access_token": access_token,
        "status": "Test:Post a text with a pic & 0217smile@听歌把妹小星星"
    }
    # 构建二进制multipart/form-data编码的参数
    files = {
        "pic": open("1.jpg", "rb")
    }
    response = requests.post(url_post_pic, data=playload, files=files)
    print '图片微博发送成功'

def main():
    #code_request() 这个功能暂未实现，遇到了些问题，他要跳转到授权页面，在下还不能处理这个，不过暂不影响下边的功能。
    #获得access_token，获得的这个access_token能用两三年。哈哈
    #access_token, expires_in = token_request()
    access_token = '2.00wNRM4GuEvwACfc2f519686jXf3bC'
    #发文字微博
    #sendtext_request(access_token)
    # 发文字微博
    sendimg_request(access_token)

if __name__ == '__main__':
    main()