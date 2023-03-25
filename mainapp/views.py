from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, DetailView, CreateView

from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Lesson, Course, CoursesTeacher, CourseFeedback


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


class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News
    # Просмотр удаленных новостей


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    # Редирект
    success_url = reverse_lazy('mainapp:news')
    # Проверка пользователя на добавление новостей
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    # Редирект
    success_url = reverse_lazy('mainapp:news')
    # Проверка пользователя на редактирование новостей
    permission_required = ('mainapp.change_news',)


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


class CourseDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CoursesTeacher.objects.filter(course=context_data['course_object'])
        context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])
        # Форма обратной связи, если пользователь авторизован
        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(course=context_data['course_object'], user=self.request.user)

        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})
