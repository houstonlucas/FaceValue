from django import forms
from .models import Puzzle

class PuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ['name', 'brand', 'type']
