# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import SmartQAndS
from sheet.models import Sheet
from qands.models import QAndS
from django import forms

class SmartQAndSForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False, label='ID')
    des = forms.CharField(widget=forms.Textarea(), label='Description')
    arg = forms.CharField(widget=forms.Textarea(), label='Parameters')
    question = forms.CharField(widget=forms.Textarea(), label='Question')
    solution = forms.CharField(widget=forms.Textarea(), label='Solution')
    ref = forms.CharField(widget=forms.TextInput(), required=False, label='Reference')
    key = forms.CharField(widget=forms.TextInput(), required=False, label='Keyword')

class KeywordForm(forms.Form):
    key = forms.CharField(label='Keyword')
    up = forms.CharField(required=False, label='More general keyword')

def list_smartqands(request, id_sheet=None):
    """
    Return a list of smartqands.
    """
    c = {}
    c['id_sheet'] = id_sheet
    l = SmartQAndS.objects.all()
    c['smartqandss'] = l
    return render_to_response('list_smartqands.html', c)

def list_keyword(request):
    """
    Return a list of keyword.
    """
    return NotImplementedError

def show_smartqands(request, id_smartqands=None, id_sheet=None):
    """
    Return a working smartqands.
    """
    c = {}
    if id_smartqands:
        c['smartqands'] = SmartQAndS.objects.get(id = id_smartqands)
    if id_sheet:
        c['id_sheet'] = id_sheet
        print 'render add_to=' + str(id_sheet)
    return render_to_response('show_smartqands.html', c)

def edit_smartqands(request, id_smartqands=None):
    """
    If id_smartqands != None it edit the smartqands otherwise it create a new one.
    """
    c = {}
    t = 'edit_smartqands.html'
    if id_smartqands:
        if request.method == "GET":
            form = SmartQAndSForm(request.GET)
            if form.is_valid():
                old = SmartQAndS.objects.get(id=id_smartqands)
                old.des = form.cleaned_data['des']
                old.arg = form.cleaned_data['arg']
                old.question = form.cleaned_data['question']
                old.solution = form.cleaned_data['solution']
                old.save()
                return HttpResponseRedirect('..')
            else:
                c['edit'] = True
                old = SmartQAndS.objects.get(id=id_smartqands)
                init = {}
                init['des'] = old.des
                init['arg'] = old.arg
                init['question'] = old.question
                init['solution'] = old.solution
                form = SmartQAndSForm(initial=init)
                c['form'] = form
                c['id'] = id_smartqands
    else:
        if request.method == "GET":
            print 'try create'
            form = SmartQAndSForm(request.GET)
            if form.is_valid():
                print 'valid'
                new = SmartQAndS(des=form.cleaned_data['des'], arg=form.cleaned_data['arg'], question=form.cleaned_data['question'], solution=form.cleaned_data['solution'])
                new.save()
                return HttpResponseRedirect(str(new.id))
            else:
                form = SmartQAndSForm()
                c['form'] = form
    return render_to_response(t, c)

def form_keyword(request, id_keyword):
    """
    Return a form for create a new keyword or edit one.
    """
    return NotImplementedError

def apply_smartqands(request, id_smartqands=None):
    """
    Try to save in the database a smartqands and return a result message.
    """
    c = {}
    if request.method == 'GET':
        form = SmartQAndSForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['id'] in ('', None):
                try:
                    s_new = SmartQAndS(arg = form.cleaned_data['arg'], question = form.cleaned_data['question'], solution = form.cleaned_data['solution'])
                    s_new.save()
                except:
                    c['error'] = True
            else:
                try:
                    s_new = SmartQAndS.objects.get(id = form.cleaned_data['id'])
                    s_new.arg = form.cleaned_data['arg']
                    s_new.question = form.cleaned_data['question']
                    s_new.solution = form.cleaned_data['solution']
                    s_new.save()
                except:
                    c['error'] = True
    return HttpResponseRedirect('../')

def apply_keyword(request, id_keyword):
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

def smartqands_to_qands(request, id_sheet=None, id_smartqands=None):
    if id_sheet and id_smartqands:
        if request.method == "GET":
            if request.GET.get('q', None):
                this_sheet = Sheet.objects.get(id=id_sheet)
                this_smartqands = SmartQAndS.objects.get(id=id_smartqands)
                q = QAndS(sheet=this_sheet, smartqands=this_smartqands, question=request.GET.get('q'), solution=request.GET.get('s',''))
                q.save()
    return HttpResponseRedirect('../../../sheet/' + str(id_sheet))


