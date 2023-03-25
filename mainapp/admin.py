from django.contrib import admin
from mainapp.models import News, Course, Lesson, CoursesTeacher

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CoursesTeacher)


# Более информативный вывод новостей в админке
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # Отображение
    list_display = ('pk', 'title', 'deleted',)
    # Сортировка
    ordering = ('pk',)
    # Пагинация
    list_per_page = 2
    # Фильтрация
    list_filter = ('deleted', 'created_at',)
    # Поиск по тексту
    search_fields = ('title', 'body',)
    # Дополнительные опции (кастомизация)
    actions = ('mark_as_delete',)

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'


