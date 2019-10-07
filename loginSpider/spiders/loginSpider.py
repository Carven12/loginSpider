import scrapy
from  scrapy import log


class LoginSpider(scrapy.Spider):

    name = "login_spider"
    # allowed_domains = ["dro.orange-business.com"]
    userName = 'XXX'
    password = 'XXx'

    start_urls = ['https://selfcare.cloud.orange-business.com']
    login_url = 'https://dro.orange-business.com'

    def parse(self, response):
        # xpath定位获取登录请求必要参数
        login_url = self.login_url + response.xpath('//*[@id="authenValidation"]').attrib['action']
        res_lg = response.xpath('//*[@id="authenValidation"]/input[@name="lg"]').attrib['value']
        res_csrfToken = response.xpath('//*[@id="authenValidation"]/input[@name="csrfToken"]').attrib['value']
        # 发起Form表单请求，并回调after_login
        return scrapy.FormRequest(
            login_url,
            formdata={
                'lg': res_lg,
                'csrfToken': res_csrfToken,
                'user': self.userName,
                'pwd': self.password
            },
            callback=self.after_login
        )

    def after_login(self, response):
        url = response.xpath('//form').attrib['action']
        SAMLResponse = response.xpath('//input[@name="SAMLResponse"]').attrib['value']
        # cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        return scrapy.FormRequest(
            url,
            formdata={
                'SAMLResponse': SAMLResponse
            },
            callback=self.get_account_access
        )

    # def parse_login_data(self, response):
    #     cookies_str = response.request.headers.getlist('Cookie')[0].decode()
    #     cookies_dict = self.stringToDict(cookies_str)
    #     with open("b.html", "w", encoding="utf-8") as f:
    #         f.write(response.body.decode())
    #     print(response)
    #     return scrapy.Request(
    #         'https://selfcare.cloud.orange-business.com/contracts/contracts',
    #         method='GET',
    #         cookies=cookies_dict,
    #         callback=self.get_user_info
    #     )


    def get_account_access(self, response):
        cookies_str = response.request.headers.getlist('Cookie')[0].decode()
        cookies_dict = self.stringToDict(cookies_str)
        return scrapy.Request(
            'https://selfcare.cloud.orange-business.com/contracts/contracts/OCB0001686/access',
            method='GET',
            cookies=cookies_dict,
            callback=self.set_current_contract_id
        )

    def set_current_contract_id(self, response):
        cookies_str = response.request.headers.getlist('Cookie')[0].decode()
        cookies_dict = self.stringToDict(cookies_str)
        return scrapy.Request(
            'https://selfcare.cloud.orange-business.com/currentcontractid/OCB0001686',
            method='put',
            cookies=cookies_dict,
            callback=self.parse_response
        )

    def parse_response(self, response):
        cookies_str = response.request.headers.getlist('Cookie')[0].decode()
        cookies_dict = self.stringToDict(cookies_str)


    def stringToDict(self, cookies):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = cookies.split(';')
        for item in items:
            arr = item.split('=')
            key = arr[0].replace(' ', '')
            value = arr[1]
            itemDict[key] = value
        return itemDict

# if __name__ == '__main__':
#     cmdline.execute("scrapy crawl spider_post".split())




