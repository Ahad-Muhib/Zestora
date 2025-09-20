from django.contrib import admin
from .models import Category, Recipe, RecipeStep

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'difficulty', 'featured', 'created_at')
    list_filter = ('category', 'difficulty', 'featured', 'created_at')
    search_fields = ('title', 'description', 'ingredients', 'instructions')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'image')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'instructions', 'prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Publication', {
            'fields': ('author', 'featured')
        }),
    )

@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'step_number', 'instruction_preview')
    list_filter = ('recipe',)
    ordering = ('recipe', 'step_number')
    
    def instruction_preview(self, obj):
        return obj.instruction[:50] + '...' if len(obj.instruction) > 50 else obj.instruction
    instruction_preview.short_description = 'Instruction Preview'
