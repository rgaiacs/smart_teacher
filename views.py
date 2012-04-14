# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(label='User', max_length=100)
    pwd = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=100)

def index(request):
    c = {}
    c.update(csrf(request))
    try:
        c['user'] = request.session['user']
        t = 'home.html'
    except:
        form = LoginForm()
        c['form'] = form
        t = 'index.html'
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['user'], password=form.cleaned_data['pwd'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.session['user'] = user.username
                        c['user'] = user.username
                        t = 'home.html'
                    else:
                        c['error'] = "User isn't active"
                else:
                    c['error'] = "User or Password wrong"
            else:
                c['error'] = "Form invalid"
    return render_to_response(t, c)

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponseRedirect('..')
