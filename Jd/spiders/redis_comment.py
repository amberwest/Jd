# -*- coding: utf-8 -*-
import json
import re

import logging
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from Jd.items import CommentItem, SummaryItem

# logger = logging.getLogger(__file__)


class JdCrawlSpider(RedisCrawlSpider):
    name = 'jd_comment'
    redis_key = 'jd_comment:start_urls'
    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={pid}&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&rid=0&fold=1'

    rules = (
        Rule(LinkExtractor(allow=('\w+\.jd\.com', ), restrict_css=('.cate_menu_lk', ),
                           deny=('mvd', 'e', 'z', 'dujia', 'gupiao', )), follow=True),
        Rule(LinkExtractor(allow=('[item|e]+\.jd\.com/\d+\.html$', )), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            pid = re.search('\d+', response.url).group()
            title = ''.join(response.css('.sku-name::text,#name h1::text').extract()).strip()
        except:
            pid = ''
            # logger.info('failed to get product\'s id %d', response.url)
        if pid:
            yield scrapy.Request(self.comment_url.format(pid=pid, page=0),
                                 meta={'pid': pid, 'page': 0, 'title':title},
                                 callback=self.parse_comment)

    def parse_comment(self, response):
        pid = response.meta.get('pid')
        page = response.meta.get('page')
        title = response.meta.get('title')
        # logger.info('getting comments from %s', response.url)

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            print('response is not a json')
        else:
            comments = data.get('comments')
            if comments:
                for comment in comments:
                    item = CommentItem()
                    item['pid'] = int(pid)
                    item['title'] = title
                    # 用户名
                    item['nick_name'] = comment['nickname']
                    item['view_count'] = comment['viewCount']
                    # 2:iphone 21:wechat 4:android
                    item['user_client'] = comment['userClient']
                    item['is_mobile'] = comment['isMobile']
                    # plus会员 金牌会员
                    item['user_level_name'] = comment['userLevelName']
                    item['user_level_id'] = comment['userLevelId']
                    # 京享值
                    item['user_exp_value'] = int(comment['userExpValue'])
                    item['plus_available'] = int(comment['plusAvailable'])
                    # 是否有回复
                    item['recommend'] = comment['recommend']

                    item['reference_id'] = comment['referenceId']
                    item['reference_name'] = comment['referenceName']
                    item['is_top'] = comment['isTop']
                    # 评论创建时间
                    item['comment_time'] = comment['creationTime']
                    # 购买时间？？
                    item['reference_time'] = comment['referenceTime']
                    item['content'] = comment['content']
                    # 产品三个类别
                    item['first_category'] = int(comment['firstCategory'])
                    item['second_category'] = int(comment['secondCategory'])
                    item['third_category'] = int(comment['thirdCategory'])
                    # 打分
                    item['score'] = int(comment['score'])
                    item['useful_vote_count'] = int(comment['usefulVoteCount'])
                    item['useless_vote_count'] = int(comment['uselessVoteCount'])
                    yield item

                page += 1
                yield scrapy.Request(self.comment_url.format(pid=pid, page=page),
                                     meta={"pid": pid, 'page': page, 'title': title},
                                     callback=self.parse_comment)
            else:
                summary = SummaryItem()
                summary['pid'] = pid
                summary['title'] = title
                summary['good_rate_show'] = data['productCommentSummary']['goodRateShow']
                summary['poor_rate_show'] = data['productCommentSummary']['poorRateShow']
                summary['average_score'] = data['productCommentSummary']['averageScore']
                # 好评
                summary['good_count'] = data['productCommentSummary']['goodCount']
                # 默认好评
                summary['default_good_count'] = data['productCommentSummary']['defaultGoodCount']
                # 中评
                summary['general_count'] = data['productCommentSummary']['generalCount']
                # 追评
                summary['after_count'] = data['productCommentSummary']['afterCount']
                # 差评
                summary['poor_count'] = data['productCommentSummary']['poorCount']
                yield summary
