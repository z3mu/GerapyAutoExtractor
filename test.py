from lxml.html import HtmlElement, fromstring
from lxml import etree
import html
from gerapy_auto_extractor import extract_list, extract_detail, is_detail, is_list, probability_of_detail, \
    probability_of_list
from gerapy_auto_extractor.helpers import content, jsonify

html_1 = open('detail.html', encoding='utf-8').read()
element = fromstring(html=html_1)

METAS = [
    '//meta[starts-with(@property, "og:title")]/@content',
    '//meta[starts-with(@name, "og:title")]/@content',
    '//meta[starts-with(@property, "title")]/@content',
    '//meta[starts-with(@name, "title")]/@content',
    '//meta[starts-with(@property, "page:title")]/@content',
    '//meta[starts-with(@property, "ArticleTitle")]/@content',
    '//meta[starts-with(@name, "ArticleTitle")]/@content',
]

def extract_by_meta(element: HtmlElement) -> str:
    for xpath in METAS:
        title = element.xpath(xpath)
        if title:
            return ''.join(title)

def extract_by_title(element: HtmlElement) -> str:
    return ''.join(element.xpath('//title//text()')).strip()

def extract_by_h(element: HtmlElement) -> list[HtmlElement]:
    hs = element.xpath('//h1//text()|//h2//text()|//h3//text()')
    return hs or []

def similarity(s1, s2):
    if not s1 or not s2:
        return 0
    s1_set = set(list(s1))
    s2_set = set(list(s2))
    intersection = s1_set.intersection(s2_set)
    union = s1_set.union(s2_set)
    return len(intersection) / len(union)

def extract_title(element: HtmlElement):
    title_extracted_by_meta = extract_by_meta(element)
    title_extracted_by_h = extract_by_h(element)
    title_extracted_by_title = extract_by_title(element)

    if title_extracted_by_meta:
        return title_extracted_by_meta

    title_extracted_by_h = sorted(title_extracted_by_h, key=lambda x: similarity(x, title_extracted_by_title), reverse=True)
    if title_extracted_by_h:
        return title_extracted_by_h[0]

    return title_extracted_by_title

title_extracted_by_meta = extract_by_meta(element)
title_extracted_by_h = extract_by_h(element)
title_extracted_by_title = extract_by_title(element)
print(title_extracted_by_meta)
print(title_extracted_by_h)
print(title_extracted_by_title)


title = extract_title(element)
print(title)
res = extract_detail(html_1)
# print(res['content'])
# exit()
ss = etree.tostring(res['content'].xpath('.')[0], pretty_print=True, method='html').decode('utf-8')
ss = html.unescape(ss)
print(ss)
# print(res['content'])
