from util import *
from crawler import *
from parser import *
import time

def menu_session(subject, dir):
    q, h, p = init(dir)
    while True:
        error = 0
        try :
            source = crawl_menu(subject, p, dir)
            error = 0
        except Exception:
            error += 1
            if error > 2 :
                print("stop at page {:d} with queue {:d}".format(p, len(q)))
                break                
            continue
        links = menu_parse(source)
        q += links
        p += 1
        print(len(q))
        record_status(q, h, p)
        time.sleep(1)

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
    content_session(subject, dir)
