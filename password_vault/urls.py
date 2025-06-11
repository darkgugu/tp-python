from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'password_vault'

urlpatterns = [
    path('', views.password_list, name='password_list'),
    path('<int:pk>/', views.password_detail, name='password_detail'),
    path('add/', views.password_add, name='password_add'),
    path('<int:pk>/delete/', views.password_delete, name='password_delete'),
    path('<int:pk>/generate_share_link/', views.generate_share_link, name='generate_share_link'),
    path('share/<uuid:token>/', views.view_shared_password, name='view_shared_password'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('generate_password/', views.generate_password, name='generate_password'),
]

