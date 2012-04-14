# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django import forms
from django.contrib.auth.models import User
from sheet.models import Sheet
from smartqands.models import SmartQAndS
from qands.models import QAndS
from django.contrib.auth.models import User

class SheetForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title', help_text="A title for this sheet.")
    des = forms.CharField(widget=forms.Textarea(), required=False, label='Description', help_text="A description of this sheet.")

def list_sheets(request):
    c = {}
    this_user = User.objects.get(username=request.user.username)
    sheets = Sheet.objects.filter(user=this_user)
    c['sheets'] = sheets
    return render_to_response('list.html', c)

def edit_sheet(request, id_sheet=None):
    """
    If id_sheet != None it edit the sheet otherwise it create a new one.
    """
    c = {}
    t = 'edit.html'
    if id_sheet:
        if request.method == "GET":
            form = SheetForm(request.GET)
            if form.is_valid():
                old_sheet = Sheet.objects.get(id=id_sheet)
                old_sheet.title = form.cleaned_data['title']
                old_sheet.des = form.cleaned_data['des']
                old_sheet.save()
                return HttpResponseRedirect('..')
            else:
                c['id_sheet'] = id_sheet
                old = Sheet.objects.get(id=id_sheet)
                init = {}
                init['title'] = old.title
                init['des'] = old.des
                form = SheetForm(initial=init)
                c['form'] = form
    else:
        if request.method == "GET":
            form = SheetForm(request.GET)
            if form.is_valid():
                new_sheet = Sheet(title=form.cleaned_data['title'], des=form.cleaned_data['des'])
                new_sheet.save()
                this_user = User.objects.get(username=request.user.username)
                new_sheet.user.add(this_user)
                new_sheet.save()
                return HttpResponseRedirect('sheet/' + str(new_sheet.id))
            else:
                form = SheetForm()
                c['form'] = form
    return render_to_response(t, c)

def del_sheet(request, id_sheet):
    old_sheet = Sheet.objects.get(id=id_sheet)
    old_sheet.delete()
    return HttpResponseRedirect('../..')

def show_sheet(request, id_sheet):
    c = {}
    this_sheet = Sheet.objects.get(id=id_sheet)
    c['sheet'] = this_sheet
    qandss = QAndS.objects.filter(sheet=this_sheet)
    c['qandss'] = qandss
    return render_to_response('sheet.html', c)

def show_qands_from_sheet(request, id_sheet, id_qands):
    c = {}
    this_sheet = Sheet.objects.get(id=id_sheet)
    this_qands = QAndS.objects.get(id=id_qands)
    return HttpResponseRedirect('../../../smartqands/' + str(this_qands.smartqands.id))

def add_qands_to_sheet(request, id_sheet, id_qands):
    c = {}
    try:
        this_sheet = Sheet(id=id_sheet)
        s_q = SmartQAndS.objects.get(id=id_qands_to_add)
        q = QAndS(sheet=this_sheet, smartqands=s_q, question=s_q.question, solution=s_q.solution)
        q.save()
    except:
        print 'error'
    return HttpResponseRedirect('..')

def del_qands_from_sheet(request, id_sheet, id_qands):
    q = QAndS.objects.get(id= id_qands)
    q.delete()
    return HttpResponseRedirect('../..')


def export_pdf(request, id_sheet=None):
    if id_sheet:
        import os
        import subprocess
        
        this_sheet = Sheet.objects.get(id=id_sheet)
        this_qands = QAndS.objects.filter(sheet=this_sheet)
        
        #SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        #filename = SITE_ROOT + '/tmp/' + str(request.session['user']) + str(id_sheet)
        filename = 'tmp/' + str(request.session['user']) + str(id_sheet)
        tex = open(filename + '.tex', 'w')
        if request.GET.get('solution', False):
            tex.write("\\documentclass[a4paper, answers]{exam}\n\\begin{document}\n\\begin{questions}\n")
        else:
            tex.write("\\documentclass[a4paper]{exam}\n\\begin{document}\n\\begin{questions}\n")
        for qands in this_qands:
            tex.write("\question ")
            tex.write(qands.question)
            tex.write("\n\\begin{solution}\n")
            tex.write(qands.solution)
            tex.write("\n\\end{solution}\n")
        tex.write("\\end{questions}\\end{document}")
        tex.close()
        
        #subprocess.call(['pdflatex', '-interaction=nonstopmode', '-output-directory=' + SITE_ROOT + 'tmp', filename + '.tex'])
        subprocess.call(['pdflatex', '-interaction=nonstopmode', '-output-directory=tmp', filename + '.tex'])
        
        pdf = open(filename + '.pdf', 'r')

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename=' + filename + '.pdf'
        return response
