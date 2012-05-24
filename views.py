# Create your views here.
import sys, traceback
import codecs
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper
from django import forms

class UserCreationForm(forms.Form):
    sm_user = forms.CharField(label='User', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    pwd = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=100)
    check_pwd = forms.CharField(widget=forms.PasswordInput, label='Check Password', max_length=100)

class LoginForm(forms.Form):
    sm_user = forms.CharField(label='User', max_length=100)
    pwd = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=100)

# Deprecated
def index(request):
    c = {}
    c.update(csrf(request))
    t = 'index.tml'
    try:
        c['sm_user'] = request.session['sm_user']
    except:
        pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def main_page(request):
    c = {}
    if request.is_ajax():
        t = 'main_page.html'
    else:
        t = 'index.html'
        c['content'] = 'main_page.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def smart_teacher_user_creation(request):
    c = {}
    c.update(csrf(request))
    t = 'user_creation.html'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['pwd'] == form.cleaned_data['check_pwd']:
                try:
                    user = User.objects.create_user(form.cleaned_data['sm_user'], form.cleaned_data['email'], form.cleaned_data['pwd'])
                    user.save()
                    return HttpResponseRedirect('/')
                except:
                    c['error'] = 'Server error'
            else:
                c['error'] = "Password don't match"
        else:
            c['error'] = 'Form error'
    form = UserCreationForm()
    c['form'] = form
    return render_to_response(t, c)

def smart_teacher_login(request):
    c = {}
    c.update(csrf(request))
    try:
        c['sm_user'] = request.session['sm_user']
        t = 'home.html'
    except:
        form = LoginForm()
        c['form'] = form
        t = 'login.html'
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['sm_user'], password=form.cleaned_data['pwd'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.session['sm_user'] = user.username
                        c['sm_user'] = user.username
                        return HttpResponseRedirect('/')
                    else:
                        c['error'] = "User isn't active"
                else:
                    c['error'] = "User or Password wrong"
            else:
                c['error'] = "Form invalid"
    return render_to_response(t, c)

def smart_teacher_logout(request):
    try:
        del request.session['sm_user']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def events(request):
    c = {}
    if request.is_ajax():
        t = 'events.html'
    else:
        t = 'index.html'
        c['content'] = 'events.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def donate(request):
    c = {}
    if request.is_ajax():
        t = 'donate.html'
    else:
        t = 'index.html'
        c['content'] = 'donate.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def help(request):
    c = {}
    if request.is_ajax():
        t = 'help.html'
    else:
        t = 'index.html'
        c['content'] = 'help.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def about(request):
    c = {}
    if request.is_ajax():
        t = 'about.html'
    else:
        t = 'index.html'
        c['content'] = 'about.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def contact(request):
    c = {}
    if request.is_ajax():
        t = 'contact.html'
    else:
        t = 'index.html'
        c['content'] = 'contact.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def trial(request):
    c = {}
    if request.is_ajax():
        t = 'trial.html'
    else:
        t = 'index.html'
        c['content'] = 'trial.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def trial_pdf(request):
    import os
    import subprocess
    import random
    
    #SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    #filename = SITE_ROOT + '/tmp/' + str(request.session['user']) + str(sheet_id)
    filename = str(random.randrange(1, 10000, 1))
    tex = codecs.open('tmp/' + filename + '.tex', mode='w', encoding='utf-8')
    tex.write("\\documentclass[a4paper, ")
    tex.write("]{exam}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{amsfonts}\\begin{document}\n\\begin{questions}\n")
    if request.GET.get('q1', False):
        tex.write("\question ")
        tex.write(request.GET.get('q1'))
    if request.GET.get('q2', False):
        tex.write("\question ")
        tex.write(request.GET.get('q2'))
    if request.GET.get('q3', False):
        tex.write("\question ")
        tex.write(request.GET.get('q3'))
    if request.GET.get('q4', False):
        tex.write("\question ")
        tex.write(request.GET.get('q4'))
    if request.GET.get('q5', False):
        tex.write("\question ")
        tex.write(request.GET.get('q5'))
    if request.GET.get('q6', False):
        tex.write("\question ")
        tex.write(request.GET.get('q6'))
    tex.write("\\end{questions}\\end{document}")
    tex.close()
    
    #subprocess.call(['pdflatex', '-interaction=nonstopmode', '-output-directory=' + SITE_ROOT + 'tmp', SITE_ROOT + 'tmp/' + filename + '.tex'])
    subprocess.call(['pdflatex', '-interaction=nonstopmode', '-output-directory=tmp', 'tmp/' + filename + '.tex'])
    
    pdf = open('tmp/' + filename + '.pdf', 'r')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + filename + '.pdf'
    return response
