from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus


# Тестирование на работу статичных страниц
from authapp.models import User
from mainapp.models import News


class StaticPagesSmokeTest(TestCase):

    def test_page_index_open(self):
        url = reverse('mainapp:index')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        url = reverse('mainapp:contacts')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)


# Тестирование новостей
class NewsTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        for i in range(10):
            News.objects.create(
                title=f'Тестовая новость{i}',
                preview=f'Вступление для тестовой новости{i}',
                body=f'Текст тестовой новости{i}'
            )
        # Создаем суперюзера
        User.objects.create_superuser(username='berber', password='220883')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'berber', 'password': '220883'}
        )

    # Тест на открытие страницы
    def test_open_page(self):
        url = reverse('mainapp:news')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    # Тест на провальное открытие неавторизованным пользователем страницы редактирования
    def test_failed_open_add_by_anonym(self):
        url = reverse('mainapp:news_create')

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    # Тест на создание новости админом
    def test_create_news_item_by_admin(self):

        news_count = News.objects.all().count()

        url = reverse('mainapp:news_create')
        result = self.client_with_auth.post(
            url,
            data={
                'title': 'Test news',
                'preview': 'Test preview',
                'body': 'Test body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.CREATED)

        self.assertEqual(News.objects.all().count(), news_count + 1)