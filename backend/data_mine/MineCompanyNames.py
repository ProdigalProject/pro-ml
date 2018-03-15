from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib3
import json
import requests


class MineCompanyNames:

    def __init__(self):
        self.http = urllib3.PoolManager()
        self.base = 'http://stocks.tradingcharts.com/stocks/symbols/b/all/'
        self.website = 'http://stocks.tradingcharts.com'
        self.api = 'http://prodigal-ml.us-east-2.elasticbeanstalk.com/\
                   companies/'
        self.links = [self.base+x for x in ascii_lowercase]
        self.soups = []

    def find_company_names(self, soup):
        companies = []
        all_tr = soup.find_all('tr', bgcolor=True)
        for tr in all_tr:
            company_names = tr.find_all('td', rowspan=True, valign=True)
            exchange_tag = tr.find('td', align='middle')
            if len(company_names) != 0 and exchange_tag is not None:
                json_dict = {}
                json_dict['company_name'] = company_names[0].text.strip()
                json_dict['ticker'] = company_names[1].text.strip()
                json_dict['exchange'] = exchange_tag.text.strip()
                if json_dict['exchange'] == 'Nasdaq Stock Exchange':
                    companies.append(json_dict)
        return companies

    def post_to_api(self, companies):
        for company in companies:
            requests.post(self.api, data=company)

    def find_urls(self, soup):
        urls = set()
        a_tags = soup.find_all('a', href=True)
        for a in a_tags:
            if a['href'].startswith('/stocks/symbols/b/all'):
                urls.add(self.website + a['href'])
        return list(urls)

    def get_soup(self, url):
        response = self.http.request('GET', url)
        soup = BeautifulSoup(response.data, 'lxml')
        return soup

    def run(self):
        total_links = []
        for link in self.links:
            soup = self.get_soup(link)
            urls = self.find_urls(soup)  # list of urls
            total_links = total_links + urls
        total_links += self.links
        print("[x] LINKS COLLECTION COMPLETE.")

        for link in total_links:
            my_soup = self.get_soup(link)
            companies = self.find_company_names(my_soup)
            self.post_to_api(companies)
            print(companies)
        print("[x] POSTING TO API COMPLETE.")


def main():
    mcn = MineCompanyNames()
    mcn.run()

if __name__ == "__main__":
    main()
