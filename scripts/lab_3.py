from modules.vc_spider import VcSpider

if __name__ == '__main__':
    spider = VcSpider(limit=1000)
    pages = spider.walk()
    print(pages)
