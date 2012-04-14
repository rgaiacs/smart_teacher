# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django import forms
from django.contrib.auth.models import User
from sheet.models import Sheet

def list_qands(request):
    """
    Return a list of qands.
    """
    return NotImplementedError

def apply_qands(request):
    """
    Try to save in the database a qands and return the result message.
    """
    return NotImplementedError
