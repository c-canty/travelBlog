"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from app.models import BlogEntry
from app.forms import BlogEntryCreateForm, BlogEntryUpdateForm, ToggleBlogForm
from django.contrib.auth.decorators import login_required
import pycountry


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    # Get filters from query parameters
    country_filter = request.GET.get('country', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Start with all blog entries
    blog_entries = BlogEntry.objects.all()

    # Apply country filter if specified
    if country_filter:
        blog_entries = blog_entries.filter(country__iexact=country_filter)

    # Apply date filter if both dates are specified
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            blog_entries = blog_entries.filter(
                created__date__gte=start_date,
                created__date__lte=end_date
            )
        except ValueError:
            # Handle invalid date format
            pass
    countries = sorted(list(pycountry.countries), key=lambda c: c.name)

    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'blog_entries': blog_entries.order_by('created'),
            'countries': countries,
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

