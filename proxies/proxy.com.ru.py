# -*- coding: gbk -*-

from getproxies import *
import requests
import re

class proxydotcomscraper(proxyscraper):
    def __init__(self):
        proxyscraper.__init__(self)
        self.baseurl = "http://www.proxy.com.ru"
    def build_proxy_page_urls(self):
        r = requests.get(self.baseurl)
        response = r.text
        reg_exp = re.compile(".*共([0-9]+)页.*".decode("gbk").encode("utf-8"))
        print reg_exp
        result = reg_exp.match("共22页sdf".decode("gbk").encode("utf-8"))
        print result.groups(1)[0]
        page = int(result.groups(1)[0])
        self.proxy_page_urls = ["%s/list_%d.html"%(self.baseurl,p) for p in range(1,page+1) ]

    def _parse_response(self, response):
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


if __name__ == "__main__":
    ps = proxydotcomscraper()
    ps.build_proxy_page_urls()
    for p in ps.proxy_page_urls:
        print p
