UPLOAD_DIRECTORY = "/tretafdtvd"
import pandas
import os
import dash_bootstrap_components as dbc
def uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return  [dbc.ListGroupItem( obj, id="button-item", n_clicks=0, action=True, active=True) for obj in files]


def multitags(tag_data,result):
        table_colums = ['Отзыв', 'кол. совпадений', 'Теги совпадений', 'Оценка', *tag_data.columns,
                        'Дата создания отзыва']
        data = pandas.DataFrame(columns=table_colums)
        m = 0
        temp = {}
        temp_tags = []

        all_data = set()
        tag_data.fillna('', inplace=True)
        for i in tag_data.values.tolist():
            all_data.update(i)
        df = pandas.DataFrame(0, columns=list(all_data)[1::], index=tag_data.keys().tolist())

        for index, i in enumerate(result):
            temp['Дата создания отзыва'] = i['at']
            temp['Отзыв'] = i['content']
            temp['Оценка'] = i['score']
            for column_name in tag_data.columns:
                for column_data in tag_data[f'{column_name}']:
                    if column_data != '':
                        if temp['Отзыв'].lower().count(column_data) > 0:
                            m += 1
                            df.at[column_name, column_data] = 1 + df.at[column_name, column_data]
                            # print(column_data, column_name, temp['Отзыв'], "\n")
                            # temp_tags.append(column_data)
                            temp_tags = " ~ ".join([temp_tags, column_data])
                            print("да", column_name, column_data, temp['Отзыв'])
                            temp[f'{column_name}'] = 1
            temp['кол. совпадений'] = sum(list(temp.values())[2:])
            temp['Теги совпадений'] = str(temp_tags)
            for i in table_colums:
                if i not in temp.keys():
                    temp[f'{i}'] = 0
            # print(temp)
            data = pandas.concat([data, pandas.DataFrame([temp])], )
            # data = data.append(temp,ignore_index=True)
            temp_tags = ''
            temp.clear()
        #print(df)
        print('Найдено совпадений: ' + str(m))
        return data,m,df