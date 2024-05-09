"""
Definition of urls for TravelBlog.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('blogCreate/', views.blogCreate, name='blogCreate'),
    path('blogUpdate/<int:blog_id>/', views.blogUpdate, name='blogUpdate'),
    path('blogActiveToggle/', views.blogActiveToggle, name='blogActiveToggle'),
]
