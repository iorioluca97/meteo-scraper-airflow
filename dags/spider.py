import requests
from cfg import base_url, routes, sub_routes, BASE_DATA_PATH, REGIONS_DATA_PATH, NEWS_DATA_PATH
from typing import List, Dict
from bs4 import BeautifulSoup
import pandas as pd
from logger import logger
import os
from database import Database

db = Database()

class MeteoSpider():
    def __init__(
        self,
        ):
        self.base_url = base_url
        self._setup_dirs()

    def _setup_dirs(self,):
        if os.path.exists(BASE_DATA_PATH):
            return
        else:
            logger.info('Creating data directories..')
            if not os.path.exists(BASE_DATA_PATH):
                os.makedirs(BASE_DATA_PATH)
            if not os.path.exists(REGIONS_DATA_PATH):
                os.makedirs(REGIONS_DATA_PATH)
            if not os.path.exists(NEWS_DATA_PATH):
                os.makedirs(NEWS_DATA_PATH)

    def _compose_urls(self, route_to_parse: str) -> List[str]:
        urls = []
        if route_to_parse in routes and route_to_parse in sub_routes.keys():
            for sub_route in sub_routes[route_to_parse]:
                url = f'{self.base_url}/{route_to_parse}/{sub_route}'
                urls.append(url)

        return urls

    def _get_htmls(self, route_to_parse: str) -> List[str]:
        urls = self._compose_urls(route_to_parse)
        htmls = []
        for url in urls:
            response = requests.get(url)
            htmls.append(response.text)
        return htmls
    
    def parse_regions(self,):
        logger.info('Parsing regions..')
        htmls = self._get_htmls(route_to_parse='meteo')
        
        data_regions = []
        for html in htmls:
            scraped_region = self._scrape_meteo_region(html)
            data_regions.append(scraped_region)
        
        return self._create_regions_dataframe(data_regions)
    
    def parse_news(self,):
        logger.info('Parsing news..')
        html = self._get_htmls(route_to_parse='notizie')[0]

        data_news : List = self._scrape_news(html)

        return self._create_news_dataframe(data_news)


    def _scrape_news(self, html_content: str) -> List[Dict[str, str]]:
        data_news = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Trova tutti gli articoli di notizie
        articles = soup.select('section > article')  # Selettore CSS generico per articoli
        for article in articles:
            ul = article.find_all('ul')
            for u in ul:
                li = u.find_all('li')
                for l in li:
                    a = l.find('a')
                    img = l.find('img')
                    if a:
                        data_news.append({
                            'title': a['title'] if a['title'] else None,
                            'href': str(base_url + a['href']) if a['href'] else None,
                            'src': img['src'] if img else None
                        })
        return data_news


    
    def _scrape_meteo_region(self, html_content: str) -> Dict[str, List]:
        soup = BeautifulSoup(html_content, 'html.parser')
        region_meta_tag = soup.find('meta', property="og:url")
        
        forecast_date_title = soup.select('section > header > h2').pop(0)
        
        forecast_date_title = forecast_date_title.text if forecast_date_title else ''
        
        container_city_region = soup.find_all('span', class_='containerCityRegion')
        
        info_cities_list : Dict = {
            'title': forecast_date_title,
            'region': region_meta_tag['content'].split('/')[-1] if region_meta_tag else '',
            'cities': []
        }
        for city in container_city_region:
            city_name = city.find('span', class_ = 'cityOfRegion').text
            city_min_temperature = city.find('span', class_='temperature').text
            city_max_temperature = city.find('span', class_='temperature lastTemperature').text

            # find an href href="/meteo/"
            hrefs = soup.find_all('a', href=True)
            for href in hrefs:
                if f'/meteo/{city_name.lower().strip()}' in href['href']:
                    # in href find <p>
                    p = href.find('p')
            info_cities_list['cities'].append({
                'city_name': city_name,
                'city_min_temperature': city_min_temperature,
                'city_max_temperature': city_max_temperature,
                'description': p.text if p else ''
                })
    
        return info_cities_list
    

    def _create_regions_dataframe(self, data_regions: List) -> pd.DataFrame:
        full_data = pd.DataFrame()
        for region in data_regions:

            df = pd.DataFrame(region['cities'])
            df.to_csv(f'./data/regions/{region["region"]}.csv', index=False)
            full_data = pd.concat([full_data, df])

        # Create a dt_insert column based on the current date
        full_data['dt_insert'] = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')

        full_data.to_csv('./data/regions/all_regions.csv', index=False)
        return full_data


    def _create_news_dataframe(self, data_news: List) -> pd.DataFrame:
        full_data = pd.DataFrame(data_news)

        # Create a dt_insert column based on the current date
        full_data['dt_insert'] = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
        full_data.to_csv('./data/news/all_news.csv', index=False)
        return full_data

    def run(self,):
        all_regions = self.parse_regions()
        
        all_news = self.parse_news()

        return all_regions, all_news
