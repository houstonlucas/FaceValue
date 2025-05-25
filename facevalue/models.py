from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Tag model for categorizing puzzles
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Puzzle(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    avg_rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='puzzles')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['puzzle', 'user'], name='one_review_per_user')
        ]

    def __str__(self):
        return f"{self.puzzle.name} - {self.user.username}"

# Signals to update Puzzle stats when Reviews change
@receiver([post_save, post_delete], sender=Review)
def update_puzzle_rating_stats(sender, instance, **kwargs):
    puzzle = instance.puzzle
    agg = puzzle.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    puzzle.avg_rating = agg['avg'] or 0
    puzzle.review_count = agg['count'] or 0
    puzzle.save()

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='replies', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review}"
