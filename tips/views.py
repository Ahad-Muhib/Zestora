from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import CookingTip, TipCategory
from .tip_data import TIPS_CONTENT, BASICS_CONTENT

def tip_list(request):
    tips = CookingTip.objects.all().order_by('-created_at')
    categories = TipCategory.objects.all()
    return render(request, 'tips/tip_list.html', {'tips': tips, 'categories': categories, 'active_page': 'cooking_tips'})

def tip_detail(request, slug):
    tip = get_object_or_404(CookingTip, slug=slug)
    return render(request, 'tips/tip_detail.html', {'tip': tip, 'active_page': 'cooking_tips'})

def tip_category(request, slug):
    category = get_object_or_404(TipCategory, slug=slug)
    tips = CookingTip.objects.filter(category=category)
    return render(request, 'tips/tip_category.html', {'category': category, 'tips': tips, 'active_page': 'cooking_tips'})

def tip_content_detail(request, slug):
    """Display detailed content for tips and basics"""
    # Check in both tips and basics content
    content = TIPS_CONTENT.get(slug) or BASICS_CONTENT.get(slug)
    
    if not content:
        raise Http404("Tip content not found")
    
    return render(request, 'tips/tip_content_detail.html', {
        'content': content,
        'active_page': 'cooking_tips'
    })
