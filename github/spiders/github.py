from github.items import GithubItem
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    url = 'https://github.com/search?l=Objective-C&o=desc&q=ios&s=stars&p='
    offset = 1
    start_urls = [
        url+str(offset)
    ]
    # 所有的模型
    items = []
    # 保存clone_url
    clone_urls = []

    def parse(self, response):
        # parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()

        names = response.xpath('//ul[@class=\"repo-list\"]/li/div/h3/a/text()').extract()
        # 访问url全路径,前面需要拼接:https://github.com
        urls = response.xpath('//ul[@class=\"repo-list\"]/li/div/h3/a/@href').extract()
        star_numbers:list = response.xpath('//ul[@class=\"repo-list\"]/li/div//a[@class=\"muted-link\"]/text()').extract()

        # 去掉无效值及空白回车
        for i in range(len(star_numbers)-1, -1, -1):
            temp:str = star_numbers[i].strip()
            if len(temp) > 2 or temp.find('k')!=-1:
                star_numbers[i] = temp

        update_times = response.xpath('//ul[@class=\"repo-list\"]/li/div//p[@class=\"f6 text-gray mr-3 mb-0 mt-2\"]/relative-time/text()').extract()
        for i in range(0, len(names)):
            item = GithubItem()

            item['name'] = names[i]
            item['url'] = 'https://github.com' + urls[i]
            item['star_number'] = star_numbers[i]
            item['update_time'] = update_times[i]
            self.items.append(item)

        for item in self.items:
            yield scrapy.Request(url=item['url'], meta={'item':item}, callback=self.parse_article)

        if self.offset < 3:
            self.offset += 1

        # 每次处理完一页的数据之后，重新发送下一页页面请求
        yield scrapy.Request(self.url+str(self.offset), callback=self.parse)

    def parse_article(self, response):
        """
        解析框架主页,提取其中的clone地址
        :param response:
        :return:
        """
        item = response.meta['item']
        item['clone_url'] = response.xpath('//div[@class=\"input-group\"]/input/@value').extract()
        self.clone_urls.append(item['url'])
        print('clone_url: %s'%self.clone_urls)
        # print(item)
