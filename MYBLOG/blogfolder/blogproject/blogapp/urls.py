from django.urls import path
from . import views
# from .views import show_home
from .views import (
    BlogListView, 
    BlogDetailView, 
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogProfileView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('home/',show_home, name= 'blog-home')
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('', BlogListView.as_view(), name = 'blog-home'),
    path('blog/<int:pk>', BlogDetailView.as_view(), name = 'blog-detail'),
    path('blog/<int:pk>/profile', BlogProfileView.as_view(), name = 'blog-profile'),
    path('blog/new/', BlogCreateView.as_view(), name = 'blog-create'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name = 'blog-update'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name = 'blog-delete'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)