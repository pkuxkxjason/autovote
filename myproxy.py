import settings
import simplejson
import datetime

global_proxies = []

def proxy_nums():
    return len(global_proxies)

def load_proxy():
    global global_proxies
    local_proxies = []
    with open("proxies.txt","r") as f:
        local_proxies = simplejson.loads(f.read())
    for proxy in local_proxies:
        if proxy["ip"] not in global_proxies:
            proxy["times"] = 0
            proxy["last_use_time"] = datetime.datetime.now()
            global_proxies.append(proxy)

def get_one_proxy():
    global global_proxies
    if len(global_proxies) == 0:
        load_proxy()
    for p in global_proxies:
        if datetime.datetime.now() - p['last_use_time'] > datetime.timedelta(1):
            p['times'] = 0
            p['last_use_time'] = datetime.datetime.now()

    global_proxies = sorted(global_proxies,key=lambda proxy: proxy['times'])
    for p in global_proxies:
        if p['times'] < settings.MAX_VOTE_PER_IP:
            p['times'] = p['times'] + 1
            p['last_use_time'] = datetime.datetime.now()
            return p
    return {}

if __name__ == "__main__":
    print get_one_proxy()