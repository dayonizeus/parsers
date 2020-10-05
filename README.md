W_PARSER
========
Данная библиотека предоставляет классы для парсинга русскоязычных сайтов с объявлениями о работе

## На данный момент для парсинга доступны следующие ресурсы:

- hh.ru - класс HhParser()
- work.ua - класс WorkUaParser()

## Установка

pip install w-parser

## Предоставляемые классы имеют следующие публичные методы:
**set_url(url_string)** - передает в текущий объект стартовую страницу для парсинга данных. Последующая пагинация осуществляется автоматически.<br>
**set_ads(list_of_tuples)** - передает в текущий объект результат парсинга предыдущих сайтов.<br>
**get_data()** - возвращает результирующий список, который будет состоять из кортежей имеющих следующий вид:<br>
('Заголовок объявления','Наименование работодателя, 'Ссылка на страницу объявления', 'Размер з/п')
Метод осуществляет фильтрацию данных по следующим полям: 'Заголовок объявления' и 'Наименование работодателя'. Таким образом, объявления от одного и того же работодателя с одинаковыми заголовками в результирующий список попадают только один раз.

## Пример использования:

*импорт*<br>
**from w_parser import w_parser**<br>
*инициализация объекта*<br>
**hh = w_parser.HhParser()**<br>
*образец ссылки*
**url** = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&no_magic=true&search_period=1&text=%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82+%D0%BF%D0%BE+%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E&L_save_area=true&area=2&from=cluster_area&showClusters=true'<br>
*установка ссылки для парсинга*<br>
**hh.set_url(url)**<br>
*получение списка с искомыми значениями*<br>
**hh_list = hh.get_data()**<br>

## Обратная связь
Ваши пожелания и предложения можете направлять по адресу dayonizeus@gmail.com
