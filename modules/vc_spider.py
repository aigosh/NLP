from requests import get
from ftfy import fix_text
from modules.html import get_title, query_selector, query_selector_all, extract_links_from_tags, get_description
from lxml.html import fromstring
from multiprocessing import Pool
import json


class VcSpider:
    pages = []
    url = 'https://vc.ru'
    pool = Pool()

    def __init__(self, limit=None):
        self._limit = limit

    def _get_subs_links(self):
        response = get(self.url + '/subs')
        html = response.content
        subs_selector = ".subsites_tune > .subsites_tune__list a"
        links = query_selector_all(fromstring(html), subs_selector)

        return extract_links_from_tags(links)

    def _get_news(self, etree: str):
        selector = ".feed__item"
        links = query_selector_all(etree, selector)

        return links

    def _get_news_link(self, node):
        subs_selector = ".entry_content__link"
        links = query_selector(node, subs_selector)

        return extract_links_from_tags([links])[0]

    def _parse_last_id(self, feeds):
        attr = "data-content-id"
        selector = "[{}]".format(attr)
        return query_selector(feeds, selector).get(attr)

    def _parse_last_sorting_value(self, feed):
        attr = "data-feed-last-sorting-value"
        selector = "[{}]".format(attr)
        return query_selector(feed, selector).get(attr)

    def _get_last_feed_id(self, etree):
        pass

    def _fetch_chunk(self, url, last_sorting_value, last_feed_id):
        response = get(url + "/entries/more?last_id={}&last_sorting_value={}".format(last_feed_id, last_sorting_value))
        data = json.loads(response.content)
        inner = data['data']
        html = inner['items_html']
        last_id = inner['last_id']
        last_sorting_value = inner['last_sorting_value']

        return html, last_sorting_value, last_id

    def _parse_page(self, etree):
        news = self._get_news(etree)
        for feed in news:
            if self._is_limited():
                return

            link = self._get_news_link(feed)
            feed_response = get(link)
            feed_html = feed_response.content
            title = fix_text(get_title(feed_html))
            descr = fix_text(get_description(feed_html))
            page = (link, (title, descr))
            print(page)
            self.pages.append(page)

    def _walk_sub(self, sub_link: str):
        response = get(sub_link)
        html = response.content
        etree = fromstring(html)
        last_id = self._parse_last_id(etree)
        last_sorting_value = self._parse_last_sorting_value(etree)

        self._parse_page(etree)

        while not self._is_limited():
            feeds, last_sorting_value, last_id = self._fetch_chunk(sub_link, last_sorting_value, last_id)
            self._parse_page(fromstring(feeds))

    def _is_limited(self):
        return len(self.pages) > self._limit

    def walk(self):
        subs = self._get_subs_links()
        for sub_link in subs:
            if self._is_limited():
                return self.pages

            self._walk_sub(sub_link)

        #     self.pool.apply_async(lambda x: self._walk_sub, args=(sub_link,))
        # self.pool.close()
        # self.pool.join()