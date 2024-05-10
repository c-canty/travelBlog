"""
Definition of views.
"""

from datetime import datetime
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from app.models import BlogEntry, Trip, TripComment, NewsFeedEntry, TripPhoto
from app.forms import BlogEntryCreateForm, BlogEntryUpdateForm, ToggleBlogForm, TripCreateForm
from django.contrib.auth.decorators import login_required
import pycountry
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class HomeListView(ListView):
    model = BlogEntry
    template_name = 'app/index.html'
    context_object_name = 'blog_entries'
    ordering = ['created']

    def get_queryset(self):
        queryset = super().get_queryset()  # Start with base queryset
        country_filter = self.request.GET.get('country')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if country_filter:
            queryset = queryset.filter(country__iexact=country_filter)

        # Parse start and end dates and filter the queryset
        if start_date or end_date:
            start = parse_date(start_date)
            end = parse_date(end_date)
            
            # If parsing dates was successful, apply date filters
            if start and end:
                queryset = queryset.filter(
                    created__date__gte=start,
                    created__date__lte=end
                )
            elif start:
                queryset = queryset.filter(created__date__gte=start)
            elif end:
                queryset = queryset.filter(created__date__lte=end)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        context['year'] = datetime.now().year
        context['countries'] = sorted(pycountry.countries, key=lambda c: c.name)

        return context

class BlogCreateView(CreateView, LoginRequiredMixin):
    model = BlogEntry
    form_class = BlogEntryCreateForm
    template_name = 'app/generic_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Blog Entry'
        context['year'] = datetime.now().year
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

