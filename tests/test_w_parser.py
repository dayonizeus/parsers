"""
Запуск теста с отчетом
pytest --cov=w_parser --cov-report=html
"""

from w_parser.w_parser import *

test_object = HhParser()


class TestParser():

    def test_checklist(self):
        # Установка тестового значения для свойства _ads_list
        test_object._ads_list = [
            ('работа', 'рога и копыта', 'link', '1$'),
            ('Ещё работа', 'рога и копыта', 'link', '1$'),
            ('и Ещё одна работА', 'копыта и рога', 'link', '1$')
        ]
        # Тестовое значение добавляемого кортежа
        tested_tuple = ('Какой-то текст', 'Буратино', 'link', '1$')
        # Ожидаемое значение свойства _ads_list
        test_expected = [
            ('работа', 'рога и копыта', 'link', '1$'),
            ('Ещё работа', 'рога и копыта', 'link', '1$'),
            ('и Ещё одна работА', 'копыта и рога', 'link', '1$'),
            ('Какой-то текст', 'Буратино', 'link', '1$')
        ]
        # Выполнение тестируемого метода
        test_object._checklist(tested_tuple)
        # _checklist() должен добавить уникальный кортеж в результирующий
        # список
        assert test_object._ads_list == test_expected
        # Выполнение тестируемого метода
        test_object._checklist(tested_tuple)
        # _checklist() должен отклонить запись не уникального кортежа
        assert test_object._ads_list == test_expected

    def test_set_ads(self):
        # Установка тестового значения для свойства _ads_list
        test_object._ads_list = []
        # Попробуем добавить объект не являющийся списком
        adding_object = 'Строка'
        # Выполнение тестируемого метода
        test_object.set_ads(adding_object)
        # Объект не являющийся списком не должен быть добавлен
        assert test_object._ads_list == []
        # Попробуем добавить пустой список, состоящий не из кортежей
        adding_object = [1, 2, 3, 5, 'string', [1, 2, 3]]
        # Выполнение тестируемого метода
        test_object.set_ads(adding_object)
        # Объект состоящий не из кортежей не должен быть дбавлен
        assert test_object._ads_list == []
        # Попробуем добавить валидный список
        adding_object = [
            ('работа', 'рога и копыта', 'link', '1$'),
            ('Ещё работа', 'рога и копыта', 'link', '1$'),
            ('и Ещё одна работА', 'копыта и рога', 'link', '1$')]
        # Выполнение тестируемого метода
        test_object.set_ads(adding_object)
        # Валидный объект должен быть добавлен
        assert test_object._ads_list == [
            ('работа', 'рога и копыта', 'link', '1$'),
            ('Ещё работа', 'рога и копыта', 'link', '1$'),
            ('и Ещё одна работА', 'копыта и рога', 'link', '1$')]


class TestHhParser():

    def test_set_hh_url(self):
        # Тестовое значение для корректной ссылки
        correct_url = ('https://hh.ru/search/vacancy?area=123&fromSearchLin' +
                       'e=true&st=searchVacancy&text=')
        # Тестовое значение для некорректной ссылки
        incorrect_url = 'https://rabota.ru'
        # Установка стартового значения свойста _url
        test_object._url = None
        # Выполнение тестируемого метода
        test_object.set_url(correct_url)
        # _set_url должен устанавливать корректное значение свойства _url
        assert test_object._url == correct_url
        # Установка стартового значения свойства _url
        test_object._url = None
        # Выполнение тестируемого метода
        test_object.set_url(incorrect_url)
        '''_set_url должен отвергать установку свойства _url при неверном
        формате ссылки'''
        assert test_object._url is None

    def test_get_hh_details(self):
        # Открытие тестового html-файла
        with open('tests/test_files/hh.html', encoding='utf-8') as f:
            test_page_hh = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_hh, 'lxml')
        # Присвоение тестового значения свойству _ads_list тестового объекта
        test_object._ads_list = []
        # Выполнение тестируемого метода
        test_object._get_details()
        # Тестируемый метод должен изменять свойство _ads_list тестируемого
        # объекта
        assert test_object._ads_list != []
        # В результирующем списке должно быть 28 записей. Правильность данного
        # утверждения можно проверить вручную - файл 'test_page_hh.html'
        assert len(test_object._ads_list) == 28
        # Результирующий список должен содержать кортежи
        for ad in test_object._ads_list:
            assert type(ad) is tuple
        '''Результирующие кортежи должны иметь следующий вид:
        ("Заголовок объявления",
        "Наименование работодателя",
        "ссылка на страницу объявления",
        "Размер з/п (если есть)")'''
        # Ожидаемый результат первого кортежа в списке
        expected_tuple = (
            'Web-программист (стажер)',
            'Dial',
            'https://hh.ru/vacancy/39460641',
            'от 20000 руб.'
        )
        assert test_object._ads_list[0] == expected_tuple
        '''Если з/п не указана, то четвертое значение кортежа
        должно быть "не указана"'''
        assert test_object._ads_list[1][3] == 'не указана'

    def test_hh_pagination(self):
        # Открытие тестового html-файла
        with open('tests/test_files/hh.html', encoding='utf-8') as f:
            test_page_hh = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_hh, 'lxml')
        # Установка стартового значения свойства _url
        test_object._url = 'https://hh.ru/search/'
        # Выполнение тестируемого метода
        test_object._pagination()
        # Ожидаемое значение свойства _url
        expected_link = ('https://hh.ru/search/vacancy?L_is_autosearch=fals' +
                         'e&clusters=true&enable_snippets=true&page=1')
        # Тестируемый метод должен изенять свойство _url на ожидаемое (срез
        # сделан так как в реальной ситуации ссылка на сайте обрезана -
        # нет первой части url`а ('https://hh.ru')
        assert test_object._url[13:] == expected_link
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup('<div></div>', 'lxml')
        # Выполнение тестируемого метода
        test_object._pagination()
        # При отсутствии на странице ссылки на следующую метод должен изменить
        # значение свойства _url на False
        assert test_object._url is False

    def test_get_hh_data(self):
        # Тестирование в реальных условиях
        link = ('https://hh.ru/search/vacancy?clusters=true&enable_snippet' +
                's=true&text=%D0%B4%D0%B2%D0%BE%D1%80%D0%BD%D0%B8%D0%BA&L_' +
                'save_area=true&area=1002&from=cluster_area&showClusters=true')
        # Получение списка кортежей с вакансиями
        test_object = HhParser()
        test_object.set_url(link)
        result_list = test_object.get_data()
        # Если парсер отработал - то длинна списка должна быть более 0
        assert len(result_list) > 0