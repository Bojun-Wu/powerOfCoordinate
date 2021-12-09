from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from init import initDb


def setting(request):
    initDb()
    return HttpResponseRedirect('/show_result/home')
