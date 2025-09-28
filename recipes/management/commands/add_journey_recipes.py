from django.core.management.base import BaseCommand
from recipes.models import Recipe, Category
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add missing recipes from homepage journey section'
    
    def handle(self, *args, **options):
        # Get or create categories
        breakfast_cat, _ = Category.objects.get_or_create(name='Breakfast')
        lunch_cat, _ = Category.objects.get_or_create(name='Lunch')
        dinner_cat, _ = Category.objects.get_or_create(name='Dinner')
        dessert_cat, _ = Category.objects.get_or_create(name='Dessert')
        quick_bite_cat, _ = Category.objects.get_or_create(name='Quick Bite')
        vegan_cat, _ = Category.objects.get_or_create(name='Vegan')
        
        # Get the chef_zestora user as author
        try:
            author = User.objects.get(username='chef_zestora')
        except User.DoesNotExist:
            # Fallback to any available user
            author = User.objects.first()
            if not author:
                self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
                return
        
        # Define missing recipes from journey section
        journey_recipes = [
            {
                'title': 'Lemon Blueberry Pancakes',
                'slug': 'lemon-blueberry-pancakes',
                'description': 'Fluffy pancakes bursting with fresh blueberries and a hint of lemon zest for the perfect breakfast.',
                'category': breakfast_cat,
                'ingredients': '''2 cups all-purpose flour
2 tablespoons sugar
2 teaspoons baking powder
1/2 teaspoon salt
2 large eggs
1 3/4 cups milk
1/4 cup melted butter
1 teaspoon vanilla extract
Zest of 1 lemon
1 cup fresh blueberries
Maple syrup for serving''',
                'instructions': '''1. In a large bowl, whisk together flour, sugar, baking powder, and salt.
2. In another bowl, beat eggs, then whisk in milk, melted butter, vanilla, and lemon zest.
3. Pour wet ingredients into dry ingredients and stir until just combined.
4. Gently fold in blueberries.
5. Heat a griddle or large pan over medium heat.
6. Pour 1/4 cup batter for each pancake.
7. Cook until bubbles form on surface, then flip and cook until golden.
8. Serve hot with maple syrup.''',
                'prep_time': 15,
                'cook_time': 15,
                'servings': 3,
                'difficulty': 'easy',
                'image': 'images/recipes/blueberry-pancakes.jpg'
            },
            {
                'title': 'Mediterranean Pasta Salad',
                'slug': 'mediterranean-pasta-salad',
                'description': 'A refreshing pasta salad with olives, tomatoes, and feta cheese, perfect for summer gatherings.',
                'category': lunch_cat,
                'ingredients': '''1 lb penne pasta
1 cup cherry tomatoes, halved
1/2 cup kalamata olives, pitted
1/2 cup crumbled feta cheese
1/4 red onion, thinly sliced
1/3 cup olive oil
2 tablespoons red wine vinegar
2 cloves garlic, minced
1 teaspoon dried oregano
Salt and pepper to taste
Fresh basil leaves''',
                'instructions': '''1. Cook pasta according to package directions. Drain and rinse with cold water.
2. In a large bowl, combine pasta, tomatoes, olives, feta, and red onion.
3. In a small bowl, whisk together olive oil, vinegar, garlic, oregano, salt, and pepper.
4. Pour dressing over pasta mixture and toss to combine.
5. Refrigerate for at least 1 hour before serving.
6. Garnish with fresh basil leaves before serving.''',
                'prep_time': 20,
                'cook_time': 10,
                'servings': 6,
                'difficulty': 'easy',
                'image': 'images/recipes/pasta-salad.jpg'
            },
            {
                'title': 'Spicy Thai Curry',
                'slug': 'spicy-thai-curry',
                'description': 'An authentic Thai curry with coconut milk, vegetables, and aromatic spices that will transport you to Thailand.',
                'category': dinner_cat,
                'ingredients': '''2 tablespoons red curry paste
1 can coconut milk
1 lb chicken breast, sliced
1 bell pepper, sliced
1 eggplant, cubed
1 tablespoon fish sauce
1 tablespoon brown sugar
Thai basil leaves
Jasmine rice for serving
Lime wedges''',
                'instructions': '''1. Heat a large pan over medium heat and add curry paste.
2. Cook for 1 minute until fragrant.
3. Add thick part of coconut milk and simmer until oil separates.
4. Add chicken and cook until no longer pink.
5. Add remaining coconut milk, vegetables, fish sauce, and sugar.
6. Simmer for 15-20 minutes until vegetables are tender.
7. Stir in Thai basil leaves.
8. Serve over jasmine rice with lime wedges.''',
                'prep_time': 15,
                'cook_time': 35,
                'servings': 4,
                'difficulty': 'medium',
                'image': 'images/recipes/thai-curry.jpg'
            },
            {
                'title': 'Classic Beef Tacos',
                'slug': 'classic-beef-tacos',
                'description': 'Tender seasoned beef in crispy taco shells with fresh toppings and zesty lime.',
                'category': quick_bite_cat,
                'ingredients': '''1 lb ground beef
1 packet taco seasoning
8 taco shells
1 cup shredded lettuce
1 cup diced tomatoes
1/2 cup diced onion
1 cup shredded cheese
Sour cream
Lime wedges
Hot sauce (optional)''',
                'instructions': '''1. Cook ground beef in a large skillet over medium heat until browned.
2. Drain fat and add taco seasoning according to package directions.
3. Warm taco shells in oven according to package directions.
4. Fill each shell with seasoned beef.
5. Top with lettuce, tomatoes, onion, and cheese.
6. Serve with sour cream, lime wedges, and hot sauce.''',
                'prep_time': 10,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'image': 'images/recipes/beef-tacos.jpg'
            },
            {
                'title': 'Gourmet Avocado Toast',
                'slug': 'gourmet-avocado-toast',
                'description': 'Creamy avocado on artisan bread topped with herbs and a drizzle of olive oil.',
                'category': breakfast_cat,
                'ingredients': '''2 slices artisan bread
1 ripe avocado
1 tablespoon lemon juice
Salt and pepper to taste
Extra virgin olive oil
Red pepper flakes
Fresh herbs (basil or cilantro)
Optional: cherry tomatoes, radish slices''',
                'instructions': '''1. Toast bread until golden brown.
2. Mash avocado with lemon juice, salt, and pepper.
3. Spread avocado mixture on toast.
4. Drizzle with olive oil.
5. Sprinkle with red pepper flakes and fresh herbs.
6. Add optional toppings if desired.
7. Serve immediately.''',
                'prep_time': 10,
                'cook_time': 0,
                'servings': 1,
                'difficulty': 'easy',
                'image': 'images/recipes/avocado-toast.jpg'
            },
            {
                'title': 'Classic Caesar Salad',
                'slug': 'classic-caesar-salad',
                'description': 'Crisp romaine lettuce with homemade caesar dressing, croutons, and parmesan.',
                'category': lunch_cat,
                'ingredients': '''2 heads romaine lettuce, chopped
1/2 cup grated parmesan cheese
1 cup croutons
2 tablespoons mayonnaise
2 tablespoons lemon juice
2 cloves garlic, minced
1 teaspoon Worcestershire sauce
1/2 teaspoon Dijon mustard
2 tablespoons olive oil
Salt and pepper to taste''',
                'instructions': '''1. Wash and chop romaine lettuce, then chill.
2. In a bowl, whisk together mayonnaise, lemon juice, garlic, Worcestershire, and mustard.
3. Slowly drizzle in olive oil while whisking.
4. Season with salt and pepper.
5. Toss lettuce with dressing.
6. Top with parmesan cheese and croutons.
7. Serve immediately.''',
                'prep_time': 15,
                'cook_time': 0,
                'servings': 4,
                'difficulty': 'easy',
                'image': 'images/recipes/caesar-salad.jpg'
            },
            {
                'title': 'Rainbow Veggie Stir Fry',
                'slug': 'rainbow-veggie-stir-fry',
                'description': 'Colorful vegetables stir-fried with ginger, garlic, and soy sauce for a healthy meal.',
                'category': vegan_cat,
                'ingredients': '''2 tablespoons vegetable oil
1 bell pepper, sliced
1 carrot, julienned
1 zucchini, sliced
1 cup broccoli florets
1/2 red onion, sliced
2 cloves garlic, minced
1 tablespoon fresh ginger, minced
3 tablespoons soy sauce
1 tablespoon rice vinegar
1 teaspoon sesame oil
Cooked rice for serving''',
                'instructions': '''1. Heat oil in a large wok or skillet over high heat.
2. Add garlic and ginger, stir-fry for 30 seconds.
3. Add harder vegetables (carrot, broccoli) first and stir-fry for 2 minutes.
4. Add remaining vegetables and stir-fry for 3-4 minutes.
5. Mix soy sauce, rice vinegar, and sesame oil.
6. Pour sauce over vegetables and toss.
7. Serve immediately over rice.''',
                'prep_time': 15,
                'cook_time': 8,
                'servings': 3,
                'difficulty': 'easy',
                'image': 'images/recipes/veggie-stir-fry.jpg'
            },
            {
                'title': 'Gourmet Grilled Cheese',
                'slug': 'gourmet-grilled-cheese',
                'description': 'Crispy grilled cheese with artisan bread and premium cheeses, served hot.',
                'category': quick_bite_cat,
                'ingredients': '''4 slices artisan bread
2 tablespoons butter, softened
2 slices aged cheddar
2 slices gruyere cheese
1 tablespoon Dijon mustard
Optional: sliced tomato, caramelized onions''',
                'instructions': '''1. Spread butter on one side of each bread slice.
2. Place bread butter-side down in a cold pan.
3. Spread mustard on top side of bread in pan.
4. Layer cheeses on two slices.
5. Add optional toppings if desired.
6. Top with remaining bread slices, butter-side up.
7. Cook over medium heat until golden brown and cheese melts.
8. Flip and cook until other side is golden.
9. Serve immediately while hot.''',
                'prep_time': 5,
                'cook_time': 8,
                'servings': 2,
                'difficulty': 'easy',
                'image': 'images/recipes/grilled-sandwich.jpg'
            },
            {
                'title': 'Classic Tiramisu',
                'slug': 'classic-tiramisu',
                'description': 'Traditional Italian dessert with coffee-soaked ladyfingers and mascarpone cream.',
                'category': dessert_cat,
                'ingredients': '''6 egg yolks
3/4 cup white sugar
1 1/4 cups mascarpone cheese
1 3/4 cups heavy cream
2 packages ladyfinger cookies
1 cup strong espresso, cooled
3 tablespoons coffee liqueur (optional)
Unsweetened cocoa powder for dusting''',
                'instructions': '''1. Whisk egg yolks and sugar until thick and pale.
2. Add mascarpone and beat until smooth.
3. In separate bowl, whip cream to stiff peaks.
4. Gently fold whipped cream into mascarpone mixture.
5. Combine espresso and coffee liqueur in shallow dish.
6. Quickly dip each ladyfinger in coffee mixture.
7. Arrange in single layer in dish.
8. Spread half the mascarpone mixture over ladyfingers.
9. Repeat layers.
10. Refrigerate at least 4 hours or overnight.
11. Dust with cocoa before serving.''',
                'prep_time': 30,
                'cook_time': 0,
                'servings': 8,
                'difficulty': 'medium',
                'image': 'images/recipes/tiramisu.jpg'
            },
            {
                'title': 'Cinnamon French Toast',
                'slug': 'cinnamon-french-toast',
                'description': 'Golden french toast with cinnamon, vanilla, and maple syrup for a perfect morning treat.',
                'category': breakfast_cat,
                'ingredients': '''8 thick slices bread
4 large eggs
1/2 cup milk
2 tablespoons sugar
1 teaspoon vanilla extract
1/2 teaspoon ground cinnamon
Pinch of salt
Butter for cooking
Maple syrup for serving
Powdered sugar for dusting''',
                'instructions': '''1. In a shallow bowl, whisk together eggs, milk, sugar, vanilla, cinnamon, and salt.
2. Heat butter in a large skillet over medium heat.
3. Dip bread slices in egg mixture, coating both sides.
4. Cook in skillet until golden brown on both sides.
5. Serve hot with maple syrup and dusted with powdered sugar.''',
                'prep_time': 10,
                'cook_time': 12,
                'servings': 4,
                'difficulty': 'easy',
                'image': 'images/recipes/french-toast.jpg'
            },
            {
                'title': 'Glazed Salmon Teriyaki',
                'slug': 'glazed-salmon-teriyaki',
                'description': 'Perfectly grilled salmon with a sweet and savory teriyaki glaze, served with rice.',
                'category': dinner_cat,
                'ingredients': '''4 salmon fillets
1/4 cup soy sauce
2 tablespoons mirin
2 tablespoons brown sugar
1 tablespoon rice vinegar
2 cloves garlic, minced
1 teaspoon fresh ginger, grated
1 tablespoon vegetable oil
Cooked rice for serving
Green onions for garnish
Sesame seeds for garnish''',
                'instructions': '''1. Combine soy sauce, mirin, brown sugar, vinegar, garlic, and ginger for glaze.
2. Heat oil in a large skillet over medium-high heat.
3. Season salmon with salt and pepper.
4. Cook salmon skin-side up for 4 minutes.
5. Flip and cook 3 minutes more.
6. Pour glaze over salmon and cook until thickened.
7. Serve over rice, garnished with green onions and sesame seeds.''',
                'prep_time': 10,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'medium',
                'image': 'images/recipes/salmon-teriyaki.jpg'
            }
        ]
        
        added_count = 0
        for recipe_data in journey_recipes:
            # Add author to each recipe
            recipe_data['author'] = author
            
            # Check if recipe already exists
            if not Recipe.objects.filter(slug=recipe_data['slug']).exists():
                Recipe.objects.create(**recipe_data)
                added_count += 1
                self.stdout.write(f"Added: {recipe_data['title']}")
            else:
                self.stdout.write(f"Skipped (already exists): {recipe_data['title']}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {added_count} new recipes from journey section!')
        )