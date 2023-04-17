import hashlib
import os
from datetime import datetime, date, time
from datetime import datetime, timedelta
import pymongo
import scrapy
import requests
from colorama import Fore
from parsel import Selector
from scrapy.cmdline import execute
from pymongo import MongoClient

from vesselfinder.items import VesselfinderItem


class News1Spider(scrapy.Spider):
    name = 'news_1'
    # allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    def __init__(self):
        self.conne=MongoClient()
        self.test = self.conne['vesselfinder']
        self.final = self.test['news_14']
        self.category = self.test['category']
        self.final.create_index('Hash_id',unique=True)
        # self.return_final.create_index('Hash_id', unique=True)
        # self.return_final = self.test['']

    def get_Data(self):
        print("data")

    def start_requests(self):
        record = self.category.find({"status": 'pending','No':'2'}, no_cursor_timeout=True)
        for j in record:
            id=j['No']
            category_url=j['category links']
            category=j['category']


            url=category_url

            url = url

            payload = {}
            headers = {
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-US,en;q=0.9',
                'cache-control':'max-age=0',
                'cookie':'_ga_0MB1EVE8B7=GS1.1.1681130340.1.0.1681130340.0.0.0; _ga=GA1.1.1494201586.1681130340; _gcl_au=1.1.685194021.1681130341',
                'sec-ch-ua':'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile':'?0',
                'sec-ch-ua-platform':'"Windows"',
                'sec-fetch-dest':'document',
                'sec-fetch-mode':'navigate',
                'sec-fetch-site':'none',
                'sec-fetch-user':'?1',
                'upgrade-insecure-requests':'1',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }
            count = 0
            yield scrapy.Request(method='GET',url=url, headers=headers,callback=self.parse,meta={'url':url,'count':count,'id':id,'category':category})
        # response = requests.request("GET", url, headers=headers, data=payload)

    def parse(self, response, **kwargs):

        item = VesselfinderItem()
        data=response.text
        count=response.meta['count']+1
        url=response.meta['url']
        dir = f"E:\\\\Parth\\\\News\\\\pagesave\\\\vesselfinder_17\\\\"  # E:\Parth\News\pagesave
        try:
            if not os.path.exists(dir):
                os.mkdir(dir)
        except Exception as e:
            print(e)
        item['homepage_path'] = dir + str(f"{count}") + '.html'
        with open(item['homepage_path'], 'w+', encoding="utf8") as f:
            f.write(response.text)
            f.close()

        data=Selector(response.text)
        try:
            all_div=data.xpath('//section[@class="listing"]/div[@class="row"]')
        except Exception as e:
            print(e)

        p_count = 0
        for k in all_div:

            try:
                item['Headline']=k.xpath('.//h2[@class="atitle"]/a/text()').get()
            except:
                item['Headline']=''
            try:
                Published_date=k.xpath('.//div[@class="col7"]/div[2]//text()').get().replace('/','').strip()
            except:
                Published_date=''
            strp_publisheddate = Published_date.replace(',','')
            datetime_object = datetime.strptime(strp_publisheddate, '%b %d %Y')
            item['Published_date']=datetime_object.strftime('%d-%m-%Y')
            code_dates00 = datetime.strftime(datetime_object, '%Y-%m-%d')
            code_dates=datetime.strptime(code_dates00, '%Y-%m-%d')

            row_fix_dates=datetime(2022,10,14)



            item['Post_Category']=response.meta['category']

            try:
                content_slug=k.xpath('.//h2[@class="atitle"]/a/@href').get()
                #https://www.vesselfinder.com/news/25996-Austal-Australia-And-Gotland-Sign-MoU-To-Develop-Design-For-130-Metre-High-Speed-Catamaran
                item['Aricle_Page_Url']=f'https://www.vesselfinder.com{content_slug}'
            except:
                content=''

            item['Updated']=''

            item['Term_badge']=''
            item['timestamp']=datetime.now()
            

            url_content = item['Aricle_Page_Url']

            payload = {}
            headers = {
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-US,en;q=0.9',
                # 'cache-control':'max-age=0',
                # 'cookie':'_ga=GA1.1.1494201586.1681130340; _gcl_au=1.1.685194021.1681130341; _ga_0MB1EVE8B7=GS1.1.1681219873.3.1.1681221307.0.0.0',
                # 'referer':'https://www.vesselfinder.com/news',
                # 'sec-ch-ua':'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                # 'sec-ch-ua-mobile':'?0',
                # 'sec-ch-ua-platform':'"Windows"',
                # 'sec-fetch-dest':'document',
                # 'sec-fetch-mode':'navigate',
                # 'sec-fetch-site':'same-origin',
                # 'sec-fetch-user':'?1',
                # 'upgrade-insecure-requests':'1',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }

            content_response = requests.request("GET", url_content, headers=headers, data=payload)

            content_xpath=Selector(content_response.text)
            p_count+=1
            dirrr = f"E:\\\\Parth\\\\News\\\\pagesave\\\\vesselfinder_nextpage\\\\"  # E:\Parth\News\pagesave
            try:
                if not os.path.exists(dirrr):
                    os.mkdir(dirrr)
            except Exception as e:
                print(e)
            item['mainpage_path'] = dirrr + str(f"{count}_{p_count}") + '.html'
            with open(item['mainpage_path'], 'w+', encoding="utf8") as f:
                f.write(response.text)
                f.close()
            try:
                item['Hash_tag'] = "|".join(content_xpath.xpath('//section[@class="sec tags-holder"]/a/text()').getall())
            except:
                item['Hash_tag']=''
            try:
                item['Attached_img_URL']=k.xpath('./div[@class="col5"]/a/img/@srcset').get()

            except:
                item['Attached_img_URL']=''
            try:
                content00=content_xpath.xpath('//section[@class="article-body"]/p//text()').getall()
                item['content_data']=''.join(content00)
            except:
                item['content_data']=''
            try:
                hash_utf8 = (f"{item['Aricle_Page_Url']}{item['Headline']}{item['Published_date']}{item['content_data']}").encode('utf8')

                item['Hash_id'] = int(hashlib.md5(hash_utf8).hexdigest(), 32) % (10 ** 9)

            except Exception as e:
                print(e)


            if code_dates > row_fix_dates:
                try:
                    self.final.insert_one(dict(item))
                    print(Fore.GREEN + f"{['return_Class']}>>>>>>>>>>>>INSERTED DATA...")

                except Exception as e:
                    print(e)
            else:
                continue
        try:
            next_page=data.xpath('//a[@rel="next"]/@href').get()
            try:
                url=f'https://www.vesselfinder.com{next_page}'
                count+=1
                try:
                    yield scrapy.Request(method='GET', url=url, headers=headers,meta={'count': count,'url':url,'category':item['Post_Category']})
                except Exception as e:
                    print(e)

            except:
                next_page=''
        except:
            next_page=''
        # if next_page=='':
        #https://www.vesselfinder.com/news?page=2&category=1






if __name__ == '__main__':
    execute('scrapy crawl news_1'.split())
        
        
        
