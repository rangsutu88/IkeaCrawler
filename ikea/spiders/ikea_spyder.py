from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from ikea.items import IkeaItem

class IkeaSpider(CrawlSpider):
    name = "ikea"
    allowed_domains = ["ikea.com"]
    start_urls = [
        "http://www.ikea.com/de/de/catalog/allproducts/",
    ]
    extractor = LinkExtractor()

#    rules = (
#        Rule(extractor, callback='parse_links', follow=True),
#    )

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('de/de/catalog/products/.*', )), callback='parse_item'),

        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor()),
    )

    def parse_item(self, response):
        #self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        print('\nFound product URL-> {}'.format(response.url))
        item = IkeaItem()
        item['description'] = hxs.select('string(/html/head/meta[@name="og:description"]/@content)').extract()
        item['keywords'] = hxs.select('string(/html/head/meta[@name="keywords"]/@content)').extract()
        item['country'] = hxs.select('/html/head/meta[@name="country"]/@content').extract()
        item['language'] = hxs.select('/html/head/meta[@name="language"]/@content').extract()
        item['store_id'] = hxs.select('/html/head/meta[@name="store_id"]/@content').extract()
        item['title'] = hxs.select('/html/head/meta[@name="title"]/@content').extract()
        item['product_name'] = hxs.select('/html/head/meta[@name="product_name"]/@content').extract()
        item['category_name'] = hxs.select('/html/head/meta[@name="category_name"]/@content').extract()
        item['subcategory_id'] = hxs.select('/html/head/meta[@name="subcategory_id"]/@content').extract()
        item['price'] = hxs.select('/html/head/meta[@name="price"]/@content').extract()
        item['price_other'] = hxs.select('/html/head/meta[@name="price_other"]/@content').extract()
        item['changed_family_price'] = hxs.select('/html/head/meta[@name="changed_family_price"]/@content').extract()
        item['changed_family_price_other'] = hxs.select('/html/head/meta[@name="changed_family_price_other"]/@content').extract()
        item['item_id'] = hxs.select('/html/head/meta[@name="item_id"]/@content').extract()
        item['partnumber'] = hxs.select('/html/head/meta[@name="partnumber"]/@content').extract()
        item['url'] = [response.url]
        item['image'] = hxs.select('/html/head/meta[@property="og:image"]/@content').extract()
        return item

    def _page(self, response):
        hxs = HtmlXPathSelector(response)
        #Products selection
        #products = codecs.decode(hxs.select("//div[@class='productInformation']"), 'unicode-escape')
        productName = hxs.select("div[@id='schemaProductPrice']").extract()
        print("holaaaaa")
        print(productName)
        #item["link"] = post.select("div[@class='bodytext']/h2/a/@href").extract()
        #item["content"] = post.select("div[@class='bodytext']/p/text()").extract()
        #items.append(item)
        #for item in items:
        #yield item
