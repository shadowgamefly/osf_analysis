import lxml.html as html
from util import *

def menu_parse(file) :
    source = load_pickle(file, 'html')
    root = html.fromstring(source)
    elements = root.xpath('.//a[text()="Go to article "]')
    return [e.get("href") for e in elements if "http://works.bepress.com/" in e.get("href")]

def content_parse(file) :
    source = load_pickle(file, 'html')
    root = html.fromstring(source)
    title = ""
    abstract = ""
    return title, abstract

if __name__ == '__main__':
    print(menu_parse('law_page15.pickle'))
