from fake_useragent import UserAgent
from django.conf import settings
import requests
import time
import random
import lxml.html          
from apps.section.models import ProductModel, ProductModelItemConnection
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.core.mail import mail_admins
from django.template.defaultfilters import slugify
import urllib2
import logging
logger = logging.getLogger('importer')

class Parse:
    """docstring for Parse"""
    def __init__(self):
        self.timeout = 20
        self.proxy_list = self.get_proxy_list()

    def get_proxy_list(self):
        with open(settings.PROXY_FILE_PATH) as plist:
            proxy_list = [{'http': item.rstrip('\n').strip()} for item in plist     ]
        return proxy_list if proxy_list else []

    def delete_proxy(self,killist):
        try: 
            self.proxy_list.remove(killist)
        except ValueError:
            pass

    def get_proxy(self):
        if  len(self.proxy_list) :
            r=random.randint(0, len(self.proxy_list)-1)
            res = self.proxy_list[r]    
        else:
            raise Exception('All proxy in proxy.txt was tried')
        return res

    def get_url (self, url):
        session = requests.session()
        ua = UserAgent()
        # data = None
        while True:
            proxy = self.get_proxy()
            time.sleep(random.randint(3, 9))
            try:
                data = requests.get(url, headers={
            'User-Agent': ua.random} , proxies= proxy ,timeout=(self.timeout))
                print 'in try',proxy
                if data.status_code == requests.codes.ok:
                    break
            except Exception, e:
                self.delete_proxy(proxy)
                print 'in exept',proxy,e
                pass
        return data

    def parse_hotline_items(self, base_url, section_id ):
        n = 0
        while True :
            if n ==0:
                url =base_url
            else:
                url = "%s?p=%s" % (base_url, n)
            print n, url
            data = self.get_url(url)
            print 'data!!!!!!!!!!!'
            html = lxml.html.fromstring(data.content)
            print 'html!!!!!!!!!!!'
            items = html.cssselect('.m_r-10 .g_statistic')
            print 'items!!!!!!!!!!!'
            if len(items) <= 0 :
                if html.cssselect('.last.m_l-5.g_statistic')==[]:
                    break
                continue
            n+=1
            for item in items:
                try:
                    p = ProductModel()
                    p.name = item.text.strip()
                    p.section_id = section_id
                    p.search_name = p.name
                    p.slug = slugify(p.name)
    
                    try:
                        image_url = "http://hotline.ua%s" % item.getparent(). \
                            getparent(). \
                            getparent(). \
                            getparent(). \
                            getparent(). \
                            cssselect('.gd-img-cell')[0].attrib['hltip']    
                    except:
                        image_url = None
    
                    if image_url:
                        f = NamedTemporaryFile(delete=True)
                        # data = self.get_url(image_url)
                        data= urllib2.urlopen(image_url).read()
                        f.write(data)
                        f.flush()
                        p.image = File(f)
                    # p = ProductModel(**data)
                    p.save()
                except Exception as ex:
                    logger.error(ex)
            if html.cssselect('.last.m_l-5.g_statistic')==[]:
                break
    # mail_admins(
        # u'Парсинг товаров в каталог', u'Парсинг товаров успешно завершился')