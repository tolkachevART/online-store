from django.contrib import admin
from django.urls import path, include

from articles.apps import ArticlesConfig
from articles.views import ArticleCreateView, ArticleUpdateView, ArticleListView, ArticleDetailView, ArticleDeleteView, \
    article_is_publication

app_name = ArticlesConfig.name

urlpatterns = [
    path("create/", ArticleCreateView.as_view(), name="create"),
    path("", ArticleListView.as_view(), name="list"),
    path("view/<int:pk>/", ArticleDetailView.as_view(), name="view"),
    path("edit/<int:pk>/", ArticleUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", ArticleDeleteView.as_view(), name="delete"),
    path("activity/<int:pk>/", article_is_publication, name="article_is_publication"),
]