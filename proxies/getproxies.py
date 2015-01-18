#!/usr/bin/python
import lxml.html
from lxml.cssselect import CSSSelector

import httplib
import string
import simplejson
import re
import requests

class theproxy:
    def __init__(self):
        self.ip = ""
        self.port = ""
        self.protocol = ""
        self.country = ""
        self.speed = ""
    def __str__(self):
        return "ip:%s\nport:%d\nprotocol:%s\ncountry:%s\nspeed:%d\n"%(self.ip,self.port,self.protocol,self.country,self.speed)

class proxyscraper:
    def __init__(self):
        self.proxy_page_urls = []
        self.proxy_website = "default"

    def build_proxy_page_urls(self):
        #overwritable
        pass

    def _scrape_single_page_proxies(self, proxy_page_url):
        r = requests.get(proxy_page_url, timeout=5)
        response = r.text
        return self._parse_response(response)

    def _parse_response(self, response):
        return [] 

    def scrape_proxies(self):
        proxies = []
        self.build_proxy_page_urls()

        for pageurl in self.proxy_page_urls:        
            proxies_page = self._scrape_single_page_proxies(pageurl)
            proxies.extend(proxies_page)

        valid_proxies = [ {"ip":p.ip,"port":p.port,"protocol":p.protocol} for p in proxies if self._test_proxy(p)]
        print len(valid_proxies),"/",len(proxies)

        with open("proxies_%s.txt"%self.proxy_website,"w+") as f:
            f.write(simplejson.dumps(valid_proxies))

    @staticmethod
    def _test_proxy(proxy):
        print "Testing:%s:%s:%d"%(proxy.protocol, proxy.ip, proxy.port),
        ok = False
        try:
            r = requests.get('http://www.baidu.com/',timeout=5, proxies = {"http": '%s:%d'%(proxy.ip,proxy.port)})
            if r.status_code == 200:
                ok = True
        except Exception,e:
            pass
        print ok
        return ok

if __name__ == "__main__":
    proxy = theproxy()
    proxy.ip = "222.74.28.14"
    proxy.port = 23
    proxy.protocol = "http"
    proxyscraper._test_proxy(proxy)

   
                   
            
