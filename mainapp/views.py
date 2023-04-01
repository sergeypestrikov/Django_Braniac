from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, DetailView, CreateView

import mainapp.tasks
from mainapp import tasks
from config import settings
from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Lesson, Course, CoursesTeacher, CourseFeedback


# Контроллер главной страницы
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


# Контроллер страницы контактов
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

    # Вызов отложенной задачи
    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_to_email.delay(message_body, message_from)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))

# Контроллер страницы курсов
class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course


# Контроллер страницы документации
class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


# Контроллер страницы страницы входа
class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


# Контроллер страницы новостей
class NewsListView(ListView):
    model = News
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


# Контроллер страницы подробного описания новости
class NewsDetailView(DetailView):
    model = News
    # Просмотр удаленных новостей


# Контроллер страницы создания новости
class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    # Редирект
    success_url = reverse_lazy('mainapp:news')
    # Проверка пользователя на добавление новостей
    permission_required = ('mainapp.add_news',)


# Контроллер страницы редактирования новости
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    # Редирект
    success_url = reverse_lazy('mainapp:news')
    # Проверка пользователя на редактирование новостей
    permission_required = ('mainapp.change_news',)


# Контроллер страницы удаления новости
class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    # Редирект
    success_url = reverse_lazy('mainapp:news')
    # Проверка пользователя на удаление новостей
    permission_required = ('mainapp.delete_news',)

# class NewsView(TemplateView):
#     template_name = 'mainapp/news_list.html'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['object_list'] = News.objects.all()
#         return context_data


# Контроллер страницы подробного описания курса
class CourseDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CoursesTeacher.objects.filter(course=context_data['course_object'])

        # Низкоуровневое кэширование отзывов на курсы
        feedback_list_key = f'course_feedback_{context_data["course_object"].pk}'
        cached_feedback_list = cache.get(feedback_list_key)
        if cached_feedback_list is None:
            context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])
            cache.set(feedback_list_key, context_data['feedback_list'], timeout=300)
        else:
            context_data['feedback_list'] = cached_feedback_list

        # Форма обратной связи, если пользователь авторизован
        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(course=context_data['course_object'], user=self.request.user)
        # Пагинация для отзывов
        # paginator = Paginator(context_data['feedback_list'], 2)
        # paginator.page(4)
        return context_data


# Контроллер страницы с обратной связью
class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


# Контроллер логгера
class LoggerView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    # Проверка на доступ к логам (только для админов)
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Список логов
        log_lines = []
        i = 0
        with open(settings.BASE_DIR / 'log/main_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                # Такая запись позволяет записывать свежие логи сверху
                log_lines.insert(0, line)
        context_data['logs'] = log_lines
        return context_data


# Скачивание логов
class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))