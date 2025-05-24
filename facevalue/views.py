from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Puzzle
from .forms import PuzzleForm

def home(request):
    """
    Render homepage using template extending base layout.
    """
    return render(request, 'home.html')

class PuzzleManagementView(ListView):
    model = Puzzle
    template_name = 'puzzle_management.html'
    context_object_name = 'puzzles'

class PuzzleCreateView(CreateView):
    model = Puzzle
    form_class = PuzzleForm
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_management')

class PuzzleUpdateView(UpdateView):
    model = Puzzle
    form_class = PuzzleForm
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_management')

class PuzzleDeleteView(DeleteView):
    model = Puzzle
    template_name = 'puzzle_confirm_delete.html'
    success_url = reverse_lazy('puzzle_management')