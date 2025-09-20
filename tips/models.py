from django.db import models
from django.contrib.auth.models import User

class TipCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tip Categories"

class CookingTip(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    short_description = models.CharField(max_length=300)
    category = models.ForeignKey(TipCategory, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    image = models.ImageField(upload_to='tips/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Cooking Tip"
        verbose_name_plural = "Cooking Tips"
