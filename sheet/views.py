# Create your views here.
import sys, traceback
import codecs
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper
from django import forms
from django.contrib.auth.models import User
from sheet.models import Sheet, QAndS
from smartqands.models import SmartQAndS
from django.contrib.auth.models import User

class SheetForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title', help_text="A title for this sheet.")
    description = forms.CharField(widget=forms.Textarea(), required=False, label='Description', help_text="A description of this sheet.")
    is_public = forms.BooleanField(required=False, label='Is Public', help_text="")

def list_sheets(request, sheet_filter='pub'):
    c = {}
    if sheet_filter == 'pub':
        sheets = Sheet.objects.filter(is_public=True)
    elif sheet_filter == 'res':
        this_user = User.objects.get(username=request.user.username)
        sheets = Sheet.objects.filter(user=this_user)
    c['sheets'] = sheets
    if request.is_ajax():
        t = 'list.html'
    else:
        t = 'index.html'
        c['content'] = 'list.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def edit_sheet(request, sheet_id=None):
    """
    If sheet_id != None it edit the sheet otherwise it create a new one.
    """
    c = {}
    if sheet_id:
        if request.method == "GET":
            form = SheetForm(request.GET)
            if form.is_valid():
                this_sheet = Sheet.objects.get(id=sheet_id)
                this_sheet.title = form.cleaned_data['title']
                this_sheet.description = form.cleaned_data['description']
                this_sheet.s_public = form.cleaned_data['is_public']
                this_sheet.save()
                if int(request.GET.get('show', False)):
                    return HttpResponseRedirect('../{0}'.format(sheet_id))
                else:
                    return HttpResponseRedirect('../res')
            else:
                c['sheet_id'] = sheet_id
                this_sheet = Sheet.objects.get(id=sheet_id)
                init = {}
                init['title'] = this_sheet.title
                init['description'] = this_sheet.description
                init['is_public'] = this_sheet.is_public
                form = SheetForm(initial=init)
                c['form'] = form
                c['show'] = int(request.GET.get('show', False))
    else:
        if request.method == "GET":
            form = SheetForm(request.GET)
            if form.is_valid():
                this_sheet = Sheet(title=form.cleaned_data['title'], description=form.cleaned_data['description'], is_public=form.cleaned_data['is_public'])
                this_sheet.save()
                this_user = User.objects.get(username=request.user.username)
                this_sheet.user.add(this_user)
                this_sheet.save()
                return HttpResponseRedirect(str(this_sheet.id))
            else:
                form = SheetForm()
                c['form'] = form
                c['show'] = int(request.GET.get('show', False))
    if request.is_ajax():
        t = 'edit.html'
    else:
        t = 'home.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
        c['content'] = 'edit.html'
    return render_to_response(t, c)

def del_sheet(request, sheet_id):
    old_sheet = Sheet.objects.get(id=sheet_id)
    old_sheet.delete()
    return HttpResponseRedirect('../../res')

def show_sheet(request, sheet_id):
    c = {}
    this_sheet = Sheet.objects.get(id=sheet_id)
    c['sheet'] = this_sheet
    qands = QAndS.objects.filter(sheet=this_sheet)
    c['qands'] = qands
    c['qands_count'] = QAndS.objects.filter(sheet=this_sheet).count()
    if request.is_ajax():
        t = 'sheet.html'
    else:
        t = 'index.html'
        c['content'] = 'sheet.html'
        try:
            c['sm_user'] = request.session['sm_user']
        except:
            pass
    return render_to_response(t, c, context_instance=RequestContext(request))

def show_qands_from_sheet(request, sheet_id, id_qands):
    c = {}
    this_sheet = Sheet.objects.get(id=sheet_id)
    this_qands = QAndS.objects.get(id=id_qands)
    return HttpResponseRedirect('../../../smartqands/' + str(this_qands.smartqands.id))

def list_smartqands(request, sheet_id):
    """
    Return a list of smartqands.
    """
    c = {}
    l = SmartQAndS.objects.all()
    c['list_smartqands'] = l
    c['sheet_id'] = sheet_id
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

def smartqands_to_qands(request, sheet_id=None, smartqands_id=None):
    c = {}
    if sheet_id and smartqands_id:
        if request.method == "GET":
            if request.GET.get('q', False):
                this_sheet = Sheet.objects.get(id=sheet_id)
                this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
                this_qands=QAndS(sheet=this_sheet, smartqands=this_smartqands, question=request.GET.get('q',''),solution=request.GET.get('s', ''))
                this_qands.save()
                return HttpResponseRedirect('/sheet/{0}'.format(this_sheet.id))
            else:
                #this_sheet = Sheet.objects.get(id=sheet_id)
                #this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
                #this_qands = QAndS(sheet=this_sheet, smartqands=this_smartqands, question=request.GET.get('q', ''), solution=request.GET.get('s', ''))
                #this_qands.save()
                this_smartqands = SmartQAndS.objects.get(id=smartqands_id)
                c['smartqands'] = this_smartqands
                c['script'] = this_smartqands.lastest.script
                c['sheet_id'] = sheet_id
                return render_to_response('show_smartqands.html', c)

def add_qands_to_sheet(request, sheet_id=None, id_qands=None):
    c = {}
    try:
        this_sheet = Sheet(id=sheet_id)
        s_q = SmartQAndS.objects.get(id=id_qands_to_add)
        q = QAndS(sheet=this_sheet, smartqands=s_q, question=s_q.question, solution=s_q.solution)
        q.save()
    except:
        print 'error'
    return HttpResponseRedirect('..')

def del_qands_from_sheet(request, sheet_id, id_qands):
    q = QAndS.objects.get(id= id_qands)
    q.delete()
    return HttpResponseRedirect('../..')


def export_pdf(request, sheet_id=None):
    if sheet_id:
        import os
        import subprocess
        
        this_sheet = Sheet.objects.get(id=sheet_id)
        this_qands = QAndS.objects.filter(sheet=this_sheet)
        
        #SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        #filename = SITE_ROOT + '/tmp/' + str(request.session['user']) + str(sheet_id)
        try:
            filename = str(request.session['sm_user']) + str(sheet_id)
        except:
            filename = 'anonymous' + str(sheet_id)
        tex = codecs.open('tmp/' + filename + '.tex', mode='w', encoding='utf-8')
        tex.write("\\documentclass[a4paper, ")
        if request.GET.get('solution', False):
            tex.write("answers")
        tex.write("]{exam}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{amsfonts}\\begin{document}\n\\begin{questions}\n")
        for qands in this_qands:
            tex.write("\question ")
            tex.write(qands.question)
            tex.write("\n\\begin{solution}\n")
            tex.write(qands.solution)
            tex.write("\n\\end{solution}\n")
        tex.write("\\end{questions}\\end{document}")
        tex.close()
        
        #subprocess.call(['pdflatex', '-interaction=nonstopmode', '-output-directory=' + SITE_ROOT + 'tmp', SITE_ROOT + 'tmp/' + filename + '.tex'])
        subprocess.call(['pdflatex', '-interaction=nonstopmode', '-output-directory=tmp', 'tmp/' + filename + '.tex'])
        
        pdf = open('tmp/' + filename + '.pdf', 'r')

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename=' + filename + '.pdf'
        return response
