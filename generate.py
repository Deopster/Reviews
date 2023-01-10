import pandas as pd
from google_play_scraper import app, reviews ,Sort,reviews_all
import glob
import pandas
import os
import string
class programm:
    def __init__(self,lang = 'ru',country = 'us',rev_number = None,freeze_colums = 2,freeze_rows = 1,autofilter = False,score=None,sort = 'NEWEST',columns=['Отзыв','кол. совпадений','Теги совпадений', 'Оценка','колонки тегов']):
        self.lang = lang
        self.country = country
        self.rev_number = rev_number
        self.freeze_colums =freeze_colums
        self.freeze_rows = freeze_rows
        self.autofilter =autofilter
        self.score = score
        sort = Sort.NEWEST
    def get_parse_data(self):
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
    def create(self):
        if not os.path.isdir("./output"):
            os.mkdir("output")
            return "создан путь output"
    def open(self):
        file = glob.glob('./input/*.xlsx')
        try:
            tag_data = pandas.read_excel(file[0])
        except IndexError:
            print("Закиньте в папку input файл с тегами")
            raise
        except Exception:
            print("Неизвестная ошибка")
            raise
        finally:
            print(f"открыт файл {file[0]} в качесте файла тегирования")
        return tag_data
    def parse(self,result,tag_data):
        self.table_colums = ['Отзыв', 'кол. совпадений', 'Теги совпадений', 'Оценка', *tag_data.columns,
                        'Дата создания отзыва']
        data = pandas.DataFrame(columns=self.table_colums)
        m = 0
        temp = {}
        temp_tags = []
        for index, i in enumerate(result):
            temp['Дата создания отзыва'] = i['at']
            temp['Отзыв'] = i['content']
            temp['Оценка'] = i['score']
            for column_name in tag_data.columns:
                for column_data in tag_data[f'{column_name}']:
                    if pandas.notnull(column_data):
                        if temp['Отзыв'].find(column_data) > 0:
                            m += 1
                            #print(column_data, column_name, temp['Отзыв'], "\n")
                            temp_tags.append(column_data)
                            # print("да",column_name,temp['Отзыв'])
                            temp[f'{column_name}'] = 1

            temp['кол. совпадений'] = sum(list(temp.values())[2:])
            temp['Теги совпадений'] = str(temp_tags)
            for i in self.table_colums:
                if i not in temp.keys():
                    temp[f'{i}'] = 0
            # print(temp)
            data = pandas.concat([data, pd.DataFrame([temp])], )
            # data = data.append(temp,ignore_index=True)
            temp_tags.clear()
            temp.clear()
        print('Найдено совпадений: ' + str(m))
        data.to_csv("./output/res.csv", index = None,header=True)
        return data
    def generate_exel(self,data):
        writer = pd.ExcelWriter('./output/results.xlsx')
        data.to_excel(writer, sheet_name='table', index=False, na_rep=0)
        worksheet = writer.sheets['table']
        format1 = writer.book.add_format({'bg_color': '#e0f2cb', 'border': 1})
        format2 = writer.book.add_format({'bg_color': 'ffa799', 'border': 1})
        format3 = format4 = writer.book.add_format({'bg_color': 'ffdca3', 'border': 1})
        for column in data:
            column_width = max(data[column].astype(str).map(len).max(), len(column)) + 5
            if column_width > 70:
                column_width = 70
            col_idx = data.columns.get_loc(column)
            worksheet.set_column(col_idx, col_idx, column_width)
        # worksheet.autofilter(f'B1:{string.ascii_uppercase[len(data.keys())-1]+"1"}')
        worksheet.freeze_panes(1, 2)
        crits = ['>4', '<3', '=3', '=4']
        formats = [format1, format2, format3, format4]
        for index, i in enumerate(data['Оценка'],
                                  start=2):  # по сути рудимент - потом заменить на цикл по колличеству строк
            # print(f"A{str(index)}:{string.ascii_uppercase[len(data.keys())]+str(index)}")
            # worksheet.write_row(f"A{str(index)}:{string.ascii_uppercase[len(data.keys())]+str(index)}", 'Ray', format4)
            for i in range(4):
                worksheet.conditional_format(
                    f"A{str(index)}:{string.ascii_uppercase[len(data.keys()) - 1] + str(index)}", {'type': 'formula',
                                                                                                   'criteria': f'=${string.ascii_uppercase[self.table_colums.index("Оценка")]}${index}{crits[i]}',
                                                                                                   'format': formats[
                                                                                                       i]})
        writer.save()

