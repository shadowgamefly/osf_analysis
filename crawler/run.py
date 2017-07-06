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

def content_session(subject, dir):
    q, h, p = init(dir)
    while q:
        url = q[0]
        response, status = crawl_content(url)
        if status != 1:
            print('{:s} is not valid, continue'.format(url))
            q.pop(0)
            continue
        else :
            title, description,status = content_parse(response)
            if status != 1:
                print('{:s} has no abstract, continue'.format(url))
                q.pop(0)
                continue
            write_json(subject, title, description)
        q.pop(0)
        record_status(q, h, p)
        time.sleep(1)

def rename_json(subject, dir):
    count = 1
    json_dir = dir + "/cache/json/"
    for file in os.listdir(json_dir):
        os.rename("{:s}{:s}".format(json_dir, file), "{:s}{:d}.json".format(json_dir, count))
        count += 1
    with open("{:s}/cache/param/count.pickle".format(dir), 'wb') as f:
        pickle.dump(count, f)
    print(count)

if __name__ == '__main__':
    dir = os.getcwd()
    subject = 'social-and-behavioral-sciences'
    write_pickle('page', 'param', 1)
    menu_session(subject, dir)
