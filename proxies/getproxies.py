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

def _scrape_proxies(page_num,category):
    conn = httplib.HTTPConnection('www.proxy360.net')
    conn.request('GET','/%s/%s'%(category, page_num))
    response = conn.getresponse().read()
    #with open("response.html","w+") as f:
    #    f.write(response)
    conn.close()
    return _parse_response(response)

def _parse_response(response):
    tree = lxml.html.fromstring(response)
    sel = CSSSelector('#listtable tbody tr')
    col_sel = CSSSelector('td')
    style_sel = CSSSelector('style')
    span_sel = CSSSelector('span')
    speed_sel = CSSSelector('.progress-indicator div')

    rows = sel(tree)  
    proxies = []
    for row in rows:
        cols = col_sel(row)

        if len(cols) < 7:
            continue
        #cols[1]: ip
        #cols[2]: port
        #cols[3]: Country
        #cols[4]: speed
        #cols[6]: protocol
        p = theproxy()    
        
        styles = style_sel(cols[1])

        invisible_style = [string.replace(style,'{display:none}','').replace('.','') for style in string.split(styles[0].text_content()) if style.find('display:none') <> -1]          
                
        elems = cols[1].find('span')      

        ip = ''
        for elem in list(elems):
            if elem.tag == 'style':
                elem.text = ""
            if elem.tag == 'div' or elem.tag == 'span':
                if 'style' in elem.attrib and elem.attrib['style'] == 'display:none':
                    elem.text = ""
                if 'class' in elem.attrib and elem.attrib['class'] in invisible_style:
                    elem.text = ""

        p.ip = elems.text_content().strip()
        p.port = int(cols[2].text_content().strip())
        p.country = cols[3].attrib['rel'].strip()
        
        speed_str = lxml.html.tostring(cols[4])
        
        speed_re = re.compile(".*width: ([0-9]+)%.*")
        m_result = speed_re.match(speed_str)

        p.speed = int(m_result.group(1))
        p.protocol = cols[6].text_content().strip().lower()
        proxies.append(p)

    return proxies

def _get_page_numbers(category):
    conn = httplib.HTTPConnection('www.proxy360.net')
    conn.request('GET','/%s/'%category)
    response = conn.getresponse().read()
    tree = lxml.html.fromstring(response)
    sel = CSSSelector('div.pagination li a')
    rows = sel(tree) 
    page = 0
    for row in rows:
        try:
            if page < int(row.text_content()):
                page = int(row.text_content())
        except Exception,e:
            continue

    conn.close()

    return page

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


def scrape_proxies(category):
    proxies = []
    page_nums = _get_page_numbers(category)

    for i in range(1,page_nums+1):        
        proxies_page = _scrape_proxies("%d"%i, category)
        proxies_page_valid = [proxy for proxy in proxies_page]
        proxies.extend(proxies_page_valid)

    valid_proxies = [ {"ip":p.ip,"port":p.port,"protocol":p.protocol} for p in proxies if _test_proxy(p)]
    print len(valid_proxies),"/",len(proxies)

    with open("proxies_%s.txt" % category,"w+") as f:
        f.write(simplejson.dumps(valid_proxies))

if __name__ == "__main__":
#    with open("response.html","r") as f:
#        response = f.read()
#        proxies = _parse_response(response)
#        valid_proxies = [ p for p in proxies if _test_proxy(p)]
    
    #page_nums = _get_page_numbers()
    #print page_nums

    #scrape_proxies("guowai")
    proxy = theproxy()
    proxy.ip = "222.74.28.14"
    proxy.port = 23
    proxy.protocol = "http"
    _test_proxy(proxy)
   
                   
            
