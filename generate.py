import pandas as pd
from google_play_scraper import app, reviews ,Sort,reviews_all
import glob
import pandas
import os
import string
class programm:
    def __init__(self,*args):
        self.lang = args[0]
        self.country = args[1]
        self.rev_number = args[2]
        self.freeze_colums =args[3]
        self.freeze_rows = args[4]
        self.autofilter =args[5]
        self.score = args[6]
        sort = Sort.NEWEST
        filter_score_with = None
        if self.rev_number is None:
            result = reviews_all(
                'com.bssys.roscapretail',
                sleep_milliseconds=0,  # defaults to 0
                lang=self.lang,  # defaults to 'en'
                country=self.country,  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
                filter_score_with=self.score  # defaults to None(means all score)
            )
        else:
            result, continuation_token = reviews(
                'com.bssys.roscapretail',
                lang=self.lang,  # defaults to 'en'
                country=self.country,  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.NEWEST
                count=self.rev_number,  # defaults to 100
                filter_score_with=self.score  # defaults to None(means all score)
            )
        return result
    def calc(self):
        return True
    def create(self):
        if not os.path.isdir("./output"):
            os.mkdir("output")
    def open(self):
        file = glob.glob('*.xlsx')
        try:
            self.tag_data = pandas.read_excel(file[0])
        except IndexError:
            print("Закиньте в корневую папку с main.py файл с тегами")
            raise
        except Exception:
            print("Неизвестная ошибка")
            raise
        finally:
            print(f"открыт файл {file[0]} в качесте файла тегирования")

