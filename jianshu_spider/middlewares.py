"""
页面加载相关设置
"""

# -*- coding: utf-8 -*-
from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse


class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\Users\ThinkPad\Desktop\p3\chromedriver.exe'
        )

    def process_request(self,request,spider):
            self.driver.get(request.url)
            self.driver.refresh()
            time.sleep(1)
            try:
                while True:  
                    showMore = self.driver.find_element_by_class_name("show-more")
                    showMore.click()
                    time.sleep(0.3)
                    if not showMore:
                        break
            except:
                pass

            source = self.driver.page_source
            print(type(source))

            time.sleep(1)
            response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding="utf-8")
            return response





