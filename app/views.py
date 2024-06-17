"""
Definition of views.
"""

from datetime import datetime
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from app.models import BlogEntry, Trip, TripComment, NewsFeedEntry, TripPhoto, UserSubscription, Sponsor
from app.forms import BlogEntryCreateForm, BlogEntryUpdateForm, ToggleBlogForm, TripCreateForm, NewsFeedEntryCreateForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import pycountry
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import random
from django.contrib.auth.models import User


class TripListView(ListView):
    model = Trip
    template_name = 'app/index.html'
    context_object_name = 'trips'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        folder_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'Images')

        try:
            all_files = os.listdir(folder_path)
        except Exception as e:
            all_files = []

        if len(all_files) >= 20:
            random_files = random.sample(all_files, 20) 
        else:
            random_files = all_files  

        # Add other context variables
        context['title'] = 'CC Travels!'
        context['news'] = NewsFeedEntry.objects.filter(active=True).order_by('-id')[:5]
        context['year'] = datetime.now().year
        context['random_files'] = random_files  

        return context

class TripCommentCreateView(CreateView, LoginRequiredMixin):
    model = TripComment
    fields = ['comment']
    template_name = 'app/comment_create.html'
    
    def form_valid(self, form):
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        form.instance.trip = trip
        form.instance.author = self.request.user
        self.success_url = reverse('blogList', kwargs={'pk': trip.pk})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Comment'
        context['year'] = datetime.now().year
        context['trip'] = Trip.objects.get(pk=self.kwargs['pk'])
        context['blogs'] = BlogEntry.objects.filter(trip=self.kwargs['pk'])
        context['comments'] = TripComment.objects.filter(trip=self.kwargs['pk'])
        context['trip_images'] = TripPhoto.objects.filter(trip=self.kwargs['pk'])
        return context

class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripCreateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        image_file = self.request.FILES.get('image')
        if image_file:
            fs = FileSystemStorage(location='app/static/app/Images/')
            filename = fs.save(image_file.name, image_file)
            form.instance.imageLink = filename
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Trip'
        context['year'] = datetime.now().year
        context['initialize_datepicker'] = True  
        context['image_upload'] = True
        return context

class TripUpdateView(UpdateView, LoginRequiredMixin):
    model = Trip
    form_class = TripCreateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        image_file = self.request.FILES.get('image')
        if image_file:
            fs = FileSystemStorage(location='app/static/app/Images/')
            filename = fs.save(image_file.name, image_file)
            form.instance.imageLink = filename
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Trip'
        context['year'] = datetime.now().year
        context['initialize_datepicker'] = True
        context['image_upload'] = True
        return context

class BlogCreateView(CreateView, LoginRequiredMixin):
    model = BlogEntry
    form_class = BlogEntryCreateForm
    template_name = 'app/generic_form.html'
    
    def get_success_url(self):
        trip_id = self.object.trip.id
        return reverse('blogList', kwargs={'pk': trip_id})

    def form_valid(self, form):
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        image_file = self.request.FILES.get('image')
        form.instance.trip = trip
        if image_file:
            fs = FileSystemStorage(location='app/static/app/Images/')
            filename = fs.save(image_file.name, image_file)
            form.instance.imageLink = filename
            trip_image = TripPhoto.objects.create(trip=trip, imageLink=filename)
            trip_image.save()

        new_news = NewsFeedEntry.objects.create(
            title=form.cleaned_data['title'], 
            body="NEW BLOG ENTRY!", active=True
            )
        new_news.save()
        # Call the parent class's form_valid method
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Blog Entry'
        context['year'] = datetime.now().year
        context['trip'] = Trip.objects.get(pk=self.kwargs['pk'])  
        context['image_upload'] = True
        return context

class BlogUpdateView(UpdateView, LoginRequiredMixin):
    model = BlogEntry
    form_class = BlogEntryUpdateForm
    template_name = 'app/generic_form.html'
    def get_success_url(self):
        trip_id = self.object.trip.id
        return reverse('blogList', kwargs={'pk': trip_id})


    def form_valid(self, form):
        image_file = self.request.FILES.get('image')
        if image_file:
            fs = FileSystemStorage(location='app/static/app/Images/')
            filename = fs.save(image_file.name, image_file)
            form.instance.imageLink = filename
            trip_image = TripPhoto.objects.create(trip=form.instance.trip, imageLink=filename)
            trip_image.save()
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Blog Entry'
        context['year'] = datetime.now().year
        context['image_upload'] = True
        return context

class BlogActiveToggleView(UpdateView, LoginRequiredMixin):
    model = BlogEntry
    form_class = ToggleBlogForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        blog_id = form.cleaned_data['blog_id']
        self.object = self.model.objects.get(pk=blog_id)
        self.object.active = not self.object.active
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return HttpResponse("Invalid form data", status=400)

class NewsCreateView(CreateView, LoginRequiredMixin):
    model = NewsFeedEntry
    form_class = NewsFeedEntryCreateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create News Entry'
        context['year'] = datetime.now().year
        return context

class UserSignUpCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'app/signup.html'
    success_url = '/login/'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        response = super().form_valid(form)

        if form.cleaned_data['subscribe_updates']:
            UserSubscription.objects.create(user=form.instance, subscribed=True)
        else:
            UserSubscription.objects.create(user=form.instance, subscribed=False)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        context['year'] = datetime.now().year
        return context
    
@login_required
def trip_image_create_view(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(pk=pk)

        image_file = request.FILES.get('image')

        if image_file:
            fs = FileSystemStorage(location='app/static/app/Images/')
            filename = fs.save(image_file.name, image_file)
            TripPhoto.objects.create(trip=trip, imageLink=filename)

        return redirect('blogList', pk=pk)

    trip = Trip.objects.get(pk=pk)
    context = {
        'title': 'Add Image to Trip ' + trip.title,
        'year': datetime.now().year,
        'image_upload': True
    }
    return render(request, 'app/generic_form.html', context)
    
# Sponsor List View - LIVE CODING!!!! 
