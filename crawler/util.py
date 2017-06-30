import os, shutil
import pickle
import queue

dir = os.getcwd()

def write_pickle(filename, type, obj):
    global dir
    with open(dir + '/cache/' + type + "/"+ filename + '.pickle', 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(filename, type):
    global dir
    try :
        with open(dir + '/cache/' + type + "/"+ filename, 'rb') as f:
            obj = pickle.load(f)
            return obj
    except FileNotFoundError:
        return None

def init(cur_dir):
    global dir
    dir = cur_dir
    try :
        os.mkdir(dir + '/cache')
        os.mkdir(dir + '/cache/html')
        os.mkdir(dir + '/cache/json')
        os.mkdir(dir + '/cache/param')
        q = []
        with open(dir + '/cache/param/queue.pickle', 'wb') as f:
            pickle.dump(q, f)
        h = set()
        with open(dir + '/cache/param/hash.pickle', 'wb') as f:
            pickle.dump(h, f)
        page = 1
        with open(dir + '/cache/param/page.pickle', 'wb') as f:
            pickle.dump(page, f)
        print("Initiation finished")
        return q, h, page
    except FileExistsError:
        print("Previous cache found, reloading...")
        return load_status()

def load_status():
    global dir
    try :
        with open(dir + '/cache/param/queue.pickle', 'rb') as f:
            q = pickle.load(f)
        with open(dir + '/cache/param/hash.pickle', 'rb') as f:
            h = pickle.load(f)
        with open(dir + '/cache/param/page.pickle', 'rb') as f:
            p = pickle.load(f)
        print("Finish reloading")
        return q, h, p
    except (FileNotFoundError, EOFError) as e:
        print("Previous cache incomplete, might require restart")
        while True:
            response = input("Do you want to reset the cache?[Y/N] ")
            if response == 'Y' :
                shutil.rmtree(dir + '/cache')
                return init()
            elif response == 'N' :
                raise e
            print("Please re-enter your response")

def record_status(q, h, p):
    global dir
    try :
        with open(dir + '/cache/param/queue.pickle', 'wb') as f:
            pickle.dump(q, f)
        with open(dir + '/cache/param/hash.pickle', 'wb') as f:
            pickle.dump(h, f)
        with open(dir + '/cache/param/page.pickle', 'wb') as f:
            pickle.dump(p, f)
        print("Finish dumping")
    except (FileNotFoundError, EOFError) as e:
        print(q, h, p)
        print("Dumping failed")
    return
