from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recipe, Category
from .forms import RecipeForm

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'active_page': 'recipes'})

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'active_page': 'recipes'})

def category_list(request):
    categories = Category.objects.all().order_by('name')
    
    # Add recipe count and sample recipes for each category
    categories_with_recipes = []
    for category in categories:
        category_recipes = Recipe.objects.filter(category=category).order_by('-created_at')
        # Get more recipes for carousel (up to 5) but limit display recipes to 3
        sample_recipes = category_recipes[:5]  # Get up to 5 for carousel
        display_recipes = category_recipes[:3]  # Limit to 3 for display list
        
        categories_with_recipes.append({
            'category': category,
            'recipe_count': category_recipes.count(),
            'sample_recipes': sample_recipes,  # For carousel
            'display_recipes': display_recipes  # For text list
        })
    
    return render(request, 'recipes/category_list.html', {
        'categories_with_recipes': categories_with_recipes,
        'categories': categories,  # Keep for backward compatibility
        'active_page': 'categories'
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(category=category)
    
    # Handle sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        recipes = recipes.order_by('created_at')
    elif sort_by == 'difficulty':
        recipes = recipes.order_by('difficulty', 'title')
    elif sort_by == 'time':
        recipes = recipes.extra(select={'total_time': 'prep_time + cook_time'}).order_by('total_time')
    else:  # newest (default)
        recipes = recipes.order_by('-created_at')
    
    return render(request, 'recipes/category_detail.html', {
        'category': category, 
        'recipes': recipes,
        'sort_by': sort_by,
        'active_page': 'categories'
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Use the currently logged-in user
            recipe.save()
            messages.success(request, f'Recipe "{recipe.title}" has been added successfully!')
            return redirect('recipes:recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'page_title': 'Add New Recipe',
        'active_page': 'recipes'
    })
