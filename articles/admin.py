from django.contrib import admin

from articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'is_publication')
    list_filter = ('title',)
    search_fields = ('title', 'description',)
