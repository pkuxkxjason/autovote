#!/usr/bin/python
import lxml.html
from lxml.cssselect import CSSSelector

import httplib
import string

class theproxy:
    def __init__(self):
        self.ip = ""
        self.port = ""
        self.protocol = ""
        self.country = ""
    def __str__(self):
        return "ip:%s\nport:%s\nprotocol:%sl\ncountry:%s\n"%(self.ip,self.port,self.protocol,self.country)

def _scrape_proxies():
    conn = httplib.HTTPConnection('www.proxy360.net')
    conn.request('GET','/guonei/')
    response = conn.getresponse().read()
    with open("response.html","w+") as f:
        f.write(response)

    return _pass_response(response)

def _pass_response(response):
    tree = lxml.html.fromstring(response)
    sel = CSSSelector('#listtable tbody tr')
    col_sel = CSSSelector('td')
    style_sel = CSSSelector('style')
    span_sel = CSSSelector('span')

    rows = sel(tree)  
    proxies = []
    for row in rows:
        cols = col_sel(row)
        #cols[1]: ip
        #cols[2]: port
        #cols[3]: Country
        #cols[6]: protocol
        p = theproxy()    
        
        styles = style_sel(cols[1])
        #for style in string.split(styles[0].text_content()):
        #    print style

        invisible_style = [string.replace(style,'{display:none}','').replace('.','') for style in string.split(styles[0].text_content()) if style.find('display:none') <> -1]          
                
        elems = cols[1].find('span')      

        #print elems.text_content()

        ip = ''
        for elem in list(elems):
            if elem.tag == 'style':
                elem.text = ""
            if elem.tag == 'div' or elem.tag == 'span':
                if 'style' in elem.attrib and elem.attrib['style'] == 'display:none':
                    elem.text = ""
                if 'class' in elem.attrib and elem.attrib['class'] in invisible_style:
                    elem.text = ""

        print elems.text_content()
        p.port = cols[2].text_content()        
        p.country = cols[3].attrib['rel']
        p.protocol = cols[6].text_content()
        proxies.append(p)

        
    
    return proxies


if __name__ == "__main__":
    with open("response.html","r") as f:
        response = f.read()
        proxies = _pass_response(response)
    #proxies = _scrape_proxies()
    #for p in proxies:
    #    print p
       