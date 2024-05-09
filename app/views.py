"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from app.models import BlogEntry
from app.forms import BlogEntryCreateForm, BlogEntryUpdateForm, ToggleBlogForm
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
            'blog_entries': BlogEntry.objects.all().order_by('created'),
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
        'app/generic_form.html',
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
        return redirect('home')
    return render(
        request,
        'app/generic_form.html',
        {
            'title':'Update Blog Entry',
            'year':datetime.now().year,
            'form': form,
        }
    )

@login_required
def blogActiveToggle(request):
    if request.method == 'POST':
        form = ToggleBlogForm(request.POST)
        if form.is_valid():
            blog_id = form.cleaned_data['blog_id']
            blog = get_object_or_404(BlogEntry, id=blog_id)
            blog.active = not blog.active
            blog.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            # What causes the form to be invalid?
            return HttpResponse("Invalid form data", status=400)
    else:
        return HttpResponse("Only POST method is allowed", status=405)

