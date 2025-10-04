from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from datetime import datetime
import weasyprint
from .models import Recipe, Category, SavedRecipe, Comment
from .forms import RecipeForm, CommentForm

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'active_page': 'recipes'})

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            
            # Check if this is a reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, recipe=recipe)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass
            
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('recipes:recipe_detail', slug=slug)
    else:
        comment_form = CommentForm() if request.user.is_authenticated else None
    
    # Get comments (only top-level comments, replies are accessed via the replies relationship)
    comments = Comment.objects.filter(recipe=recipe, parent=None, is_active=True).order_by('-created_at')
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'is_saved': is_saved,
        'comments': comments,
        'comment_form': comment_form,
        'active_page': 'recipes'
    })

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

@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Check if the current user is the author of the recipe
    if recipe.author != request.user:
        messages.error(request, 'You can only edit your own recipes.')
        return redirect('recipes:recipe_detail', slug=recipe.slug)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            updated_recipe = form.save()
            messages.success(request, f'Recipe "{updated_recipe.title}" has been updated successfully!')
            return redirect('recipes:recipe_detail', slug=updated_recipe.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'recipe': recipe,
        'page_title': f'Edit {recipe.title}',
        'active_page': 'recipes'
    })

@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Check if the current user is the author of the recipe
    if recipe.author != request.user:
        messages.error(request, 'You can only delete your own recipes.')
        return redirect('recipes:recipe_detail', slug=recipe.slug)
    
    if request.method == 'POST':
        recipe_title = recipe.title
        messages.success(request, f'Recipe "{recipe_title}" has been deleted successfully!')
        return redirect('recipes:recipe_list')
    
    return render(request, 'recipes/delete_recipe.html', {
        'recipe': recipe,
        'active_page': 'recipes'
    })

def download_recipe_pdf(request, slug):
    """Generate and download a PDF version of the recipe."""
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Parse ingredients and instructions into lists
    ingredients_list = [line.strip() for line in recipe.ingredients.split('\n') if line.strip()]
    instructions_list = [line.strip() for line in recipe.instructions.split('\n') if line.strip()]
    
    # Prepare context for PDF template
    context = {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
        'instructions_list': instructions_list,
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    
    # Render HTML template
    html_string = render_to_string('recipes/recipe_pdf.html', context)
    
    # Generate PDF
    html = weasyprint.HTML(string=html_string)
    pdf = html.write_pdf()
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recipe.slug}-recipe.pdf"'
    
    return response

@login_required
def toggle_save_recipe(request, slug):
    """Toggle save/unsave recipe"""
    recipe = get_object_or_404(Recipe, slug=slug)
    
    saved_recipe = SavedRecipe.objects.filter(user=request.user, recipe=recipe).first()
    
    if saved_recipe:
        # Unsave the recipe
        saved_recipe.delete()
        is_saved = False
        message = 'Recipe removed from saved recipes'
    else:
        # Save the recipe
        SavedRecipe.objects.create(user=request.user, recipe=recipe)
        is_saved = True
        message = 'Recipe saved successfully!'
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_saved': is_saved,
            'message': message
        })
    
    # For non-AJAX requests, redirect back
    messages.success(request, message)
    return redirect('recipes:recipe_detail', slug=slug)
