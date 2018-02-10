# -*- coding: utf-8 -*-
from scrapy import signals
from fake_useragent import UserAgent


class JdUserAgentMiddleware(object):

    def __init__(self, crawler):
        self.ua = UserAgent()
        self.ua_type = crawler

    @classmethod
    def from_crawler(cls, crawler):
        ua_type = cls(crawler.settings['USER_AGENT_TYPE'])
        return ua_type

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type, 'random')
        if get_ua():
            request.headers.setdefault('User-Agent', get_ua())