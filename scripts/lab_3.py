from modules.vc_spider import VcSpider

if __name__ == '__main__':
    spider = VcSpider(limit=10)
    spider.walk()
