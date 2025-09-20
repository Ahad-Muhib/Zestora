from django import forms
from django.utils.text import slugify
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'category', 'ingredients', 
            'instructions', 'prep_time', 'cook_time', 'servings', 
            'difficulty', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe your recipe...',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'List ingredients, one per line...',
                'rows': 8
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Provide step-by-step instructions...',
                'rows': 10
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Minutes',
                'min': '1'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Minutes',
                'min': '1'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Number of servings',
                'min': '1'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure we have categories available
        self.fields['category'].queryset = Category.objects.all()
        
        # Add help text
        self.fields['ingredients'].help_text = 'Enter each ingredient on a new line (e.g., "2 cups flour")'
        self.fields['instructions'].help_text = 'Provide clear, step-by-step cooking instructions'
        self.fields['prep_time'].help_text = 'Time needed for preparation (in minutes)'
        self.fields['cook_time'].help_text = 'Time needed for cooking (in minutes)'

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if not recipe.slug:
            recipe.slug = slugify(recipe.title)
            # Ensure slug is unique
            counter = 1
            original_slug = recipe.slug
            while Recipe.objects.filter(slug=recipe.slug).exists():
                recipe.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if commit:
            recipe.save()
        return recipe