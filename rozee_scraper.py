from scrapy.crawler import CrawlerProcess
import scrapy
import re
import datetime
from pandas import DataFrame

uniqueUrls = []


class JobSpider(scrapy.Spider):
    start_urls = []
    name = "rozee_jobs_daily_counter"
    allowed_domains = ['rozee.pk']

    def parse(self, response):
        global uniqueUrls
        tag = response.request.url.split('/')[6]

        for href in response.selector.xpath('//div[@class="j-area"]//div[@class="jlist"]//a/@href').extract():
            if re.match(r".*.rozee.pk/job/jsearch/q/.*/\?fpn=.*", href):
                tag = href.split('/')[6]
                yield response.follow(href, self.parse)
            elif re.match(r".*.rozee.pk/.*-\d*.php.*&utm_campaign=rozee.pk_job_search", href):
                if href not in uniqueUrls:
                    uniqueUrls.append(href)
                    try:
                        comp = response.selector.xpath(
                            '//a[@href="'+href+'"]/../../div//a/text()').extract()
                        Company = comp[0].strip()
                        City = comp[1].strip()
                        Country = comp[2].strip()
                    except:
                        Company = None
                        City = None
                        Country = None

                    try:
                        Title = response.selector.xpath(
                            '//a[@href="'+href+'"]/bdi/text()').extract()[0].strip()
                    except:
                        Title = None

                    try:
                        Date = response.selector.xpath(
                            '//a[@href="'+href+'"]/../../../../div[@class="jfooter"]//i/../text()').extract()[1].strip()
                    except:
                        Date = None

                    try:
                        Experience = response.selector.xpath(
                            '//a[@href="'+href+'"]/../../../../div[@class="jfooter"]//span[@class="func-area-drn"]/text()').extract()[0].strip()
                    except:
                        Experience = None

                    try:
                        Description = response.selector.xpath(
                            '//a[@href="'+href+'"]/../../../../div[@class="jbody"]/bdi/text()').extract()[0].strip()
                    except:
                        Description = None

                    try:
                        Salary = response.selector.xpath(
                            ' //a[@href="'+href+'"]/../../../../div[@class="jfooter"]//i[@class="sal rz-salary"]/../text()').extract()[1].strip()
                    except:
                        Salary = None

                    data = {
                        'Title': Title,
                        'Company': Company,
                        'City': City,
                        'Country': Country,
                        'Date':  Date,
                        'Experience': Experience,
                        'Salary': Salary,
                        'Description': Description
                    }

                    # if tag != "":
                    yield {"tag": tag, "data": data}
                    # else:
                    #     yield None
                else:
                    yield None
            else:
                yield None


class MyPipeline(object):
    """ A custom pipeline that stores scrape results in 'results'"""
    results = []

    def process_item(self, item, spider):
        self.results.append(item)


class JobWrapper():

    def __init__(self, tags):
        self.start_urls = [
            "https://www.rozee.pk/job/jsearch/q/"+s+"/?fpn=0" for s in tags
        ]

    def run(self):
        process = CrawlerProcess({
            # An example of a custom setting
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            # Hooking in our custom pipline above
            'ITEM_PIPELINES': {'rozee_scraper.MyPipeline': 1},
            'LOG_LEVEL': 'ERROR'
        })

        process.crawl(JobSpider, start_urls=self.start_urls)
        process.start()  # the script will block here until the crawling is finished

        return MyPipeline.results


def run(tags):
    print("Starting scrapping...")
    job = JobWrapper(tags)
    data = job.run()

    df = DataFrame.from_dict(data)
    data = {tag: df.loc[df['tag'] == tag]["data"].tolist()
            for tag in tags}
    print("Complete scrapping...")
    return data
