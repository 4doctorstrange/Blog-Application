
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('register', views.register, name='register'),
    path('post/<int:id>',views.post, name='post'),
    path('login', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.user_logout, name='logout'),
    path('addpost', views.add_post, name="add_post"),
    path('updatepost/<int:id>', views.update_post, name="update_post"),
    path('deletepost/<int:id>', views.delete_post, name="delete_post"),
    path('profile/<str:username>', views.view_profile, name="view_profile")
   
    
]
