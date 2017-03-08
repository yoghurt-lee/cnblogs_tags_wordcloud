#coding:utf-8

import requests
import random
from bs4 import BeautifulSoup
import os
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image

#此段代码解决 1.matplotlib中文显示问题 2 '-'显示为方块问题
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

Headers = [ 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                'Opera/9.25 (Windows NT 5.1; U; en)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",] #备用header头，防止被封

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}

def gettags(data):
    text = []
    soup = BeautifulSoup(data)
    table = soup.find('table',{'id':'MyTag1_dtTagList'})
    tags = table.findAll('a')
    nums = table.findAll('span',{'class':'small'})
    for i in xrange(len(tags)):
        num_str = nums[i].string.strip()
        num = int(num_str[1:len(num_str)-1])
        tag = [tags[i].string.strip()]
        text.extend(tag*num)
    return [' '.join(text),set(text)]

def draw_wordcloud(text):
    d = os.path.dirname(__file__)
    mask = np.array(Image.open(os.path.join(d, "love.jpg")))
    font=os.path.join(os.path.dirname(__file__), "FZSTK.ttf")
    stopwords = set(STOPWORDS)
    stopwords.add("int")
    stopwords.add("ext")
    wc = WordCloud(font_path=font,max_words=200, mask=mask,max_font_size=200, stopwords=stopwords,margin=10,random_state=42,background_color='white',scale =1.2).generate(text)
    default_colors = wc.to_array()
    #设置颜色为原图片像素颜色
    wc.to_file("cnblogs_tag/a_new_hope.png")
    #设置为 wordcloud 默认
    plt.imshow(default_colors)
    plt.axis("off")
    plt.show()

def spider():
    url = 'http://www.cnblogs.com/liyinggang/tag/'
    num = random.randint(0,7)
    headers['User-Agent'] = Headers[num]
    data = requests.get(url=url,headers=headers).content
    with open('cnblogs_tag/data.txt','w') as f:
        f.write(data)


if __name__ == '__main__':
    #spider()
    data = open('cnblogs_tag/data.txt').read()
    [text,data_list] = gettags(data)
    draw_wordcloud(text)
