import factory

from blogs.models import Blog


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog
