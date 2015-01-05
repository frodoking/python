# -*- coding:utf-8 -*-
import os
import urllib
from HTMLParser import HTMLParser
import re
from ThreadPool import ThreadPool

host_url = "http://www.dbmeizi.com/"
root_dir = "D:\\work\\tmp\\dbmeizhi\\"


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


def get_tab_list(url):
    u = urllib.urlopen(url)
    html_content = u.read()
    m = DBHtmlParser()
    m.feed(html_content)
    m.close()
    return m.tab_list


def create_dir(dir_name):
    path = os.path.join(root_dir, dir_name)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_image_url_list(image_url):
    u = urllib.urlopen(image_url)
    data = u.read()
    r = re.compile(r'http://pic.dbmeizi.com/npics/[a-z0-9-]{3}/[a-z0-9-]{3}/s_p[0-9]{8}.jpg')
    image_url_list = r.findall(data)
    return image_url_list


def down_image(image_url, image_dir):
    print image_url
    u = urllib.urlopen(image_url)
    data = u.read()
    name = image_url[-13:-3]
    f = open(image_dir + '\\' + '%s.jpg' % name, 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':
    tab_list = get_tab_list(host_url)
    # thread_pool = ThreadPool(len(tab_list))
    for tab in tab_list:
        tab_path = tab[0]
        tab_name = tab[1].decode('utf-8')
        tab_dir = create_dir(tab_name)

        print '开始抓取 >>>> ', tab_path, tab_name, tab_dir

        for p in range(10):
            for url in get_image_url_list(host_url + '?p=%d' % p):
                down_image(url, tab_dir)
                # thread_pool.add_job(down_image, url, tab_dir)

    # thread_pool.wait_for_complete()
    print '结束'