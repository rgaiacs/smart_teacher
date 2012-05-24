# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from models import *
from django import forms

class SmartQAndSForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False, label='ID')
    description = forms.CharField(widget=forms.Textarea(), label='Description')
    # redirect = forms.CharField(required=False, label='Redirect')
    # arg = forms.CharField(widget=forms.Textarea(), label='Parameters')
    # question = forms.CharField(widget=forms.Textarea(), label='Question')
    # solution = forms.CharField(widget=forms.Textarea(), label='Solution')
    interact = forms.CharField(widget=forms.Textarea(), label='Interact')
    cat = forms.CharField(widget=forms.TextInput(), required=False, label='Reference')
    key = forms.CharField(widget=forms.TextInput(), required=False, label='Keyword')

class KeywordForm(forms.Form):
    key = forms.CharField(label='Keyword')

class CommentForm(forms.Form):
    # id = forms.IntegerField(required=False, label='ID')
    comment = forms.CharField(widget=forms.Textarea(), label='Comment')

def list_smartqands(request):
    """
    Return a list of smartqands.
    """
    c = {}
    l = SmartQAndS.objects.all()
    c['list_smartqands'] = l
    if request.is_ajax():
        t = 'list_smartqands.html'
    else:
        t = 'index.html'
        c['content'] = 'list_smartqands.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def list_keyword(request):
    """
    Return a list of keyword.
    """
    return NotImplementedError

def show_smartqands(request, smartqands_id=None, smartqands_description=None):
    """
    Return a working smartqands.
    """
    c = {}
    if smartqands_id:
        this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
        c['smartqands'] = this_smartqands
    elif smartqands_description:
        this_smartqands = SmartQAndS.objects.get(description=smartqands_description)
        c['smartqands'] = this_smartqands
    this_smartqands.counter += 1
    this_smartqands.save()
    #this_revision = Revision.objects.filter(smartqands=this_smartqands).latest('id')
    c['script'] = this_smartqands.lastest.script
    if request.is_ajax():
        t = 'show_smartqands.html'
    else:
        t = 'index.html'
        c['content'] = 'show_smartqands.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def edit_smartqands(request, smartqands_id=None, smartqands_description=None, show=0):
    """
    If smartqands_id != None it edit the smartqands otherwise it create a new one.
    """
    c = {}
    show = int(show)
    c['show'] = show
    t = 'edit_smartqands.html'
    if smartqands_id or smartqands_description:
        if smartqands_id:
            this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
        elif smartqands_description:
            this_smartqands = SmartQAndS.objects.get(description=smartqands_description)
        c['id'] = this_smartqands.id
        if request.method == "GET":
            if request.GET:
                form = SmartQAndSForm(request.GET)
                if form.is_valid():
                    this_user = User.objects.get(username=request.user.username)
                    # this_script = Script(arg=form.cleaned_data['arg'], question=form.cleaned_data['question'], solution=form.cleaned_data['solution'])
                    this_script = Script(interact=form.cleaned_data['interact'])
                    this_script.save()
                    this_revision = Revision(script=this_script, smartqands=this_smartqands, user=this_user)
                    this_revision.save()
                    this_smartqands.lastest = this_revision
                    this_smartqands.description = form.cleaned_data['description']
                    this_smartqands.save()
                    if show:
                        return HttpResponseRedirect('../{0}/'.format(this_smartqands.id))
                    else:
                        return HttpResponseRedirect('..')
            else:
                init = {}
                init['id'] = this_smartqands.id
                init['description'] = this_smartqands.description
                # init['arg'] = this_smartqands.lastest.script.arg
                # init['question'] = this_smartqands.lastest.script.question
                # init['solution'] = this_smartqands.lastest.script.solution
                c['interact'] = this_smartqands.lastest.script.interact
                print this_smartqands.lastest.id
                #print init['interact']
                form = SmartQAndSForm(initial=init)
                c['form'] = form
    else:
        if request.method == "GET":
            if request.GET:
                form = SmartQAndSForm(request.GET)
                print form.is_valid()
                if form.is_valid():
                    this_smartqands = SmartQAndS(description=form.cleaned_data['description'], counter=0, is_redirect=False)
                    this_smartqands.save()
                    this_user = User.objects.get(username=request.user.username)
                    # this_script = Script(arg=form.cleaned_data['arg'], question=form.cleaned_data['question'], solution=form.cleaned_data['solution'])
                    this_script = Script(interact=form.cleaned_data['interact'])
                    this_script.save()
                    this_revision = Revision(script=this_script, smartqands=this_smartqands, user=this_user)
                    this_revision.save()
                    this_smartqands.lastest = this_revision
                    this_smartqands.save()
                    return HttpResponseRedirect('/smartqands/{0}'.format(this_smartqands.id))
            else:
                form = SmartQAndSForm()
                c['form'] = form
    return render_to_response(t, c)

def history(request, smartqands_id=None, smartqands_description=None):
    c = {}
    t = 'history.html'
    if smartqands_id or smartqands_description:
        if smartqands_id:
            this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
        elif smartqands_description:
            this_smartqands = SmartQAndS.objects.get(description=smartqands_description)
        c['id'] = this_smartqands.id
        c['revisions'] = Revision.objects.filter(smartqands=this_smartqands)
    return render_to_response(t, c)

def form_keyword(request, keyword_title):
    """
    Return a form for create a new keyword or edit one.
    """
    return NotImplementedError

def apply_keyword(request, keyword_title):
    """
    Try to save in the database a keyword and return a result message.
    """
    return NotImplementedError

def search_smartqands(request):
    """
    Return the result of a search for smartqands.
    """
    return NotImplementedError

def search_keyword(request):
    """
    Return the result of a search for keyword.
    """
    return NotImplementedError

def show_comment(request, smartqands_id=None, smartqands_description=None):
    t = 'show_comment.html'
    c = {}
    if smartqands_id:
        this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
    elif smartqands_description:
        this_smartqands = SmartQAndS.objects.get(description=smartqands_description)
    c['id'] = this_smartqands.id
    comment_list = Comment.objects.filter(smartqands=this_smartqands)
    c['comment_list'] = comment_list

    form = CommentForm()
    c['form'] = form
    return render_to_response(t, c)

def edit_comment(request, smartqands_id=None, smartqands_description=None):
    """
    If comment.
    """
    print smartqands_id
    if smartqands_id or smartqands_description:
        if smartqands_id:
            this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
        elif smartqands_description:
            this_smartqands = SmartQAndS.objects.get(description=smartqands_description)
        if request.method == "GET":
            form = CommentForm(request.GET)
            print form.is_valid()
            if form.is_valid():
                this_smartqnads = SmartQAndS.objects.get(id=smartqands_id)
                this_user = User.objects.get(username=request.user.username)
                this_comment = Comment(user=this_user, smartqands=this_smartqands, comment=form.cleaned_data['comment'])
                this_comment.save()
    return HttpResponseRedirect('../..')
