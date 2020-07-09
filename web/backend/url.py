from django.urls import path
from . import views

urlpatterns = [
    path('api/add_book', views.add_book),
    path('api/show_book', views.show_book),
    path('api/show_books', views.show_books),
    path('api/post', views.post),
    path('api/show_post', views.show_post),
    path('api/del_book', views.del_book),
    path('api/user_login', views.user_login),
    path('api/register', views.register),
    path('api/upload_image', views.upload_image),
    path('api/show_pic', views.show_pic),
    path('api/del_post', views.del_post),
    path('api/reply', views.reply),
    path('api/del_reply', views.del_reply),
    path('api/download', views.download),
    path('api/upload_text', views.upload_text),
    path('api/logout', views.logout),
    path('api/download_images', views.download_images)
]
