from urllib import request
import urllib
from util import *

def crawl_menu(subject, page, cache):
    url = "http://network.bepress.com/" + subject + "/page"+ str(page)
    response = request.urlopen(url)
    source = response.read().decode("utf-8")
    if response.getcode() != 200 :
        return url, -1
    write_pickle(subject + '_page' + str(page), 'html', source)
    return url, 1

def crawl_content(url):
    try :
        response = request.urlopen(url)
        source = response.read().decode("utf-8")
        return source, 1
    except urllib.error.HTTPError :
        return url, -1
