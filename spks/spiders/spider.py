import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SpksItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class SpksSpider(scrapy.Spider):
	name = 'spks'
	start_urls = ['https://www.spks.dk/om_sparekassen/nyheder']

	def parse(self, response):
		post_links = response.xpath('//tr//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/text()').get()
		title = response.xpath('//h1[@itemprop="headline"]/text()').get().strip()
		content = response.xpath('//h3[@class="article__subheader"]//text()').getall() + response.xpath('//div[@class="article__content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SpksItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
