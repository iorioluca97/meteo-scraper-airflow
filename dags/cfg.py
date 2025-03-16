from typing import List, Dict


BASE_DATA_PATH = './data'
REGIONS_DATA_PATH = f'{BASE_DATA_PATH}/regions'
NEWS_DATA_PATH = f'{BASE_DATA_PATH}/news'

base_url = 'https://www.meteo.it'

routes : List = [
    "meteo",
    "notizie"
]


sub_routes : Dict = {
    "meteo" : [
            'piemonte',
            'veneto',
            'emilia-romagna',
            'friuli-venezia-giulia',
            'liguria',
            'trentino-alto-adige',
            'valle-d-aosta',
            'lazio',
            'toscana',
            'umbria',
            'marche',
            'abruzzo',
            'campania',
            'puglia',
            'calabria',
            'basilicata',
            'molise',
            'sicilia',
            'sardegna',
            ],
    "notizie" : [
        ""
    ]
        }
