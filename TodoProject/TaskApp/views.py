from django.http import HttpResponseRedirect
from django.shortcuts import render

def home_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Home',
        'user': request.user,
    }
    return render(request, 'home.html', context=context)

def contacts_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Contacts',
    }
    return render(request, 'contacts.html', context=context)

def info_view(request):
    context = {
        'title': 'Info',
    }
    return render(request, 'info.html', context=context)
