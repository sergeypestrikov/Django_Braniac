from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'
    #Метод для получения контекста
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'some title'
        return context_data

# Через функцию и контекст
# def index(request):
#     context = {
#         'key': {'one': 1,
#                 'two': 2
#                 }
#     }
#     return render(request, 'mainapp/index.html', context)


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт-Петербург',
                'phone': '+7-911-777-14-62',
                'email': 'geeklab@spb.ru',
                'address': 'территория Петропавловская крепость, 3Ж',
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-911-777-14-63',
                'email': 'geeklab@kz.ru',
                'address': 'территория Кремль, 11',
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-911-777-14-64',
                'email': 'geeklab@msk.ru',
                'address': 'Красная площадь, 7',
            }
        ]

        return context_data


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = [
            {
                'title': 'IT растет',
                'preview': 'Спрос на специалистов увеличился',
                'date': datetime.now()
            }, {
                'title': 'Учиться никогда не поздно',
                'preview': 'Самое время сменить профессию',
                'date': datetime.now()
            }, {
                'title': 'Чего ждать на собеседовании',
                'preview': '30 каверзных вопросов для соискателя',
                'date': datetime.now()
            }, {
                'title': 'Люблю свою работу',
                'preview': 'Как полюбить то, что делаешь',
                'date': datetime.now()
            }, {
                'title': 'Год без софта',
                'preview': 'Кто нас покинул и что делать дальше',
                'date': datetime.now()
            }, {
                'title': 'Python или Java',
                'preview': 'Приоритетные языки программирования 2023 года',
                'date': datetime.now()
            }
        ]
        return context_data