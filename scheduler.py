import settings
from proxies.getproxies import scrape_proxies
import myproxy
import voter
import time
import sys
import random

def run(flag):
    if flag <> '-l':
        for i in range(10):
            try:
                scrape_proxies()
                break
            except:
                time.sleep(5)
                continue

    myproxy.load_proxy()
    
    proxy_nums = myproxy.proxy_nums()
    print "%d proxies loaded"%proxy_nums

    available_votes = proxy_nums * settings.MAX_VOTE_PER_IP

    interval = 1.0 * settings.TOTAL_TIME / available_votes

    vote_no = 0

    while True:
        p = myproxy.get_one_proxy()
        if len(p) == 0:
            print "out of proxy!"
            break
        voter.vote(p)
        vote_no = vote_no + 1
        next_inteval = interval + random.randint(int(-interval/2),int(interval/2))
        print "Vote:%d done with %s! Wait %d ms for next vote"%(vote_no,p["ip"].decode('utf-8').encode('gb2312'),next_inteval*1000)
        time.sleep(next_inteval)


if __name__ == "__main__":
    flag = ""
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    run(flag)