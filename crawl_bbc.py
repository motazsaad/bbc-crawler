import sys
import os
import requests
from bs4 import BeautifulSoup

crawled_links = set()



# the default recursion limit is 1000. It is a guard against a stack overflow
# sys.setrecursionlimit(1500) # doing so is dangerous.
share_string = ['شارك هذه الصفحة عبر', 'البريد الالكتروني', 'فيسبوك', 'Messenger', 'تويتر',
                'Google+', 'WhatsApp', 'LinkedIn', 'شارك عبر', 'هذه روابط خارجية وستفتح في نافذة جديدة',
                'None']


def crawl_links(web_url, keyword, out_dir, stop=1000):
    print(web_url)
    #sys.stdout.write("\rprint_links: {0}".format(len(crawled_links)))
    if len(crawled_links) > stop:
        return
    else:
        req = requests.get(web_url)
        html_doc = req.text
        date = req.headers['Date']
        soup = BeautifulSoup(html_doc, 'html.parser')
        filename = web_url.split('/')[-1]
        filename = str(filename) + ".txt"
        print(filename)
        file_writer = open(os.path.join(out_dir, filename), mode='w')
        file_writer.write(soup.title.string + '\n')
        file_writer.write(date + '\n')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            para = str(p.string).strip()
            if para and para not in share_string:
                file_writer.write(para + '\n')
        file_writer.close()
        more = soup.find(attrs={'class': "story-more"})
        if more:
            more_links = more.find_all('a')
            for link in more_links:
                my_link = str(link.get('href'))
                if my_link.startswith(keyword):
                    target_link = "http://www.bbc.com" + my_link
                    if target_link not in crawled_links:
                        print(target_link)
                        crawled_links.add(target_link)
                        crawl_links(target_link, keyword, out_dir)
        links = soup.find_all('a')
        for link in links:
            my_link = str(link.get('href'))
            if my_link.startswith(keyword):
                target_link = "http://www.bbc.com" + my_link
                if target_link not in crawled_links:
                    print(target_link)
                    crawled_links.add(target_link)
                    crawl_links(target_link, keyword, out_dir)


if __name__ == '__main__':
    bbc_news_url = [
        'http://www.bbc.com/arabic/world',
        'http://www.bbc.com/arabic/middleeast',
        'http://www.bbc.com/arabic/business',
        'http://www.bbc.com/arabic/sports'
    ]
    keywords = [
        '/arabic/world'
        '/arabic/middleeast',
        '/arabic/business',
        '/arabic/sports'
    ]
    if not os.path.exists('out'):
        os.mkdir('out')
    for url, key in zip(bbc_news_url, keywords):
        crawl_links(url, keyword=key, out_dir="out")
