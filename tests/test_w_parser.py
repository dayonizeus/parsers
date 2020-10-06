"""
Запуск теста с отчетом
pytest --cov=w_parser --cov-report=html
"""

from w_parser.w_parser import *

test_object_hh = HhParser()
test_object_work_ua = WorkUaParser()
test_object_rabota_ua = RabotaUaParser()
test_object_superjob = SuperjobParser()


class TestParser():

    def test_checklist(self, test_object=test_object_hh):
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

    def test_set_ads(self, test_object=test_object_hh):
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

    def test_set_hh_url(self, test_object=test_object_hh):
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

    def test_get_hh_details(self, test_object=test_object_hh):
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
        # В результирующем списке должно быть 48 записей. Правильность данного
        # утверждения можно проверить вручную - файл 'test_files_hh.html'
        assert len(test_object._ads_list) == 48
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
            'Менеджер по продажам',
            'ООО ФИНЭКСПРЕСС',
            'https://hh.ru/vacancy/36649951',
            '110000-350000 руб.'
        )
        assert test_object._ads_list[0] == expected_tuple
        '''Если з/п не указана, то четвертое значение кортежа
        должно быть "не указана"'''
        assert test_object._ads_list[13][3] == 'не указана'

    def test_hh_pagination(self, test_object=test_object_hh):
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
        expected_link = ('https://hh.ru/search/vacancy?clusters=true&enable_' +
                         'snippets=true&search_field=name&search_period=1&te' +
                         'xt=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%8' +
                         '0&page=1')
        # Тестируемый метод должен изенять свойство _url на ожидаемое (срез
        # сделан так как в реальной ситуации ссылка на сайте обрезана -
        # нет первой части url`а ('https://hh.ru')
        assert test_object._url == expected_link
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup('<div></div>', 'lxml')
        # Выполнение тестируемого метода
        test_object._pagination()
        # При отсутствии на странице ссылки на следующую метод должен изменить
        # значение свойства _url на False
        assert test_object._url is False

    def test_get_hh_data(self, test_object=test_object_hh):
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


class TestWorkUaParser():

    def test_set_work_ua_url(self, test_object=test_object_work_ua):
        # Тестовое значение для корректной ссылки
        correct_url = (
            'https://www.work.ua/ru/jobs-legal/?advs=1&employment=76')
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

    def test_get_work_ua_details(self, test_object=test_object_work_ua):
        # Открытие тестового html-файла
        with open('tests/test_files/work_ua.html', encoding='utf-8') as f:
            test_page_work_ua = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_work_ua, 'lxml')
        # Присвоение тестового значения свойству _ads_list тестового объекта
        test_object._ads_list = []
        # Выполнение тестируемого метода
        test_object._get_details()
        # Тестируемый метод должен изменять свойство _ads_list тестируемого
        # объекта
        assert test_object._ads_list != []
        # В результирующем списке должно быть 13 записей. Правильность данного
        # утверждения можно проверить вручную - файл 'test_page_hh.html'
        assert len(test_object._ads_list) == 13
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
            'Специалист по работе с задолженностью',
            'Hired!',
            'https://www.work.ua/ru/jobs/3919529/',
            '30 000 грн · ставка + бонусы'
        )
        assert test_object._ads_list[2] == expected_tuple
        '''Если з/п не указана, то четвертое значение кортежа
        должно быть "не указана"'''
        assert test_object._ads_list[3][3] == 'не указана'

    def test_work_ua_pagination(self, test_object=test_object_work_ua):
        # Открытие тестового html-файла
        with open('tests/test_files/work_ua.html', encoding='utf-8') as f:
            test_page_work_ua = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_work_ua, 'lxml')
        # Установка стартового значения свойства _url
        test_object._url = 'https://www.work.ua/ru/jobs-legal'
        # Выполнение тестируемого метода
        test_object._pagination()
        # Ожидаемое значение свойства _url
        expected_link = ('https://www.work.ua/ru/jobs-legal/?advs=1' +
                         '&employment=76&_pjax=%23pjax&page=2')
        # Тестируемый метод должен изенять свойство _url на ожидаемое
        assert test_object._url == expected_link
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup('<div></div>', 'lxml')
        # Выполнение тестируемого метода
        test_object._pagination()
        # При отсутствии на странице ссылки на следующую метод должен изменить
        # значение свойства _url на False
        assert test_object._url is False

    def test_get_work_ua_data(self):
        # Тестирование в реальных условиях
        link = ('https://www.work.ua/ru/jobs-legal/?advs=1&employment=76')
        # Получение списка кортежей с вакансиями
        test_object = WorkUaParser()
        test_object.set_url(link)
        result_list = test_object.get_data()
        # Если парсер отработал - то длинна списка должна быть более 0
        assert len(result_list) > 0


