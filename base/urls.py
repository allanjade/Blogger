from . import views

from django.urls import path, re_path, include


from django.conf import settings

from django.conf.urls.static  import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('admin', views.admin, name='admin'),
    path('visitor', views.visitor, name='visitor'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('postnew', views.postnew, name='postnew'),
    path('one_post/<int:id>', views.one_post, name='one_post'),
    path('post_update/<int:id>', views.post_update, name='post_update'),
    path('post_delete/<int:id>', views.post_delete, name='post_delete'),
    path('about', views.about, name='about')  ,
    
    path('profile/', views.profile, name='profile'),
    path('updadateprofile/<int:id>/update/', views.updateprofile, name='updateprofile'),
    path('deleteprofile/<int:id>/delete/', views.deleteprofile, name='deleteprofile'),
]

 



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)