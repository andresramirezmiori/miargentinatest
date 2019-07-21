from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from exercise.forms import UsuarioArgentinaForm
from exercise.models import UsuarioArgenitna

def index(request):
    return HttpResponse("Hola mundo")


class UsuarioArgenitnaDetailView(generic.DetailView):
    model = UsuarioArgenitna
    template_name = 'exercise/user_detail.html'
    context_object_name = 'usuario'


class UsuarioArgenitnaCreateView(generic.edit.CreateView):
    model = UsuarioArgenitna
    form_class = UsuarioArgentinaForm
    template_name = 'exercise/user_form.html'


class UsuarioArgenitnaUpdateView(generic.edit.UpdateView):
    model = UsuarioArgenitna
    form_class = UsuarioArgentinaForm
    template_name = 'exercise/user_form.html'


user_create = UsuarioArgenitnaCreateView.as_view()
user_update = UsuarioArgenitnaUpdateView.as_view()
user_detail = UsuarioArgenitnaDetailView.as_view()
