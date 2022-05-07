from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from markdown2 import markdown
from random import choice
from .forms import *
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, entry_title):
    if entry_title == 'random':
        return random_page(request)

    requested_entry_content = util.get_entry(entry_title)
    if requested_entry_content is None:
        return render(request, 'encyclopedia/404.html')

    request.session['entry_title'] = entry_title
    request.session['entry_content'] = requested_entry_content
    entry_content = {"entry": markdown(requested_entry_content), "entry_name": entry_title}
    return render(request, 'encyclopedia/entry.html', context=entry_content)


def random_page(request):
    random_entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki:title', args=[random_entry]))


def search(request):
    titles = util.list_entries()
    search_result = request.GET.get('q')

    if search_result != '' and search_result in titles:
        return title(request, entry_title=search_result)

    elif search_result != '':
        all_matched_entries = []
        for entry_name in titles:
            if search_result.lower() in entry_name.lower():
                all_matched_entries.append(entry_name)
        return render(request, 'encyclopedia/search.html', context={"matched": all_matched_entries})

    else:
        return HttpResponseRedirect(reverse('wiki:index'))


def new_page(request):
    new_page_form = NewPage(request.POST or None)
    if new_page_form.is_valid():
        entry_title = new_page_form.cleaned_data.get('title_name')
        entry_content = new_page_form.cleaned_data.get('content')
        if util.get_entry(entry_title) is None:
            util.save_entry(entry_title, entry_content)
            return HttpResponseRedirect(reverse('wiki:title', args=[entry_title]))
        else:
            raise forms.ValidationError("This entry is already exists")
    return render(request, 'encyclopedia/new-page.html', context={"new_page": new_page_form})


def edit_page(request):
    initial_data = {
        'title_name': request.session.get('entry_title'),
        'content': request.session.get('entry_content'),
    }
    edit_form = EditPage(request.POST or None, initial=initial_data)
    if edit_form.is_valid():
        same_entry_title = edit_form.cleaned_data.get('title_name')
        entry_content = edit_form.cleaned_data.get('content')
        if same_entry_title == request.session['entry_title']:
            util.save_entry(request.session['entry_title'], entry_content)
            return HttpResponseRedirect(reverse('wiki:title', args=[request.session['entry_title']]))
        else:
            raise forms.ValidationError("Title should be the same")
    return render(request, 'encyclopedia/edit-page.html', context={"edit_page": edit_form,
                                                                   "entry_title": request.session['entry_title']})
