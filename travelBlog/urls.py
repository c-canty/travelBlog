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
    path('', views.TripListView.as_view(), name='home'),
    path('blogCreate/<int:pk>/', views.BlogCreateView.as_view(), name='blogCreate'),
    path('blogUpdate/<int:pk>/', views.BlogUpdateView.as_view(), name='blogUpdate'),
    path('blogActiveToggle/<int:pk>/', views.BlogActiveToggleView.as_view(), name='blogActiveToggle'),
    path('blogList/<int:pk>/', views.TripCommentCreateView.as_view(), name='blogList'),
    path('tripCreate/', views.TripCreateView.as_view(), name='tripCreate'),
    path('tripUpdate/<int:pk>/', views.TripUpdateView.as_view(), name='tripUpdate'),
    path('newsCreate/', views.NewsCreateView.as_view(), name='newsCreate'),
    path('signup/', views.UserSignUpCreateView.as_view(), name='signup'),
    path('tripImageCreate/<int:pk>/', views.trip_image_create_view, name='tripImageCreate'),
    
]
