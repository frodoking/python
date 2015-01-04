# !/usr/bin/evn python
# coding=utf8
# 风行网 高清VIP电影  ^_^

import time
import urllib2
import cStringIO
import gzip
import re
import json
import random

def create_request(url, referer=None):
    req = urllib2.Request(
        urllib2.quote(url.split('#')[0].encode('utf8'), safe="%/:=&?~#+!$,;'@()*[]"),
        headers={"Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                 "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
                 "Accept-Encoding": "gzip",
                 "Accept-Language": "zh-CN,zh;q=0.8",
                 "Cache-Control": "max-age=0",
                 "Connection": "keep-alive",
                 "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.106 Safari/535.2",
        })

    if referer is not None:
        req.add_header('Referer', referer)
    return req


def get_content(url, referer=None):
    f = urllib2.urlopen(create_request(url, referer), timeout=15)
    data = f.read()
    if data[:6] == '\x1f\x8b\x08\x00\x00\x00':
        data = gzip.GzipFile(fileobj=cStringIO.StringIO(data)).read()
    f.close()

    return data


def get_cdn_url(api_url, referer=None):
    content = get_content(api_url, referer)
    data = json.loads(content)
    token = data['token']
    for resource in data['fsps']:
        fsp_url = resource['url']
        if resource['clarity'] == 'super-dvd':
            fsp_url = resource['url']

    fsp = re.findall("fsp://(\w+)", fsp_url)[0]
    if fsp == '':
        return None
    else:
        timestamp = int(time.time())
        cdn_url = 'http://jobsfe.funshion.com/query/v1/mp4/{0}.json?clifz=fun&mac=&tm={1}&token={2}'.format(fsp,
                                                                                                            timestamp,
                                                                                                            token)
        return cdn_url


def get_play_url(cdn_url, referer=None):
    content = get_content(cdn_url, referer)
    data = json.loads(content)
    if data['return'] == 'succ':
        play_urls = data['playlist'][0]['urls']
        return play_urls[random.randint(0, len(play_urls) - 1)]
    return None


if __name__ == '__main__':
    # if len(sys.argv) < 2 or sys.argv[1].startswith('http') is None:
    # print 'Usage: python fun.py http://www.fun.tv/vplay/m-115946/'
    # print 'Please input the url to be parse'
    # sys.exit()

    # videoUrl = sys.argv[1]
    video_url = "http://www.fun.tv/vplay/m-97920"
    vid = int(re.findall("vplay/m-(\d+)", video_url)[0])
    api_url = 'http://api.fun.tv/ajax/get_webplayinfo/{0}/1/mp4?user=funshion'.format(vid)
    cdn_url = get_cdn_url(api_url, video_url)
    playUrl = get_play_url(cdn_url, video_url)
    print playUrl