"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.models import BlogEntry
from app.forms import BlogEntryCreateForm, BlogEntryDeactivateForm, BlogEntryUpdateForm
from django.contrib.auth.decorators import login_required


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'blog_entries': BlogEntry.objects.filter(active=True).order_by('created')[:5],
        }
    )

@login_required
def blogCreate(request):
    """Renders the blog create page."""
    assert isinstance(request, HttpRequest)
    form = BlogEntryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(
        request,
        'app/blogCreate.html',
        {
            'title':'Create Blog Entry',
            'year':datetime.now().year,
            'form': form,
        }
    )

@login_required
def blogUpdate(request, blog_id):
    """Renders the blog update page."""
    assert isinstance(request, HttpRequest)
    blog = BlogEntry.objects.get(id=blog_id)
    form = BlogEntryUpdateForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
    return render(
        request,
        'app/blogUpdate.html',
        {
            'title':'Update Blog Entry',
            'year':datetime.now().year,
            'form': form,
        }
    )

@login_required
def blogDeactivate(request, blog_id):
    """Renders the blog deactivate page."""
    assert isinstance(request, HttpRequest)
    blog = BlogEntry.objects.get(id=blog_id)
    form = BlogEntryDeactvateForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
    return render(
        request,
        'app/blogDeactivate.html',
        {
            'title':'Deactivate Blog Entry',
            'year':datetime.now().year,
            'form': form,
        }
    )
    
    
