from aiohttp import ClientSession
from selectolax.parser import HTMLParser
from dataclasses import dataclass, field
from httpx import Client
from typing import List
from random import choice

@dataclass
class Agency:
    website: str
    contact: str
    office: str
    phone: str
    gov_branch: str

@dataclass
class Usagov:
    baseurl: str = 'https://www.usa.gov'
    proxies: List[str] = field(default_factory=lambda: [
        '142.214.181.36:8800',
        '142.214.181.241:8800',
        '196.51.116.40:8800',
        '196.51.114.196:8800',
        '142.214.181.41:8800',
        '196.51.116.171:8800',
        '142.214.181.219:8800',
        '142.214.183.243:8800',
        '196.51.114.248:8800',
        '142.214.183.70:8800'
    ])
    useragent: List[str] = field(default_factory=lambda: [
        'Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.137 Safari/537.36 Ubuntu/22.04 (5.0.2497.35-1) Vivaldi/5.0.2497.35',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.48-1) Vivaldi/5.0.2497.48',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.51-1) Vivaldi/5.0.2497.51,',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.39',
        'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.92 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.34'
    ])
    def fetch_index(self, url):
        ua = choice(self.useragent)
        proxy = choice(self.proxies)

        proxies = {
            "all://": f"http://{proxy}",
        }

        headers = {
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers'
        }
        with Client(proxies=proxies) as session:
            response = session.get(url, headers=headers)
        return response.text

    def parse_index(self, html):
        tree = HTMLParser(html)
        items = tree.css('ul.one_column_bullet > li')
        agencies_urls = []
        for item in items:
            agencies_url = f"{self.baseurl}{item.css_first('a').attributes['href']}"
            agencies_urls.append(agencies_url)
        return agencies_urls

    def fetch_agency(self, urls):
        htmls = []
        for url in urls:
            ua = choice(self.useragent)
            proxy = choice(self.proxies)

            proxies = {
                "all://": f"http://{proxy}",
            }
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.usa.gov/federal-agencies/b',
                'Connection': 'keep-alive',
                # Cookie: _ga_GXFTMLX26S=GS1.1.1679083037.1.1.1679086257.0.0.0; _ga=GA1.2.1085666698.1679083038; nmstat=5185af43-46f9-9c41-9d6f-73c9619aabdb; _gid=GA1.2.151269674.1679083039; _ce.s=v~79e7e90d8778204e9ae0ca6db593fe88024474ce~vpv~0; cebs=1; _ce.clock_event=1; _ce.clock_data=37%2C120.188.93.224%2C1; cebsp_=14; QSI_HistorySession=https%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fu-s-department-of-housing-and-urban-development~1679083040543%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies~1679083128985%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fu-s-abilityone-commission~1679083137992%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fb%23current-letter~1679084203700%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies~1679084761356%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fb%23current-letter~1679085092963%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fu-s-abilityone-commission~1679086213267%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fbankruptcy-courts~1679086248258%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fb%23current-letter~1679086254110%7Chttps%3A%2F%2Fwww.usa.gov%2Ffederal-agencies%2Fbarry-m-goldwater-scholarship-and-excellence-in-education-program~1679086259316; QSI_SI_1XHUnb52JkGZWm1_intercept=true; _gat_gtag_UA_28227333_1=1; _gat_GSA_ENOR0=1; _gat_GSA_ENOR1=1; _gat_GSA_ENOR2=1; _gat_UA-33523145-1=1
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                # If-Modified-Since: Fri, 17 Mar 2023 20:45:36 GMT
                # If-None-Match: W/"bb0b2062245ccbf1a877e9a9faf1d4a5"
                'TE': 'trailers'
            }
            with Client(proxies=proxies) as session:
                response = session.get(url, headers=headers)
            htmls.append(response.text)
        return htmls

    def parse_agency(self, htmls):
        for html in htmls:
            tree = HTMLParser(html)


if __name__ == '__main__':
    baseurl = url = 'https://www.usa.gov/federal-agencies/b'
    scraper = Usagov()
    html = scraper.fetch_index(url)
    urls = scraper.parse_index(html)
    htmls = scraper.fetch_agency(urls)
    print(len(htmls))