from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView
from blog.apps import BlogConfig
from django.views.decorators.cache import cache_page, never_cache

app_name = BlogConfig.name

urlpatterns = [
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path("", BlogListView.as_view(), name='blogs_list'),
    path("view_blog/<int:pk>/", cache_page(60)(BlogDetailView.as_view()), name='view_blog'),
    path("update_blog/<int:pk>/", BlogUpdateView.as_view(), name='update_blog'),
    path("delete_blog/<int:pk>/", BlogDeleteView.as_view(), name='delete_blog'),
]
