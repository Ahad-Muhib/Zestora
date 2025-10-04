# This will be added to recipes/models.py
from django.db import models
from django.contrib.auth.models import User

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recipe')
        ordering = ['-saved_at']
    
    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"
