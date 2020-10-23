from django.db import models


STATUS_NEW = 'new'
STATUS_MODERATED = 'moderated'
STATUS_CHOICES = (
    (STATUS_NEW, 'Новая'),
    (STATUS_MODERATED, 'Модерированная')
)
DEFAULT_STATUS = STATUS_NEW


class Quote(models.Model):
    text = models.TextField(max_length=2000, verbose_name='Текст')
    author = models.CharField(max_length=100, verbose_name='Автор')
    email = models.EmailField(verbose_name='Email')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    status = models.CharField(max_length=15, verbose_name='Статус',
                              choices=STATUS_CHOICES, default=DEFAULT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.text[:20]}'

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        ordering = ('-created_at',)