# -*- coding: utf-8 -*-

# Define here the models for your scraped s
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/s.html

import scrapy


class JdItem(scrapy.Item):
    url = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    uid = scrapy.Field()
    subdomain = scrapy.Field()
    info = scrapy.Field()

class CommentItem(scrapy.Item):
    """商品评论详情"""
    # 商品id
    pid = scrapy.Field()
    title = scrapy.Field()
    # 用户名
    nick_name = scrapy.Field()
    view_count = scrapy.Field()
    # 2:iphone 21:wechat 4:android
    user_client = scrapy.Field()
    is_mobile = scrapy.Field()
    # plus会员 金牌会员
    user_level_name = scrapy.Field()
    user_level_id = scrapy.Field()
    # 京享值
    user_exp_value = scrapy.Field()
    plus_available = scrapy.Field()
    # 是否有回复
    recommend = scrapy.Field()

    reference_id = scrapy.Field()
    reference_name = scrapy.Field()
    is_top = scrapy.Field()
    # 评论创建时间
    comment_time = scrapy.Field()
    # 购买时间？？
    reference_time = scrapy.Field()
    content = scrapy.Field()
    # 产品三个类别
    first_category = scrapy.Field()
    second_category = scrapy.Field()
    third_category = scrapy.Field()
    # 打分
    score = scrapy.Field()
    useful_vote_count = scrapy.Field()
    useless_vote_count = scrapy.Field()

class SummaryItem(scrapy.Item):
    """商品评论总结"""
    # 商品id
    pid = scrapy.Field()
    title = scrapy.Field()
    good_rate_show = scrapy.Field()
    poor_rate_show = scrapy.Field()
    average_score = scrapy.Field()
    # 好评
    good_count = scrapy.Field()
    # 默认好评
    default_good_count = scrapy.Field()
    # 中评
    general_count = scrapy.Field()
    # 追评
    after_count = scrapy.Field()
    # 差评
    poor_count = scrapy.Field()