class TestRabotaUaParser():

    def test_set_rabota_ua_url(self, test_object=test_object_rabota_ua):
        # Тестовое значение для корректной ссылки
        correct_url = ('https://rabota.ua/zapros/%d0%b2%d0%be%d0%b4%d0%b8%d1' +
                       '%82%d0%b5%d0%bb%d1%8c/%d1%83%d0%ba%d1%80%d0%b0%d0%b8' +
                       '%d0%bd%d0%b0')
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

    def test_get_rabota_ua_details(self, test_object=test_object_rabota_ua):
        # Открытие тестового html-файла
        with open('tests/test_files/rabota_ua.html', encoding='utf-8') as f:
            test_page_rabota_ua = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_rabota_ua, 'lxml')
        # Присвоение тестового значения свойству _ads_list тестового объекта
        test_object._ads_list = []
        # Выполнение тестируемого метода
        test_object._get_details()
        # Тестируемый метод должен изменять свойство _ads_list тестируемого
        # объекта
        assert test_object._ads_list != []
        # В результирующем списке должно быть 20 записей. Правильность данного
        # утверждения можно проверить вручную - файл 'test_page_hh.html'
        assert len(test_object._ads_list) == 20
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
            'Водитель на наше авто (Uber, Uklon, Bolt, Позняки)',
            'ЛКТ',
            'https://rabota.ua/company6182579/vacancy7858961',
            '18000 грн'
        )
        assert test_object._ads_list[0] == expected_tuple
        '''Если з/п не указана, то четвертое значение кортежа
        должно быть "не указана"'''
        assert test_object._ads_list[1][3] == 'не указана'

    def test_rabota_ua_pagination(self, test_object=test_object_rabota_ua):
        # Открытие тестового html-файла
        with open('tests/test_files/rabota_ua.html', encoding='utf-8') as f:
            test_page_rabota_ua = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_rabota_ua, 'lxml')
        # Установка стартового значения свойства _url
        test_object._url = 'https://rabota.ua/'
        # Выполнение тестируемого метода
        test_object._pagination()
        # Ожидаемое значение свойства _url
        expected_link = ('https://rabota.ua/zapros/%d0%b2%d0%be%d0%b4%d0%b8%' +
                         'd1%82%d0%b5%d0%bb%d1%8c/%d1%83%d0%ba%d1%80%d0%b0%d' +
                         '0%b8%d0%bd%d0%b0/pg2')
        # Тестируемый метод должен изенять свойство _url на ожидаемое
        assert test_object._url == expected_link
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup('<div></div>', 'lxml')
        # Выполнение тестируемого метода
        test_object._pagination()
        # При отсутствии на странице ссылки на следующую метод должен изменить
        # значение свойства _url на False
        assert test_object._url is False

    def test_get_rabota_ua_data(self):
        # Тестирование в реальных условиях
        link = ('https://rabota.ua/zapros/%d1%80%d0%b0%d0%b7%d1%80%d0%b0%d0%' +
                'b1%d0%be%d1%82%d1%87%d0%b8%d0%ba/%d0%b7%d0%b0%d0%bf%d0%be%d' +
                '1%80%d0%be%d0%b6%d1%8c%d0%b5')
        # Получение списка кортежей с вакансиями
        result_list = RabotaUaParser().set_url(link).get_data()
        # Если парсер отработал - то длинна списка должна быть более 0
        assert len(result_list) > 0


class TestSuperjobParser():

    def test_set_superjob_url(self, test_object=test_object_superjob):
        # Тестовое значение для корректной ссылки
        correct_url = (
            'https://ufa.superjob.ru/vacancy/search/?remote_work_binary=2')
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

    def test_get_superjob_details(self, test_object=test_object_superjob):
        # Открытие тестового html-файла
        with open('tests/test_files/superjob.html', encoding='utf-8') as f:
            test_page_superjob = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_superjob, 'lxml')
        # Присвоение тестового значения свойству _ads_list тестового объекта
        test_object._ads_list = []
        # Выполнение тестируемого метода
        test_object._get_details()
        # Тестируемый метод должен изменять свойство _ads_list тестируемого
        # объекта
        assert test_object._ads_list != []
        # В результирующем списке должно быть 20 записей. Правильность данного
        # утверждения можно проверить вручную - файл 'test_page_hh.html'
        assert len(test_object._ads_list) == 20
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
            'Менеджер по продажам банковских продуктов',
            'КИВИ Банк',
            'https://www.superjob.ru/vakansii/menedzher-po-prodazham-' +
            'bankovskih-produktov-30577005.html',
            'от 50 000 руб./месяц'
        )
        assert test_object._ads_list[0] == expected_tuple

    def test_superjob_pagination(self, test_object=test_object_superjob):
        # Открытие тестового html-файла
        with open('tests/test_files/superjob.html', encoding='utf-8') as f:
            test_page_superjob = f.read()
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup(test_page_superjob, 'lxml')
        # Установка стартового значения свойства _url
        test_object._url = 'https://ufa.superjob.ru/vacancy/search'
        # Выполнение тестируемого метода
        test_object._pagination()
        # Ожидаемое значение свойства _url
        expected_link = ('https://www.superjob.ru/vacancy/search/?remote_wor' +
                         'k_binary=2&page=2')
        # Тестируемый метод должен изенять свойство _url на ожидаемое
        assert test_object._url == expected_link
        # Присвоение тестового значения свойству _soup тестового объекта
        test_object._soup = BeautifulSoup('<div></div>', 'lxml')
        # Выполнение тестируемого метода
        test_object._pagination()
        # При отсутствии на странице ссылки на следующую метод должен изменить
        # значение свойства _url на False
        assert test_object._url is False

    def test_get_work_ua_data(self):
        # Тестирование в реальных условиях
        link = ('https://ufa.superjob.ru/vacancy/search/?remote_work_binary=2')
        # Получение списка кортежей с вакансиями
        result_list = SuperjobParser().set_url(link).get_data()
        # Если парсер отработал - то длинна списка должна быть более 0
        assert len(result_list) > 0
