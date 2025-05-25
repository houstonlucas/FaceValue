from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django import forms
from django.db.models import Prefetch
from .models import Puzzle, Review, Comment
from .forms import PuzzleForm, ReviewForm, CommentForm, ReviewFilterForm, ReviewFormWithPuzzle

def home(request):
    """
    Render homepage using template extending base layout.
    """
    return render(request, 'home.html')

class PuzzleManagementView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Puzzle
    template_name = 'puzzle_management.html'
    context_object_name = 'puzzles'
    
    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        from datetime import timedelta
        from .models import Review

        # Total reviews across all puzzles
        context['total_reviews'] = Review.objects.count()

        # Active reviewers in last 24 hours
        active_window = timezone.now() - timedelta(hours=24)
        context['active_reviewers'] = (
            Review.objects.filter(created_at__gte=active_window)
                          .values('user')
                          .distinct()
                          .count()
        )
        return context

class PuzzleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Puzzle
    form_class = PuzzleForm
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_management')
    
    def test_func(self):
        return self.request.user.is_staff

class PuzzleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Puzzle
    form_class = PuzzleForm
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_management')
    
    def test_func(self):
        return self.request.user.is_staff

class PuzzleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Puzzle
    template_name = 'puzzle_confirm_delete.html'
    success_url = reverse_lazy('puzzle_management')
    
    def test_func(self):
        return self.request.user.is_staff

class PuzzleDetailView(DetailView):
    model = Puzzle
    template_name = 'puzzle_detail.html'
    context_object_name = 'puzzle'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Create a prefetch object to get top-level comments
        top_comments = Prefetch(
            'comments',
            queryset=Comment.objects.filter(parent__isnull=True).select_related('user').prefetch_related(
                Prefetch('replies', queryset=Comment.objects.select_related('user'))
            ),
            to_attr='top_level_comments'
        )
        
        # Use it in our main queryset
        return Puzzle.objects.prefetch_related(
            Prefetch('reviews', queryset=Review.objects.select_related('user').prefetch_related(top_comments))
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['comment_form'] = CommentForm()
        
        # Check if user has already reviewed this puzzle
        puzzle = self.get_object()
        if self.request.user.is_authenticated:
            user_reviews = [r for r in puzzle.reviews.all() if r.user == self.request.user]
            context['user_has_reviewed'] = len(user_reviews) > 0
        else:
            context['user_has_reviewed'] = False
            
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review_form.html'
    
    def get_form_class(self):
        if 'slug' in self.kwargs:
            return ReviewForm
        else:
            # Use a form with puzzle selection field
            return ReviewFormWithPuzzle

    def form_valid(self, form):
        if 'slug' in self.kwargs:
            # From puzzle detail page
            puzzle = get_object_or_404(Puzzle, slug=self.kwargs['slug'])
            form.instance.puzzle = puzzle
        # Always set the user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('puzzle_detail', kwargs={'slug': self.object.puzzle.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'slug' in self.kwargs:
            context['puzzle'] = get_object_or_404(Puzzle, slug=self.kwargs.get('slug'))
        return context

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse('puzzle_detail', kwargs={'slug': self.object.puzzle.slug})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse_lazy('puzzle_detail', kwargs={'slug': self.object.puzzle.slug})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def form_valid(self, form):
        review = get_object_or_404(Review, pk=self.kwargs['review_pk'])
        form.instance.review = review
        # handle replies
        parent_id = self.request.GET.get('parent')
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, pk=parent_id)
        form.instance.user = self.request.user
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = get_object_or_404(Review, pk=self.kwargs['review_pk'])
        parent_id = self.request.GET.get('parent')
        if parent_id:
            context['parent'] = get_object_or_404(Comment, pk=parent_id)
        return context

    def get_success_url(self):
        return reverse('puzzle_detail', kwargs={'slug': self.object.review.puzzle.slug})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object.review
        puzzle = review.puzzle
        context['review'] = review
        return context

    def get_success_url(self):
        puzzle = self.object.review.puzzle
        if not puzzle.slug:
            # Regenerate slug if missing
            puzzle.slug = slugify(puzzle.name)
            puzzle.save()
        return reverse('puzzle_detail', kwargs={'slug': puzzle.slug})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse_lazy('puzzle_detail', kwargs={'slug': self.object.review.puzzle.slug})

class ReviewListView(LoginRequiredMixin, ListView):
    """List all reviews with optional filtering."""
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        qs = Review.objects.select_related('puzzle', 'user').all()
        form = ReviewFilterForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('puzzle'):
                qs = qs.filter(puzzle=data['puzzle'])
            if data.get('brand'):
                qs = qs.filter(puzzle__brand=data['brand'])
            if data.get('tags'):
                qs = qs.filter(puzzle__tags__in=data['tags']).distinct()
            if data.get('rating'):
                qs = qs.filter(rating=data['rating'])
            if data.get('user'):
                # Fuzzy match on username
                qs = qs.filter(user__username__icontains=data['user'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ReviewFilterForm(self.request.GET)
        return context