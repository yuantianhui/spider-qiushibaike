# -*- coding: utf-8 -*-
import scrapy
# 导入数据模型
from qiubaipro.items import QiubaiproItem

class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/']

    # 如果要爬取指定页码
    page = 1
    url = 'https://www.qiushibaike.com/8hr/page/{}/'

    def parse(self, response):
        # 先查找得到所有的div
        div_list = response.xpath('//div[@id="content-left"]/div')
        # 遍历每一个div，获取每一个div的属性
        for odiv in div_list:
        	# 创建一个对象
        	item = QiubaiproItem()
        	# 获取头像
        	image_url = odiv.xpath('.//div//img/@src')[0].extract()
        	# 获取名字
        	name = odiv.css('.author h2::text').extract()[0].strip('\n')
        	# 获取年龄
        	try:
        		age = odiv.xpath('.//div[starts-with(@class,"articleGender")]/text()')[0].extract()
        	except Exception as e:
        		age = '没有年龄'
        	
        	# 获取内容
        	lt = odiv.css('.content > span::text').extract()
        	content = ''.join(lt).rstrip('查看全文').replace('\n', '')
        	# 获取好笑个数
        	haha_count = odiv.xpath('.//i[@class="number"]/text()').extract()[0]
        	# 获取评论个数
        	ping_count = odiv.xpath('.//i[@class="number"]/text()').extract()[1]
        	# 依次保存到item中
        	item['image_url'] = image_url
        	item['name'] = name
        	item['age'] = age
        	item['content'] = content
        	item['haha_count'] = haha_count
        	item['ping_count'] = ping_count

        	fields = ['image_url', 'name', 'age', 'content', 'haha_count', 'ping_count']
        	for field in item.fields:
        		item[field] = eval(field)

        	# 将item扔给引擎
        	yield item

        # 判断，并且接着发送请求
        if self.page < 5:
        	self.page += 1
        	url = self.url.format(self.page)
        	yield scrapy.Request(url=url, callback=self.parse)

