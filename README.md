W_PARSER
========
Данная библиотека предоставляет классы для парсинга русскоязычных сайтов с объявлениями о работе

## На данный момент для парсинга доступны следующие ресурсы:

- hh.ru - класс HhParser()
- work.ua - класс WorkUaParser()

## Установка

pip install w-parser

## Использование

*импорт*
**from w_parser import w_parser**
*инициализация объекта*
**hh = w_parser.HhParser()**
*установка ссылки для парсинга*
**url** = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&no_magic=true&search_period=1&text=%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82+%D0%BF%D0%BE+%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E&L_save_area=true&area=2&from=cluster_area&showClusters=true'
**hh.set_url(url)**
*получение списка с искомыми значениями*
**hh_list = hh.get_data()**
