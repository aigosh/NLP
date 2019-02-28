from lxml.html import fromstring
from lxml.cssselect import CSSSelector


def query_selector_all(tree, selector: str):
    selector = CSSSelector(selector)
    return selector(tree)


def query_selector(tree, selector: str):
    return query_selector_all(tree, selector)[0]


def get_title(html: str) -> str:
    html_tree = fromstring(html)
    tag = query_selector(html_tree, 'head>meta[property="og:title"]')

    content = tag.get('content')

    return content


def get_description(html: str) -> str:
    html_tree = fromstring(html)
    tag = query_selector(html_tree, 'head>meta[property="og:description"]')

    content = tag.get('content')

    return content


def extract_links_from_tags(links):
    return [link.get('href') for link in links]
