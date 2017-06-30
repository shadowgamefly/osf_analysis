from util import *
from crawler import *
from parser import *
import time

if __name__ == '__main__':
    dir = os.getcwd()
    subject = 'law'
    q, h, p = init(dir)
    while True:
        url, status = crawl(subject, p, dir)
        if status != 1 :
            print("Crawling finished")
            break
        print("{:s} saved".format(url))
        p += 1
        record_status(q, h, p)
        time.sleep(5)
