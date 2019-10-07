import requests
import lxml.html
from lxml import etree
import time
import os
import codecs
from fake_useragent import UserAgent
import pickle


session = None

base_url = 'http://hotline.ua/mobile/mobilnye-telefony-i-smartfony/?p=%s'


def parse_hotline_items(base_url):
    result = []
    session = requests.session()
    ua = UserAgent()
    for n in xrange(20):
        try:
            url = base_url % (n+1)
            print n, url
            data = requests.get(url, headers={
                'User-Agent': ua.random
            })
            html = lxml.html.fromstring(data.content)
            items = html.cssselect('.m_r-10 .g_statistic')
            if len(items)<=0:
                break

            for item in items:
                print item.text
                spec = item.getparent().getparent().getparent().getparent().getparent().cssselect('.gd-img-cell')[0].attrib['hltip']
                print spec
                result.append(item.text)

            # time.sleep(2)
        except Exception as ex:
            print ex

    file_name = os.path.join('.', 'hotline1.txt')
    f = codecs.open(file_name, "w", encoding='utf-8')
    f.write(str(result))
    f.close()
    f = file("p1.bin", "w")
    pickle.dump(result, f)
    f.close()
    print "Result:", len(result),len(set(result))

parse_hotline_items(base_url=base_url)