from scrapy import Spider, Request
from carscom.items import CarscomItem
import re

class CarsSpider(Spider):

	name = 'cars_spider'
	allowed_urls = ['https://www.cars.com/']
	start_urls = ['https://www.cars.com/for-sale/searchresults.action/?page=1&perPage=100&rd=30&searchSource=PAGINATION&showMore=false&sort=relevance&stkTypId=28881&zc=10001&userSetIxt=true']

	def parse(self,response):

		global make_urls

		make_lst = response.xpath('//*[@class="dimension facet mkId always-open-desktop"]/ul')

		make_id = make_lst.xpath('./li/input/@value').extract()

		make_urls = ['https://www.cars.com/for-sale/searchresults.action/?mkId={}&page=1&perPage=100&rd=30&searchSource=GN_REFINEMENT&showMore=false&sort=relevance&stkTypId=28881&zc=10001&userSetIxt=true'.format(e) for e in make_id]

		for make_u in make_urls:
			yield Request(url = make_u, callback = self.parse_make_urls)



	def parse_make_urls(self, response):

		total_rec = re.sub(',', '', response.xpath('//*[@class="matchcount"]/span/text()').extract_first())
		page_nums = int(total_rec) // 100 
		page_urls = []

		for u in make_urls:
			page_urls.extend([u.replace('page=1', 'page={}').format(n) for n in range(1, page_nums+1)])


		for page_u in page_urls:
			yield Request(url = page_u, callback = self.parse_page_urls)


	def parse_page_urls(self, response):

		# Scrap the urls of each car on the page
		vehicle_urls = response.xpath('//*[@class="shop-srp-listings__listing-container"]/a/@href').extract()

		for v_u in vehicle_urls:
			yield Request(url = 'https://www.cars.com' + v_u, callback = self.parse_vehicle_details)


	def parse_vehicle_details(self, response):

		details = response.xpath('//*[@class="vdp-details-basics__list"]')
		det_lst = response.xpath('//*[@class="vdp-details-basics__list"]/li/strong/text()').extract()

		fuel = ''
		exter = ''
		cty = ''
		inter = ''
		hwy = ''
		drive = ''
		tran = ''
		eng = ''
		mileage = ''

		for i, e in enumerate(det_lst):
			if e == 'Fuel Type:':
				fuel = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Exterior Color:':
				exter = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'City MPG:':
				cty = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Interior Color:':
				inter = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Highway MPG:':
				hwy = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Drivetrain:':
				drive = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Transmission:':
				tran = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Engine:':
				eng = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()
			elif e == 'Mileage:':
				mileage = details.xpath('./li[%d]/span/text()'%(i+1)).extract_first()

		title = response.xpath('//h1[@class="cui-heading-2--secondary vehicle-info__title"]/text()').extract_first()
		year = re.search('\d{4} [A-za-z- ]+ [A-za-z0-9-]+', response.xpath('//h1[@class="cui-heading-2--secondary vehicle-info__title"]/text()').extract_first()).group().split()[0]
		made = re.search('\d{4} [A-za-z- ]+ [A-za-z0-9-]+', response.xpath('//h1[@class="cui-heading-2--secondary vehicle-info__title"]/text()').extract_first()).group().split()[1]
		price = response.xpath('//*[@class="vehicle-info__price"]//text()').extract_first()

		try:
			model = re.search('\d{4} [A-za-z- ]+ [A-za-z0-9-]+', response.xpath('//h1[@class="cui-heading-2--secondary vehicle-info__title"]/text()').extract_first()).group().split()[2]
		except TypeError:
			mdoel = ''

		try:
			slrzip = re.findall('\d{5}', response.xpath('//*[@class="get-directions-link seller-details-location__text"]/a/text()').extract_first())[0]
		except TypeError:
			slrzip = ''

		try:
			slreview = re.findall('(\d.\d|\d)', response.xpath('//*[@class="rating__link rating__link--has-reviews"]/text()').extract_first())[0]
		except TypeError:
			slreview = ''
			

		item = CarscomItem()
		item['title'] = title
		item['year'] = year
		item['made'] = made
		item['model'] = model
		item['price'] = price
		item['slrzip'] = slrzip
		item['slreview'] = slreview
		item['fuel'] = fuel
		item['exter'] = exter
		item['cty'] = cty
		item['inter'] = inter
		item['hwy'] = hwy
		item['drive'] = drive
		item['tran'] = tran
		item['eng'] = eng
		item['mileage'] = mileage

		yield item