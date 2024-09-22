from urllib import parse
import mimetypes
from knifes.media import MediaType, extension_to_media_type_dict
from typing import Optional, Union
from urllib.parse import urlparse
import os


def get_url_from_text(text):
    if not text:
        return text
    start_index = text.rfind('http://')
    if start_index == -1:
        start_index = text.rfind('https://')
    if start_index == -1:
        return None
    text = text[start_index:]
    # 去掉空格后内容
    end_index = text.find(' ')
    if end_index != -1:
        text = text[0:end_index]
    return text


# m.oasis.weibo.cn => weibo.cn
def get_domain_with_top_level_from_url(url) -> Optional[str]:
    if not url:
        return url
    u = parse.urlparse(url)
    host_list = u.hostname.split('.')
    if len(host_list) < 2:
        return None
    return host_list[-2].lower() + '.' + host_list[-1].lower()


# m.oasis.weibo.cn => weibo
def get_domain_from_url(url) -> Optional[str]:
    if not url:
        return url
    u = parse.urlparse(url)
    host_list = u.hostname.split('.')
    if len(host_list) < 2:
        return None
    return host_list[-2].lower()


# m.oasis.weibo.cn => oasis.weibo
def get_sub_domain_from_url(url) -> Optional[str]:
    if not url:
        return url
    u = parse.urlparse(url)
    host_list = u.hostname.split('.')
    if len(host_list) < 3:
        return None
    return host_list[-3].lower() + '.' + host_list[-2].lower()


# 目前支持video、audio、image类型，其他返回None
# fixed bug for 'http://v.example.com/o0/000bH9u0lx07TQ0OHwmA01041200Onth0E010.mp4?label=mp4_hd&template=852x480.28.0&ori=0&ps=1CwnkDw1GXwCQx&Expires=1645114865&ssig=8QbZXUCE85&KID=unistore,video'
def guess_media_type(url) -> Optional[MediaType]:
    url_without_query = url[:url.index('?')] if '?' in url else url
    mimetype, _ = mimetypes.guess_type(url_without_query)
    if not mimetype:
        return extension_to_media_type_dict.get(get_extension(url_without_query.lower()))
    if mimetype in ('application/x-mpegurl', 'application/vnd.apple.mpegurl'):   # .m3u8
        return MediaType.VIDEO
    try:
        return MediaType(mimetype.split('/')[0])
    except:
        return None


def parse_query(url, key_=None) -> Union[dict, str, None]:
    query_dict = dict(parse.parse_qsl(parse.urlparse(url).query))
    return query_dict.get(key_) if key_ else query_dict


def parse_path(url, index_: int = None) -> Union[list, str, None]:
    path_list = parse.urlparse(url).path.strip('/').split('/')
    if index_ is not None:
        return path_list[index_] if len(path_list) > index_ else None
    return path_list


def parse_url(url) -> (str, list, dict):
    """return (netloc、path_list, query_dict)"""
    parsed = parse.urlparse(url)
    return parsed.netloc, parsed.path.strip('/').split('/'), dict(parse.parse_qsl(parsed.query))


def sanitize_url(url, scheme='http'):
    """ Prepend protocol-less URLs with `http:` scheme in order to mitigate
    the number of unwanted failures due to missing protocol
    """
    if not url:
        return url
    if url.startswith('//'):
        return f'{scheme}:{url}'
    return url


def get_extension(url):
    return os.path.splitext(parse.urlparse(url).path)[1]


def is_http_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc]) and result.scheme in {'http', 'https'}

