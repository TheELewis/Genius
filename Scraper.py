from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random
import requests
import re
import string
import urllib
import os
from hashlib import sha1  

user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']

# def get_by_url(url):
#     try:
#         with closing(get(url, stream=True)) as resp:
#             if is_good_response(resp):
#                 return resp.content
#             else:
#                 return None
        
#     except RequestException as e:
#         log_error('Error occured during requests to {0} : {1}'.format(url, str(e)))
#         return None

# def is_good_response(resp):
#     content_type = resp.headers['Content-Type'].lower()
#     return (resp.status_code == 200
#             and content_type is not None
#             and content_type.find('html') > -1)


def get_lyrics_by_url(url, user_agents):
    
    response = requests.get(url, headers = {'User-Agent': random.choice(user_agents)})
    soup = BeautifulSoup(response.content, "lxml")
    content = response.content
    page_lyrics = soup.find_all( class_ = "lyricbox")
    lyric = re.sub('[(<.!,;?>/\-)]', " ",  str(content)).split()
    lyric = [word for word in lyric if word != 'br']
    return lyric[10:-4]
        

def log_error(e):
    print(e)

if __name__ == "__main__":
    html_data = get_lyrics_by_url("http://lyrics.wikia.com/wiki/Run_The_Jewels:Talk_To_Me", user_agents)
    #soup = BeautifulSoup(html_data, 'html.parser')
    #all_div = soup.findAll
    
