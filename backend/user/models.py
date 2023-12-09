from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Username'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Name'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Last Name'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'), name='unique_username&email'
            ),
        )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Following'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            ),
        )
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
