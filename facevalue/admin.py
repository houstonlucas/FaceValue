from django.contrib import admin
from .models import Puzzle, Review, Comment, Tag

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ReviewAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('puzzle', 'user', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'updated_at', 'user', 'puzzle')
    search_fields = ('comment',)

class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'type', 'slug', 'avg_rating', 'review_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'brand', 'type')
    list_filter = ('brand', 'type', 'tags')
    filter_horizontal = ('tags',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'parent', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'user')

admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
