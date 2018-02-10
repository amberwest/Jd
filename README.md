### Jd

使用scrapy_redis爬取京东评论

##### spider.py
* 继承RedisSpider(如果要使用CrawlSpider需要多继承)
* 设置redis_key
* 不用写start_urls

##### settings.py
* 添加参数并开启redispipeline
```
# 确保所有的爬虫通过redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_ORDER = 'BFO'
# 不清除redis队列，这样可以暂停/恢复 爬取
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300,
    }
```
* 设置数据库redis字段
```
REDIS_URL = None
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PARAMS = {
    'password': '',
    'db': 1
}
```

##### 启动redis
* 登录redis
```
redis-server
redis-cli -a password
```
* 选择对应数据库并输入start_url

```
127.0.0.1:6379> select 1
OK
127.0.0.1:6379[1]> lpush jd_comment:start_urls http://jd.com
(integer) 1```