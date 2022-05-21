from django.shortcuts import render
from django.http import HttpResponse
import pickle
import os


def main(request):
    return HttpResponse("<h1>Linear Model Main Page</h1>")
