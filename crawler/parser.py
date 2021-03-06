import lxml.html as html
from util import *

# parse the menu page and get the urls on the mune
def menu_parse(source) :
    root = html.fromstring(source)
    elements = root.xpath('.//a[text()="Go to article "]')
    return [e.get("href") for e in elements if "http://works.bepress.com/" in e.get("href")]

# parse the content page with the abstract and the title
def content_parse(source) :
    root = html.fromstring(source)
    try :
        title = root.xpath('.//title')[0].text
        title = title[title.find('\"', 0) + 1 : title.find('\"', title.find('\"', 0) + 1)].encode('ascii', 'ignore').decode('ascii')
        abstract = root.xpath(".//meta[@name='description']")[1].get('content').encode('ascii', 'ignore').decode('ascii')
        return title, abstract, 1
    except IndexError:
        return title, "", -1

# test
if __name__ == '__main__':
    print(menu_parse('law_page15.pickle'))
