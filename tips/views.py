from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CookingTip, TipCategory

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
