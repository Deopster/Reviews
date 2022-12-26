from generate import programm
import os
programm(
lang = 'ru',
country = 'us',
rev_number = None,
freeze_colums = 2,
freeze_rows = 1,
autofilter = False,
score=None,
sort = 'NEWEST',
columns=['Отзыв','кол. совпадений','Теги совпадений', 'Оценка','колнки тегов']

)
programm.create() #создание папки
