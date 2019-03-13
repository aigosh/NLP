from modules.vc_spider import VcSpider
from modules.db import create_db, write_pages, read_pages

if __name__ == '__main__':
    table_name = "articles"
    db = create_db("../articles.sqlite", table_name)

    def write_pages_to_db(pages):
        write_pages(db, table_name, pages)


    spider = VcSpider(limit=10, on_batch=write_pages_to_db)
    spider.walk()

    print(read_pages(db, table_name))

