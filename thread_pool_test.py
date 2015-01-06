# -*- coding:utf-8 -*-
import socket
import urllib2

from thread_pool import WorkerManager

root_dir = "D:\\work\\tmp\\test\\"


def main():
    url_list = {"sina": "http://www.sina.com.cn",
                "sohu": "http://www.sohu.com",
                "yahoo": "http://www.yahoo.com",
                "xiaonei": "http://www.xiaonei.com",
                "qihoo": "http://www.qihoo.com",
                "laohan": "http://www.laohan.org",
                "eyou": "http://www.eyou.com",
                "chinaren": "http://www.chinaren.com",
                "douban": "http://www.douban.com",
                "163": "http://www.163.com",
                "daqi": "http://www.daqi.com",
                "qq": "http://www.qq.com",
                "baidu_1": "http://www.baidu.com/s?wd=asdfasdf",
                "baidu_2": "http://www.baidu.com/s?wd=dddddddf",
                "google_1": "http://www.baidu.com/s?wd=sadfas",
                "google_2": "http://www.baidu.com/s?wd=sadflasd",
                "hainei": "http://www.hainei.com",
                "microsoft": "http://www.microsoft.com",
                "wlzuojia": "http://www.wlzuojia.com"}

    # 使用线程池
    socket.setdefaulttimeout(10)
    print 'start testing'
    wm = WorkerManager(10)
    for url_name in url_list.keys():
        wm.add_job(do_get_con, url_name, url_list[url_name])
    wm.wait_for_complete()
    print 'end testing'


def do_get_con(url_name, url_link):
    print url_link
    try:
        fd = urllib2.urlopen(url_link)
        data = fd.read()
        f_hand = open(root_dir + "%s" % url_name, "wb")
        f_hand.write(data)
        f_hand.close()
    except Exception, e:
        pass


if __name__ == "__main__":
    main()