from django.contrib import admin
from .models import Author, Category, Post, PostCategory, CategorySubscriber, Comment

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(CategorySubscriber)
