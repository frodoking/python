# -*- coding:utf-8 -*-
import urllib
import re

global num
num = 0
i = 0
save_path = "D:\\work\\tmp\\dbmeizhi\\"


def get_url(n):
    url = urllib.urlopen('http://www.dbmeizi.com/category/14?p=%d' % n)
    data = url.read()
    r = re.compile(r'http://pic.dbmeizi.com/npics/[a-z0-9-]{3}/[a-z0-9-]{3}/s_p[0-9]{8}.jpg')
    pic = r.findall(data)
    return pic


for page in range(1, 10):
    girl = get_url(page)
    length = len(girl)
    for i in range(0, length):
        print(girl[i])
        url2 = urllib.urlopen(girl[i])
        data2 = url2.read()
        f = open(save_path + '%d.jpg' % num, 'wb')
        f.write(data2)
        f.close()
        print num
        num += 1
print '结束'