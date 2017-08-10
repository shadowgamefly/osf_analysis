from util import *
from crawler import *
from parser import *
import time

# menu session crawled the menu page of each taxonomy and stored them into a queue of urls
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

# content session grab urls from the queue created by menu session, and crawl the content of each url page and store them        
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

# used for rename the data crawled
def rename_json(subject, dir):
    count = 1
    json_dir = dir + "/cache/json/"
    for file in os.listdir(json_dir):
        os.rename("{:s}{:s}".format(json_dir, file), "{:s}{:d}.json".format(json_dir, count))
        count += 1
    with open("{:s}/cache/param/count.pickle".format(dir), 'wb') as f:
        pickle.dump(count, f)
    print(count)

# to run the crawler, one need to specify the subject to crawl, the directory to store the cache, then one can start
# the menu_session followed by content session. Multiple crawler can run in parallel with different taxonomy, and both 
# session save its own status upon each page reach. With minor change, menu session and content session can also run in parallel.
if __name__ == '__main__':
    dir = os.getcwd()
    subject = 'social-and-behavioral-sciences'
    content_session(subject, dir)
