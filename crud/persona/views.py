from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Persona
from django.db.models import Q  
# Import login mixins if needed
from django.contrib.auth.mixins import LoginRequiredMixin


class PersonaListView(ListView):
    model = Persona
    template_name = "persona/lista.html"
    context_object_name = "personas"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Personas"
        return context
    

class PersonaDetailView(DetailView):
    model = Persona
    template_name = "persona/detalle.html"
    context_object_name = "persona"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle de Persona"
        return context

class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = "persona/crear.html"
    fields = ['nombre', 'edad', 'email']
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Persona"
        return context

class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    template_name = "persona/crear.html"
    fields = ['nombre', 'edad', 'email']
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Persona"
        return context

class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    template_name = "persona/eliminar.html"
    context_object_name = "persona"
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Borrar Persona"
        context['confirm_message'] = "¿Estás seguro de que deseas eliminar esta persona?"
        context['cancel_url'] = reverse_lazy('persona:lista')
        return context

class PersonaSearchView(ListView):
    model = Persona
    template_name = "persona/buscar.html"
    context_object_name = "personas"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Persona.objects.filter(nombre__icontains=query)
        return Persona.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Buscar Personas"
        context['query'] = self.request.GET.get('q', '')
        return context

