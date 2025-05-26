from django import forms
from .models import Puzzle, Review, Comment
from .models import Tag
from django.contrib.auth.models import User

class BootstrapFormMixin:
    """Mixin to add Bootstrap CSS classes to form fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs['class'] = 'form-select'
                field.widget.attrs['multiple'] = True
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['rows'] = 4
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Add placeholder text for better UX
            if hasattr(field, 'label') and field.label:
                field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'

class PuzzleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ['name', 'brand', 'type', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'placeholder': 'Share your thoughts about this puzzle...'}),
        }
        
class ReviewFormWithPuzzle(ReviewForm):
    puzzle = forms.ModelChoiceField(queryset=Puzzle.objects.all(), required=True)
    
    class Meta(ReviewForm.Meta):
        fields = ['puzzle', 'rating', 'comment']

class CommentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add your comment...', 'rows': 3}),
        }

class ReviewFilterForm(BootstrapFormMixin, forms.Form):
    puzzle = forms.ModelChoiceField(
        queryset=Puzzle.objects.all(),
        required=False,
        empty_label='All Puzzles'
    )
    brand = forms.ChoiceField(choices=[('', 'All Brands')], required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    rating = forms.ChoiceField(
        choices=[('', 'All Ratings')] + [(str(i), f'{i} Stars') for i in range(1, 6)],
        required=False
    )
    user = forms.CharField(
        required=False,
        label='User',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by username'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate brand choices and tags queryset to avoid import-time DB queries
        brands = Puzzle.objects.values_list('brand', flat=True).distinct()
        self.fields['brand'].choices = [('', 'All Brands')] + [(b, b) for b in brands]
        self.fields['tags'].queryset = Tag.objects.all()
