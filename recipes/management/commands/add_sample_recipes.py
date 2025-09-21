from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category

class Command(BaseCommand):
    help = 'Add sample recipes to the database'

    def handle(self, *args, **options):
        # Get or create a user
        user, created = User.objects.get_or_create(
            username='chef_zestora',
            defaults={
                'first_name': 'Chef',
                'last_name': 'Zestora',
                'email': 'chef@zestora.com'
            }
        )
        
        # Get categories
        categories = {cat.slug: cat for cat in Category.objects.all()}
        
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
            },
            {
                'title': 'Creamy Mushroom Risotto',
                'slug': 'creamy-mushroom-risotto',
                'description': 'A luxurious and creamy mushroom risotto that brings the authentic taste of Italy to your table. Perfect for a romantic dinner or special occasion.',
                'ingredients': '''1 1/2 cups Arborio rice
4 cups warm chicken or vegetable broth
1 lb mixed mushrooms (cremini, shiitake, oyster)
1 medium onion, finely diced
3 cloves garlic, minced
1/2 cup dry white wine
1/2 cup grated Parmesan cheese
3 tbsp butter
2 tbsp olive oil
Salt and pepper to taste
Fresh parsley for garnish''',
                'instructions': '''1. Heat broth in a saucepan and keep warm
2. Sauté mushrooms in olive oil until golden, set aside
3. In the same pan, cook onion until translucent
4. Add garlic and rice, stir for 2 minutes
5. Add wine and stir until absorbed
6. Add warm broth one ladle at a time, stirring constantly
7. Continue until rice is creamy and al dente (about 18-20 minutes)
8. Stir in mushrooms, butter, and Parmesan
9. Season with salt and pepper
10. Garnish with fresh parsley and serve immediately''',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'category': 'dinner'
            },
            {
                'title': 'Avocado Toast Deluxe',
                'slug': 'avocado-toast-deluxe',
                'description': 'Elevate your morning with this gourmet avocado toast featuring perfectly ripe avocados, cherry tomatoes, and a perfectly poached egg.',
                'ingredients': '''4 slices sourdough bread
2 ripe avocados
1 cup cherry tomatoes, halved
4 eggs
2 tbsp lemon juice
1 tbsp olive oil
1/4 cup microgreens
Salt and pepper to taste
Red pepper flakes (optional)''',
                'instructions': '''1. Toast bread slices until golden
2. Mash avocados with lemon juice, salt, and pepper
3. Poach eggs in simmering water for 3-4 minutes
4. Spread mashed avocado on toast
5. Top with cherry tomatoes
6. Place poached egg on top
7. Drizzle with olive oil
8. Garnish with microgreens and red pepper flakes
9. Serve immediately''',
                'prep_time': 10,
                'cook_time': 10,
                'servings': 4,
                'difficulty': 'easy',
                'category': 'breakfast'
            }
        ]
        
        created_count = 0
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
                created_count += 1
                self.stdout.write(f'Created recipe: {recipe.title}')
            else:
                self.stdout.write(f'Recipe already exists: {recipe.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(recipes_data)} recipes. Created {created_count} new recipes.')
        )
