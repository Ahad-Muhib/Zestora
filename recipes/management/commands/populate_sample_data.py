from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from tips.models import CookingTip, TipCategory
from community.models import CulinaryStory

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        # Create default user if not exists
        user, created = User.objects.get_or_create(
            username='chef_zestora',
            defaults={
                'first_name': 'Chef',
                'last_name': 'Zestora',
                'email': 'chef@zestora.com',
                'is_staff': True
            }
        )
        
        # Create categories
        categories_data = [
            {'name': 'Breakfast', 'slug': 'breakfast', 'description': 'Morning meals and brunch recipes'},
            {'name': 'Lunch', 'slug': 'lunch', 'description': 'Midday meals and light dishes'},
            {'name': 'Dinner', 'slug': 'dinner', 'description': 'Evening meals and main courses'},
            {'name': 'Dessert', 'slug': 'dessert', 'description': 'Sweet treats and desserts'},
            {'name': 'Appetizer', 'slug': 'appetizer', 'description': 'Starter dishes and snacks'},
            {'name': 'Vegetarian', 'slug': 'vegetarian', 'description': 'Plant-based recipes'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample recipes
        recipes_data = [
            {
                'title': 'Savory Herb-Infused Chicken',
                'slug': 'savory-herb-chicken',
                'description': 'Indulge in the rich and savory symphony of flavors with our Savory Herb-Infused Chicken. This dish combines aromatic herbs with tender chicken for a memorable dining experience.',
                'ingredients': '''2 lbs chicken thighs
3 tbsp olive oil
4 cloves garlic, minced
2 tbsp fresh rosemary
2 tbsp fresh thyme
1 tbsp fresh oregano
1 lemon, juiced
Salt and pepper to taste
1 cup chicken broth''',
                'instructions': '''1. Preheat oven to 375°F (190°C)
2. Mix olive oil, garlic, herbs, lemon juice, salt, and pepper in a bowl
3. Coat chicken thighs with the herb mixture
4. Place chicken in a baking dish
5. Pour chicken broth around the chicken
6. Bake for 45-50 minutes until golden and cooked through
7. Let rest for 5 minutes before serving
8. Garnish with fresh herbs and lemon wedges''',
                'prep_time': 15,
                'cook_time': 45,
                'servings': 4,
                'difficulty': 'easy',
                'category': 'dinner',
                'featured': True
            },
            {
                'title': 'Decadent Chocolate Mousse',
                'slug': 'chocolate-mousse',
                'description': 'Dive into the velvety indulgence of our Decadent Chocolate Mousse. A dessert that transcends the ordinary with its rich, creamy texture and intense chocolate flavor.',
                'ingredients': '''8 oz dark chocolate (70% cacao)
4 large eggs, separated
1/4 cup sugar
1 cup heavy cream
2 tbsp coffee liqueur (optional)
Pinch of salt
Fresh berries for garnish''',
                'instructions': '''1. Melt chocolate in a double boiler, let cool slightly
2. Beat egg yolks with half the sugar until pale
3. Gradually add melted chocolate to egg yolks
4. Beat egg whites with remaining sugar until stiff peaks
5. Whip cream until soft peaks form
6. Fold egg whites into chocolate mixture
7. Gently fold in whipped cream
8. Add coffee liqueur if desired
9. Divide into serving glasses
10. Chill for at least 4 hours before serving''',
                'prep_time': 20,
                'cook_time': 10,
                'servings': 6,
                'difficulty': 'medium',
                'category': 'dessert',
                'featured': True
            },
            {
                'title': 'Mediterranean Quinoa Bowl',
                'slug': 'mediterranean-quinoa-bowl',
                'description': 'A healthy and vibrant Mediterranean Quinoa Bowl packed with fresh vegetables, herbs, and a tangy lemon dressing.',
                'ingredients': '''1 cup quinoa
2 cups vegetable broth
1 cucumber, diced
2 tomatoes, diced
1/2 red onion, thinly sliced
1/2 cup kalamata olives
1/2 cup feta cheese, crumbled
1/4 cup fresh parsley
1/4 cup fresh mint
3 tbsp olive oil
2 tbsp lemon juice
Salt and pepper to taste''',
                'instructions': '''1. Rinse quinoa and cook in vegetable broth for 15 minutes
2. Let quinoa cool to room temperature
3. Mix olive oil, lemon juice, salt, and pepper for dressing
4. Combine quinoa with all vegetables
5. Add olives and feta cheese
6. Toss with dressing
7. Garnish with fresh herbs
8. Serve immediately or chill for 30 minutes''',
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'category': 'lunch'
            },
            {
                'title': 'Fluffy Pancakes with Berries',
                'slug': 'fluffy-pancakes-berries',
                'description': 'Light and fluffy pancakes topped with fresh berries and maple syrup - the perfect weekend breakfast treat.',
                'ingredients': '''2 cups all-purpose flour
2 tbsp sugar
2 tsp baking powder
1/2 tsp salt
2 large eggs
1 3/4 cups milk
1/4 cup melted butter
1 tsp vanilla extract
1 cup mixed berries
Maple syrup for serving''',
                'instructions': '''1. Mix dry ingredients in a large bowl
2. Whisk eggs, milk, butter, and vanilla in another bowl
3. Add wet ingredients to dry ingredients, mix until just combined
4. Heat griddle or pan over medium heat
5. Pour 1/4 cup batter for each pancake
6. Cook until bubbles form on surface
7. Flip and cook until golden brown
8. Serve with berries and maple syrup''',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'category': 'breakfast'
            }
        ]
        
        for recipe_data in recipes_data:
            category_slug = recipe_data.pop('category')
            recipe, created = Recipe.objects.get_or_create(
                slug=recipe_data['slug'],
                defaults={
                    **recipe_data,
                    'category': categories[category_slug],
                    'author': user
                }
            )
            if created:
                self.stdout.write(f'Created recipe: {recipe.title}')
        
        # Create tip categories
        tip_categories_data = [
            {'name': 'Knife Skills', 'slug': 'knife-skills'},
            {'name': 'Cooking Techniques', 'slug': 'cooking-techniques'},
            {'name': 'Ingredient Tips', 'slug': 'ingredient-tips'},
            {'name': 'Kitchen Hacks', 'slug': 'kitchen-hacks'},
        ]
        
        tip_categories = {}
        for cat_data in tip_categories_data:
            category, created = TipCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            tip_categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created tip category: {category.name}')
        
        # Create sample cooking tips
        tips_data = [
            {
                'title': 'Perfect Knife Sharpening Technique',
                'slug': 'knife-sharpening-technique',
                'content': 'A sharp knife is the most important tool in your kitchen. Hold the knife at a 20-degree angle against the sharpening stone and use smooth, consistent strokes. Always sharpen both sides equally.',
                'short_description': 'Learn the proper technique for keeping your knives razor-sharp',
                'category': 'knife-skills',
                'difficulty': 'beginner'
            },
            {
                'title': 'How to Properly Season a Cast Iron Pan',
                'slug': 'season-cast-iron-pan',
                'content': 'Seasoning creates a natural non-stick surface. Clean the pan, apply a thin layer of oil, and bake at 350°F for an hour. Repeat this process 2-3 times for best results.',
                'short_description': 'Master the art of cast iron seasoning for a lifetime of great cooking',
                'category': 'cooking-techniques',
                'difficulty': 'intermediate'
            },
            {
                'title': 'Storing Fresh Herbs to Last Longer',
                'slug': 'storing-fresh-herbs',
                'content': 'Wrap herbs in damp paper towels and store in the refrigerator. For woody herbs like rosemary and thyme, store them like flowers in a glass of water.',
                'short_description': 'Keep your fresh herbs fresh for weeks with these simple storage tips',
                'category': 'ingredient-tips',
                'difficulty': 'beginner'
            }
        ]
        
        for tip_data in tips_data:
            category_slug = tip_data.pop('category')
            tip, created = CookingTip.objects.get_or_create(
                slug=tip_data['slug'],
                defaults={
                    **tip_data,
                    'category': tip_categories[category_slug]
                }
            )
            if created:
                self.stdout.write(f'Created tip: {tip.title}')
        
        # Create sample community stories
        stories_data = [
            {
                'title': 'My First Perfect Soufflé',
                'slug': 'first-perfect-souffle',
                'content': 'After months of failed attempts, I finally mastered the art of making a perfect soufflé. The key was understanding the importance of room temperature ingredients and not opening the oven door too early. The moment I saw that beautiful rise, I knew all the practice was worth it!',
                'author': 'Sarah M.',
                'likes': 15
            },
            {
                'title': 'Cooking with My Grandmother',
                'slug': 'cooking-with-grandmother',
                'content': 'Every Sunday, my grandmother and I would cook together. She taught me not just recipes, but the love and patience that goes into every dish. Her secret ingredient was always a pinch of love, and I carry that tradition forward in my own kitchen.',
                'author': 'Michael R.',
                'likes': 23
            }
        ]
        
        for story_data in stories_data:
            story, created = CulinaryStory.objects.get_or_create(
                slug=story_data['slug'],
                defaults=story_data
            )
            if created:
                self.stdout.write(f'Created story: {story.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
