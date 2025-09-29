from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Fix ingredients and instructions formatting for better display'

    def handle(self, *args, **options):
        updated_count = 0
        
        for recipe in Recipe.objects.all():
            # Fix ingredients formatting
            if recipe.ingredients:
                ingredients_lines = [line.strip() for line in recipe.ingredients.split('\n') if line.strip()]
                # Ensure each ingredient is on a separate line
                formatted_ingredients = '\n'.join(ingredients_lines)
                
                # Fix instructions formatting  
                if recipe.instructions:
                    instructions_lines = [line.strip() for line in recipe.instructions.split('\n') if line.strip()]
                    # Ensure each instruction step is on a separate line
                    formatted_instructions = '\n'.join(instructions_lines)
                    
                    # Update the recipe if changes were made
                    if (formatted_ingredients != recipe.ingredients or 
                        formatted_instructions != recipe.instructions):
                        recipe.ingredients = formatted_ingredients
                        recipe.instructions = formatted_instructions
                        recipe.save()
                        updated_count += 1
                        self.stdout.write(f'✓ Fixed formatting for {recipe.title}')
                    else:
                        self.stdout.write(f'- {recipe.title} already has good formatting')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated formatting for {updated_count} recipes!')
        )