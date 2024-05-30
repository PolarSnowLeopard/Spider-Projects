#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/05/30 18:41:58
@Author  :   YuFanWenShu 
@Contact :   1365240381@qq.com

'''

# here put the import lib


# here put the import lib


import time
import requests
import re  

re_title = re.compile(r'<h1>(.*?)</h1>')
re_text = re.compile(r'<div id="htmlContent".*?>(.*?)</div>')
re_next_page = re.compile(r'章节目录.*?<a href="(.*?)" id="link-next">下一章</a>')

name = '斗破苍穹'
novel_url = "https://www.bxwx7.org/article/6692/"
page_url = "https://www.bxwx7.org/article/6692/4379302.html" # 首页

def get_page(url):    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        status = r.status_code
        title, text, next_page = parse(r)            
        
        print(f'状态码{status}，爬取成功: {title}')

    except Exception as e:
        print(f"\n状态码{status}，爬取失败，{url}")
        print(e,"\n")
    
    return title, text, next_page

def parse(response):
    title = re_title.search(response.text).group(1)
    text = re_text.search(response.text).group(1)
    next_page = re_next_page.search(response.text).group(1)

    if title and text:
        text = text.replace('<br/><br/>','\n')
        text = text.replace('<br><br>','\n')
        text = text.replace('<br /><br />','\n')
        text = text.replace('&nbsp;&nbsp;&nbsp;&nbsp;','\t')
        text = text.replace('一秒记住【笔下文学 www.bxwx7.org】，精彩小说无弹窗免费阅读！\n','')
        return title, text, next_page
    else:
        return '匹配失败','匹配失败'
    
def save_page(title, text, f):
    f.write(f"{title} \n\n")
    f.write(f"{text} \n\n\n\n")

if __name__ == '__main__':
    with open(f'{name}.txt','w+',encoding='utf-8') as f:
        while page_url != novel_url:
            title, text, page_url = get_page(page_url)
            save_page(title, text, f)
