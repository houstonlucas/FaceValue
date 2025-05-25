from django import forms
from .models import Puzzle, Review, Comment
from .models import Tag
from django.contrib.auth.models import User

class PuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ['name', 'brand', 'type', 'tags']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
class ReviewFormWithPuzzle(ReviewForm):
    puzzle = forms.ModelChoiceField(queryset=Puzzle.objects.all(), required=True)
    
    class Meta(ReviewForm.Meta):
        fields = ['puzzle', 'rating', 'comment']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReviewFilterForm(forms.Form):
    puzzle = forms.ModelChoiceField(
        queryset=Puzzle.objects.all(),
        required=False,
        empty_label='All Puzzles'
    )
    brand = forms.ChoiceField(
        choices=[('', 'All Brands')] + [(b, b) for b in Puzzle.objects.values_list('brand', flat=True).distinct()],
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    rating = forms.ChoiceField(
        choices=[('', 'All Ratings')] + [(str(i), str(i)) for i in range(1, 6)],
        required=False
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label='All Users'
    )
