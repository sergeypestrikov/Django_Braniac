from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    deleted = models.BooleanField(default=False, verbose_name='удалено')

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class NewsManager(models.Manager):

    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    objects = NewsManager()

    title = models.CharField(max_length=64, verbose_name='новостной заголовок')
    preview = models.CharField(max_length=1000, verbose_name='вступление')
    body = models.TextField(verbose_name='сама новость')
    body_as_markdown = models.BooleanField(default=False, verbose_name='способ разметки')

    def __str__(self):
        return f'#{self.pk} {self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Course(BaseModel):
    name = models.CharField(max_length=256, verbose_name="название курса")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="способ разметки", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="стоимость", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="картинка")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="номер лекции")
    title = models.CharField(max_length=256, verbose_name="название лекции")
    description = models.TextField(verbose_name="описание лекции", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="способ разметки", default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ("course", "num")


class CoursesTeacher(BaseModel):
    course = models.ManyToManyField(Course)
    name = models.CharField(max_length=128, verbose_name="имя")
    surname = models.CharField(max_length=128, verbose_name="фамилия")
    day_birth = models.DateField(verbose_name="дата рождения")

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name, self.surname)