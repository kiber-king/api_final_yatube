from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Модель для групп."""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для постов."""
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Текст нового поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    group = models.ForeignKey(Group,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Группа',
                              help_text='Группа, которой принадлежит пост')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True)

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[0:15]


class Comment(models.Model):
    """Модель для комментариев."""
    post = models.ForeignKey(Post,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='Пост')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, db_index=True,
                                   verbose_name='Создан')

    class Meta:
        default_related_name = 'comments'
        ordering = ['-created']
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:20]


class Follow(models.Model):
    """Модель для подписчиков и подписок."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='follower',
                             verbose_name='Пользователь'
                             )
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=True,
                                  related_name='following',
                                  verbose_name='Автор'
                                  )

    class Meta:
        unique_together = [['user', 'following']]

    def __str__(self):
        return '{} follows {}'.format(self.user, self.following)
