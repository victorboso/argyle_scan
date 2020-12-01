import scrapy
from scrapy_splash import SplashRequest
import re
import demjson
import json

script_login = """
function main(splash)
  splash.resource_timeout = 10
  splash:init_cookies(splash.args.cookies)
  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(3))
  
  splash:set_viewport_full()
  
  
  local search_input_username = splash:select('#login_username')
  search_input_username:send_text("bob-veryhardwork")
  assert(splash:wait(3))
  
  local submit_button_username = splash:select('#login_password_continue')
  submit_button_username:click()
  assert(splash:wait(3))
  
  
  local search_input_password = splash:select('#login_password')
  search_input_password:send_text("Argyleawesome123!")
  assert(splash:wait(3))
  
  local submit_button_password = splash:select('#login_control_continue')
  submit_button_password:click()
  assert(splash:wait(7))
  
  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    headers = last_response.headers,
    http_status = last_response.status,
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
end
"""


class UpworkSpider(scrapy.Spider):
    name = 'upwork'
    save_profile = False

    def __init__(self, da_user=None, *args, **kwargs):
        super(UpworkSpider, self).__init__(*args, **kwargs)
        if da_user:
            self.da_user = da_user

    def start_requests(self):
        yield SplashRequest("https://www.upwork.com/ab/account-security/login", self.parse_login,
                            endpoint='execute',
                            cache_args=['lua_source'],
                            args={'lua_source': script_login},
                            session_id="foo"
                            )

    def parse_login(self, response):
        pattern = '"label":"Settings","link":"(.*?)"'
        path = re.findall(pattern, response.text)[0].replace('\\', '')
        xsrf_token = next(item["value"] for item in response.data['cookies'] if item["name"] == "XSRF-TOKEN")
        master_access_token = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "master_access_token")
        odesk_signup_referer_raw = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "odesk_signup.referer.raw")
        user_uid = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "user_uid")
        session_id = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "session_id")
        oauth2_global_js_token = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "oauth2_global_js_token")
        user_oauth2_slave_access_token = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "user_oauth2_slave_access_token")
        sz = next(
            item["value"] for item in response.data['cookies'] if item["name"] == "SZ")
        authorization = "Bearer " + next(
            item["value"] for item in response.data['cookies'] if item["name"] == "oauth2_global_js_token")

        headers = {
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9,pt;q=0.8,it;q=0.7",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        cookies = {
            "odesk_signup.referer.raw": odesk_signup_referer_raw,
            "user_uid": user_uid,
            "session_id": session_id,
            "master_access_token": master_access_token,
            "oauth2_global_js_token": oauth2_global_js_token,
            "user_oauth2_slave_access_token": user_oauth2_slave_access_token,
            "SZ": sz,
            "DA[bob-veryhardwork]": self.da_user,
            "XSRF-TOKEN": xsrf_token
        }
        req = scrapy.Request("https://www.upwork.com" + path, callback=self.get_profile_settings,
                             headers=headers,
                             cookies=cookies
                             )
        req.meta['authorization'] = authorization
        req.meta['xsrf_token'] = xsrf_token
        req.meta['cookies_login'] = response.data['cookies']
        yield req

    def get_profile_settings(self, response):
        main_data = response.xpath('//script[contains(., "var phpVars")]/text()').extract_first()
        obj_to = re.findall('var phpVars = (.*);', main_data)[0]
        py_obj = demjson.decode(obj_to)
        freelancer = demjson.decode(py_obj['freelancer'])

        user_profile = {
            "username": freelancer['3']['str'],
            "name": freelancer['4']['str'],
            "last_name": freelancer['5']['str'],
            "email": freelancer['6']['rec']['1']['str'],
            "street": freelancer['7']['rec']['1']['str'],
            "number": freelancer['7']['rec']['2']['str'],
            "state": freelancer['7']['rec']['3']['str'],
            "city": freelancer['7']['rec']['5']['str'],
            "zip_code": freelancer['7']['rec']['6']['str'],
            "phone": freelancer['8']['str'],
            "img_profile": freelancer['10']['rec']['1']['str']
        }

        headers = {
            ":authority": "www.upwork.com",
            ":method": "GET",
            ":path": "/ab/find-work/api/feeds/search?user_location_match=1",
            ":scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,pt;q=0.8,it;q=0.7",
            "authorization": response.meta['authorization'],
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "x-oauth2-required": "true",
            "x-odesk-csrf-token": response.meta['xsrf_token'],
            "x-odesk-user-agent": "oDesk LM",
            "x-requested-with": "XMLHttpRequest"
        }

        req = scrapy.FormRequest(url="https://www.upwork.com/ab/find-work/api/feeds/search?user_location_match=1",
                                 callback=self.parse_pagination, method='GET',
                                 headers=headers,
                                 cookies=response.meta['cookies_login'])
        req.meta['headers'] = headers
        req.meta['cookies_login'] = response.meta['cookies_login']
        req.meta['user_profile'] = user_profile
        yield req

    def parse_pagination(self, response):
        data = json.loads(response.body_as_unicode())
        result_set_ts = data['paging']['resultSetTs']
        total_items = data['paging']['total']
        for page in range(0, total_items, 10):
            url = 'https://www.upwork.com/ab/find-work/api/feeds/search?max_result_set_ts={}&paging={};10&user_location_match=1'.format(
                result_set_ts,
                page
            )
            req = scrapy.FormRequest(url=url,
                                     callback=self.parse_result_main_page, method='GET',
                                     headers=response.meta['headers'],
                                     cookies=response.meta['cookies_login'])
            req.meta['user_profile'] = response.meta['user_profile']
            yield req

    def parse_result_main_page(self, response):
        data = json.loads(response.body_as_unicode())
        user_profile = response.meta['user_profile']
        for result in data['results']:
            if not self.save_profile:
                self.save_profile = True
                yield user_profile
            yield result
