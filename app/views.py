"""
Definition of views.
"""

from datetime import datetime
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from app.models import BlogEntry, Trip, TripComment, NewsFeedEntry, TripPhoto
from app.forms import BlogEntryCreateForm, BlogEntryUpdateForm, ToggleBlogForm, TripCreateForm, NewsFeedEntryCreateForm
from django.contrib.auth.decorators import login_required
import pycountry
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse


class TripListView(ListView):
    model = Trip
    template_name = 'app/index.html'
    context_object_name = 'trips'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CC Travels!'
        context['news'] = NewsFeedEntry.objects.filter(active=True)[:5]
        context['year'] = datetime.now().year
        return context
    

class TripCommentCreateView(CreateView, LoginRequiredMixin):
    model = TripComment
    fields = ['comment']
    template_name = 'app/comment_create.html'
    
    def form_valid(self, form):
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        form.instance.trip = trip
        form.instance.author = self.request.user
        # Redirect back to the same trip detail page
        self.success_url = reverse('blogList', kwargs={'pk': trip.pk})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Comment'
        context['year'] = datetime.now().year
        context['news'] = NewsFeedEntry.objects.filter(active=True)
        context['trip'] = Trip.objects.get(pk=self.kwargs['pk'])
        context['blogs'] = BlogEntry.objects.filter(trip=self.kwargs['pk'])
        context['comments'] = TripComment.objects.filter(trip=self.kwargs['pk'])
        return context

class TripCreateView(CreateView, LoginRequiredMixin):
    model = Trip
    form_class = TripCreateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Trip'
        context['year'] = datetime.now().year
        context['initialize_datepicker'] = True  # Unique context variable
        return context

class TripUpdateView(UpdateView, LoginRequiredMixin):
    model = Trip
    form_class = TripCreateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Trip'
        context['year'] = datetime.now().year
        context['initialize_datepicker'] = True  # Unique context variable
        return context


class BlogCreateView(CreateView, LoginRequiredMixin):
    model = BlogEntry
    form_class = BlogEntryCreateForm
    template_name = 'app/generic_form.html'
    
    # Define a success_url that redirects to a relevant page (could be the trip detail page, or a blog list page)
    def get_success_url(self):
        # Redirect back to the detail page of the trip with the given pk
        return reverse('blogList', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        # Retrieve the trip based on the URL parameter
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        # Associate the BlogEntry with the specific trip
        form.instance.trip = trip
        
        # Create a newsfeed entry as before
        new_news = NewsFeedEntry.objects.create(title=form.cleaned_data['title'], body="NEW BLOG ENTRY!", active=True)
        


        # Call the parent class's form_valid method
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Blog Entry'
        context['year'] = datetime.now().year
        context['trip'] = Trip.objects.get(pk=self.kwargs['pk'])  # Pass the trip to the context
        return context

class BlogUpdateView(UpdateView, LoginRequiredMixin):
    model = BlogEntry
    form_class = BlogEntryUpdateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Blog Entry'
        context['year'] = datetime.now().year
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
