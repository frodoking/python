# -*- coding:utf-8 -*-
import os
import socket
import urllib
from HTMLParser import HTMLParser
import re
import urllib2
from thread_pool import WorkerManager


# html页面解析
class DBHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = None
        self.is_pair = False
        self.tab_list = []
        self.index = 0

    def handle_starttag(self, tag, attrs):  # 这里重新定义了处理开始标签的函数
        # 判断标签<a>的属性
        if tag == 'a':
            self.flag = 'a'
            for href, link in attrs:
                if href == 'href' and link.find('category') > 0 and link.find('10') == -1:
                    self.is_pair = True
                    item = [link, None]
                    self.tab_list.append(item)

    def handle_data(self, data):  # 处理<a>标签之间的数据
        if self.flag == 'a' and self.is_pair is True:
            self.is_pair = False
            self.tab_list[self.index][1] = data
            self.index += 1


# 获取tab的url列表
def get_tab_list(url):
    u = urllib.urlopen(url)
    html_content = u.read()
    m = DBHtmlParser()
    m.feed(html_content)
    m.close()
    return m.tab_list


# 创建不存在的目录
def create_dir(dir, name):
    path = os.path.join(dir, name)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


# 获取当前tab中的图片url列表
def get_image_url_list(image_url):
    u = urllib.urlopen(image_url)
    data = u.read()
    r = re.compile(r'http://pic.dbmeizi.com/npics/[a-z0-9-]{3}/[a-z0-9-]{3}/s_p[0-9]{8}.jpg')
    image_url_list = r.findall(data)
    return image_url_list


# 下载
def down_image(image_url, image_dir, high):
    if high is True:  # 高清图片
        image_url = image_url.replace('s_', '')
    print image_url, image_dir, high
    try:
        fd = urllib2.urlopen(image_url)
        data = fd.read()
        name = image_url[-13:-3]
        f_hand = open(image_dir + '\\' + '%s.jpg' % name, 'wb')
        f_hand.write(data)
        f_hand.close()
    except:
        pass


def main():
    host_url = "http://www.dbmeizi.com/"
    root_dir = "D:\\work\\tmp\\dbmeizhi\\"

    print '************ 开始 ***********'
    tab_list = get_tab_list(host_url)
    # 使用线程池
    socket.setdefaulttimeout(10)
    wm = WorkerManager(len(tab_list))
    for tab in tab_list:
        tab_path = tab[0]
        tab_name = tab[1].decode('utf-8')
        tab_dir = create_dir(root_dir, tab_name)

        print '开始抓取 >>>> ', tab_path, tab_name, tab_dir

        for p in range(10):  # 默认10页
            image_urls = get_image_url_list(host_url + '?p=%d' % p)
            count = 0
            for url in set(image_urls):
                count += 1
                print '当前状态 >>>> ', tab_name, count, len(image_urls), ' <<<< '
                down_image(url, tab_dir, True)
                # wm.add_job(down_image, url, tab_dir, True)
    wm.wait_for_complete()
    print '************ 结束 ***********'

if __name__ == '__main__':
    main()