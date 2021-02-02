import scrapy


class TjSpider(scrapy.Spider):
    name = 'tj'
    # allowed_domains = ['tiaoji.com']
    start_urls = ['http://www.chinakaoyan.com/tiaoji/schoollist/pagenum/1.shtml']

    def parse(self, response):
        links = response.xpath('//span[@class="title"]/a/@href').getall()
        for link in links:
            # print(link)
            yield response.follow(url=link, callback=self.parse_detail)
        pages = response.xpath('//div[@class="dajax"]/a/@href').getall()
        if pages:
            for one_page in pages:
                yield response.follow(url=one_page, callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath('//div[@class="t-header"]/h1/text()').get()
        s_name = response.xpath('//div[@class="student-info"]/div[@class="s-item font16"][1]/span[@class="name sw"]/text()').get()

        loc = response.xpath('//div[@class="student-info"]/div[@class="s-item font16"][1]/span[@class="num"]/text()').get()
        # print(title, s_name, loc)
        zhuanye = response.xpath('//div[@class="student-info"]/div[@class="s-item font16"][2]/span[@class="name sw"]/text()').get()
        gonfei_num = response.xpath('//div[@class="student-info"]/div[@class="s-item font16"][2]/span[@class="num"]/text()').get()
        # print(zhuanye, gonfei_num)
        release_time = response.xpath('//div[@class="student-info"]/div[@class="s-item font16"][3]/span[@class="name sw"]/text()').get()
        end_time = response.xpath('//div[@class="student-info"]/div[@class="s-item font16"][3]/span[@class="num"]/text()').get()
        # print(release_time, end_time)
        content_li = response.xpath('//div[@class="student-body font14"]/p//text()').getall()
        content = '_'.join(x.strip() for x in content_li)
        # print(content)

        item = {}
        item['title'] = title
        item['s_name'] = s_name
        item['loc'] = loc
        item['zhuanye'] = zhuanye
        item['gonfei_num'] = gonfei_num
        item['release_time'] = release_time
        item['end_time'] = end_time
        item['content'] = content
        yield item