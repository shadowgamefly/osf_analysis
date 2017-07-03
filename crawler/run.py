from util import *
from crawler import *
from parser import *
import time

def menu_session(subject, dir):
    q, h, p = init(dir)
    while True:
        url, status = crawl_menu(subject, p, dir)
        if status != 1 :
            print("Crawling finished")
            break
        print("{:s} saved".format(url))
        links = menu_parse(subject + '_page' + str(p) + '.pickle')
        q += links
        p += 1
        print(q)
        record_status(q, h, p)
        time.sleep(5)

if __name__ == '__main__':
    dir = os.getcwd()
    subject = 'law'
    menu_session(subject, dir)
