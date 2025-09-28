from django.core.management.base import BaseCommand
from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Add sample recipes for categories that have no recipes'
    
    def handle(self, *args, **options):
        # Get the chef_zestora user as author
        try:
            author = User.objects.get(username='chef_zestora')
        except User.DoesNotExist:
            # Fallback to any available user
            author = User.objects.first()
            if not author:
                self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
                return

        # Get categories that need recipes
        empty_categories = [cat for cat in Category.objects.all() if Recipe.objects.filter(category=cat).count() == 0]
        
        # Define recipes for each empty category
        category_recipes = {
            'quick-easy': [
                {
                    'title': '15-Minute Garlic Butter Shrimp',
                    'slug': '15-minute-garlic-butter-shrimp',
                    'description': 'Quick and flavorful shrimp cooked in garlic butter, perfect for busy weeknights.',
                    'ingredients': '''1 lb large shrimp, peeled and deveined
4 cloves garlic, minced
3 tablespoons butter
2 tablespoons olive oil
1/4 cup white wine (optional)
2 tablespoons lemon juice
Salt and pepper to taste
Fresh parsley for garnish
Cooked rice or pasta for serving''',
                    'instructions': '''1. Heat olive oil and butter in a large skillet over medium-high heat.
2. Add garlic and cook for 30 seconds until fragrant.
3. Add shrimp and season with salt and pepper.
4. Cook shrimp for 2-3 minutes per side until pink.
5. Add white wine and lemon juice, cook for 1 minute.
6. Garnish with fresh parsley and serve over rice or pasta.''',
                    'prep_time': 5,
                    'cook_time': 10,
                    'servings': 4,
                    'difficulty': 'easy',
                    'image': 'images/recipes/garlic-butter-shrimp.jpg'
                },
                {
                    'title': 'Quick Chicken Stir Fry',
                    'slug': 'quick-chicken-stir-fry',
                    'description': 'Fast and healthy chicken stir fry with crisp vegetables and savory sauce.',
                    'ingredients': '''1 lb boneless chicken breast, sliced thin
2 cups mixed vegetables (broccoli, bell peppers, snap peas)
2 tablespoons vegetable oil
3 cloves garlic, minced
1 tablespoon ginger, minced
3 tablespoons soy sauce
1 tablespoon oyster sauce
1 teaspoon cornstarch
Cooked rice for serving''',
                    'instructions': '''1. Heat oil in a large wok or skillet over high heat.
2. Add chicken and cook until no longer pink, about 5 minutes.
3. Add garlic and ginger, cook for 30 seconds.
4. Add vegetables and stir-fry for 3-4 minutes.
5. Mix soy sauce, oyster sauce, and cornstarch, add to pan.
6. Stir for 1 minute until sauce thickens.
7. Serve immediately over rice.''',
                    'prep_time': 10,
                    'cook_time': 10,
                    'servings': 4,
                    'difficulty': 'easy',
                    'image': 'images/recipes/quick-chicken-stir-fry.jpg'
                },
                {
                    'title': 'Microwave Mug Mac and Cheese',
                    'slug': 'microwave-mug-mac-cheese',
                    'description': 'Single-serving mac and cheese ready in just 2 minutes using your microwave.',
                    'ingredients': '''1/3 cup elbow macaroni
1/3 cup water
2 tablespoons milk
1/4 cup shredded cheddar cheese
Salt and pepper to taste
Optional: breadcrumbs for topping''',
                    'instructions': '''1. Add macaroni and water to a microwave-safe mug.
2. Microwave for 2 minutes, stir, then microwave 1 more minute.
3. Stir in milk and cheese until melted and creamy.
4. Season with salt and pepper.
5. Top with breadcrumbs if desired.
6. Serve immediately while hot.''',
                    'prep_time': 1,
                    'cook_time': 3,
                    'servings': 1,
                    'difficulty': 'easy',
                    'image': 'images/recipes/mug-mac-cheese.jpg'
                }
            ],
            'healthy': [
                {
                    'title': 'Quinoa Power Bowl',
                    'slug': 'quinoa-power-bowl',
                    'description': 'Nutritious bowl packed with quinoa, fresh vegetables, and protein-rich chickpeas.',
                    'ingredients': '''1 cup quinoa, cooked
1 can chickpeas, drained and roasted
2 cups mixed greens
1 avocado, sliced
1 cup cherry tomatoes, halved
1/2 cucumber, diced
1/4 cup pumpkin seeds
3 tablespoons tahini
2 tablespoons lemon juice
1 tablespoon olive oil
Salt and pepper to taste''',
                    'instructions': '''1. Cook quinoa according to package directions and let cool.
2. Roast chickpeas in oven at 400°F for 20 minutes.
3. Prepare vegetables and arrange in bowls.
4. Mix tahini, lemon juice, olive oil, salt, and pepper for dressing.
5. Layer quinoa, greens, vegetables, and chickpeas in bowls.
6. Drizzle with dressing and sprinkle with pumpkin seeds.''',
                    'prep_time': 15,
                    'cook_time': 25,
                    'servings': 4,
                    'difficulty': 'easy',
                    'image': 'images/recipes/quinoa-power-bowl.jpg'
                },
                {
                    'title': 'Green Smoothie Bowl',
                    'slug': 'green-smoothie-bowl',
                    'description': 'Refreshing and nutritious smoothie bowl loaded with vitamins and antioxidants.',
                    'ingredients': '''1 frozen banana
1 cup fresh spinach
1/2 avocado
1/2 cup mango chunks
1/2 cup coconut milk
1 tablespoon chia seeds
Toppings: granola, berries, coconut flakes, nuts''',
                    'instructions': '''1. Blend banana, spinach, avocado, mango, and coconut milk until smooth.
2. Pour into a bowl and smooth the top.
3. Sprinkle with chia seeds.
4. Arrange toppings in colorful sections.
5. Serve immediately with a spoon.''',
                    'prep_time': 10,
                    'cook_time': 0,
                    'servings': 2,
                    'difficulty': 'easy',
                    'image': 'images/recipes/green-smoothie-bowl.jpg'
                },
                {
                    'title': 'Baked Lemon Herb Salmon',
                    'slug': 'baked-lemon-herb-salmon',
                    'description': 'Heart-healthy salmon baked with fresh herbs and bright lemon flavors.',
                    'ingredients': '''4 salmon fillets
2 lemons, sliced
2 tablespoons olive oil
2 tablespoons fresh dill
1 tablespoon fresh parsley
2 cloves garlic, minced
Salt and pepper to taste
Steamed vegetables for serving''',
                    'instructions': '''1. Preheat oven to 400°F.
2. Place salmon on parchment-lined baking sheet.
3. Mix olive oil, herbs, garlic, salt, and pepper.
4. Brush mixture over salmon fillets.
5. Top with lemon slices.
6. Bake for 12-15 minutes until fish flakes easily.
7. Serve with steamed vegetables.''',
                    'prep_time': 10,
                    'cook_time': 15,
                    'servings': 4,
                    'difficulty': 'easy',
                    'image': 'images/recipes/baked-lemon-herb-salmon.jpg'
                }
            ],
            'comfort-food': [
                {
                    'title': 'Classic Chicken Pot Pie',
                    'slug': 'classic-chicken-pot-pie',
                    'description': 'Traditional comfort food with tender chicken and vegetables in a creamy sauce, topped with flaky pastry.',
                    'ingredients': '''2 cups cooked chicken, diced
1 cup mixed vegetables (carrots, peas, celery)
1/4 cup butter
1/4 cup all-purpose flour
2 cups chicken broth
1/2 cup milk
Salt and pepper to taste
2 pie crusts (store-bought or homemade)
1 egg, beaten for wash''',
                    'instructions': '''1. Preheat oven to 425°F.
2. Melt butter in a large pot, whisk in flour to make roux.
3. Gradually add broth and milk, stirring until thickened.
4. Add chicken and vegetables, season with salt and pepper.
5. Pour filling into pie dish, cover with top crust.
6. Brush with beaten egg and cut vents.
7. Bake for 30-35 minutes until golden brown.''',
                    'prep_time': 20,
                    'cook_time': 35,
                    'servings': 6,
                    'difficulty': 'medium',
                    'image': 'images/recipes/chicken-pot-pie.jpg'
                },
                {
                    'title': 'Loaded Baked Potato Soup',
                    'slug': 'loaded-baked-potato-soup',
                    'description': 'Creamy, hearty soup that tastes like a loaded baked potato in a bowl.',
                    'ingredients': '''6 large russet potatoes, baked and diced
6 slices bacon, cooked and crumbled
1/4 cup butter
1/4 cup flour
4 cups milk
1 cup sour cream
1 cup shredded cheddar cheese
3 green onions, chopped
Salt and pepper to taste''',
                    'instructions': '''1. Bake potatoes until tender, let cool and dice.
2. Cook bacon until crispy, crumble and set aside.
3. In large pot, melt butter and whisk in flour.
4. Gradually add milk, stirring until smooth.
5. Add diced potatoes and simmer for 10 minutes.
6. Stir in sour cream and cheese until melted.
7. Top with bacon and green onions.''',
                    'prep_time': 15,
                    'cook_time': 45,
                    'servings': 6,
                    'difficulty': 'medium',
                    'image': 'images/recipes/loaded-potato-soup.jpg'
                },
                {
                    'title': 'Homemade Meatloaf',
                    'slug': 'homemade-meatloaf',
                    'description': 'Classic American comfort food - juicy meatloaf with a tangy glaze.',
                    'ingredients': '''2 lbs ground beef
1 cup breadcrumbs
1 onion, finely diced
2 eggs, beaten
1/4 cup milk
2 tablespoons Worcestershire sauce
Salt and pepper to taste
1/2 cup ketchup
2 tablespoons brown sugar
1 tablespoon mustard''',
                    'instructions': '''1. Preheat oven to 350°F.
2. Mix ground beef, breadcrumbs, onion, eggs, milk, and seasonings.
3. Shape into a loaf and place in baking dish.
4. Mix ketchup, brown sugar, and mustard for glaze.
5. Brush half the glaze over meatloaf.
6. Bake for 45 minutes, brush with remaining glaze.
7. Bake 15 more minutes until internal temp reaches 160°F.''',
                    'prep_time': 15,
                    'cook_time': 60,
                    'servings': 8,
                    'difficulty': 'easy',
                    'image': 'images/recipes/homemade-meatloaf.jpg'
                }
            ],
            'international': [
                {
                    'title': 'Authentic Pad Thai',
                    'slug': 'authentic-pad-thai',
                    'description': 'Traditional Thai stir-fried noodles with sweet, sour, and savory flavors.',
                    'ingredients': '''8 oz rice noodles
2 tablespoons tamarind paste
3 tablespoons fish sauce
2 tablespoons palm sugar
2 tablespoons vegetable oil
2 eggs, beaten
1/2 cup firm tofu, cubed
2 cloves garlic, minced
Bean sprouts, peanuts, lime wedges
Green onions for garnish''',
                    'instructions': '''1. Soak rice noodles in warm water until soft.
2. Mix tamarind paste, fish sauce, and palm sugar for sauce.
3. Heat oil in wok, scramble eggs and set aside.
4. Stir-fry garlic and tofu until golden.
5. Add drained noodles and sauce, toss to combine.
6. Add eggs back in with bean sprouts.
7. Serve with peanuts, lime, and green onions.''',
                    'prep_time': 20,
                    'cook_time': 15,
                    'servings': 4,
                    'difficulty': 'medium',
                    'image': 'images/recipes/authentic-pad-thai.jpg'
                },
                {
                    'title': 'Italian Osso Buco',
                    'slug': 'italian-osso-buco',
                    'description': 'Classic Milanese braised veal shanks in white wine and vegetables.',
                    'ingredients': '''4 veal shanks, cross-cut
1/2 cup flour for dredging
3 tablespoons olive oil
1 onion, diced
2 carrots, diced
2 celery stalks, diced
1 cup white wine
2 cups beef broth
1 can diced tomatoes
Fresh herbs (thyme, rosemary)
Gremolata for serving''',
                    'instructions': '''1. Dredge veal shanks in flour and brown in olive oil.
2. Remove shanks and sauté vegetables until soft.
3. Add wine and scrape up browned bits.
4. Return shanks to pot with broth, tomatoes, and herbs.
5. Cover and braise in 325°F oven for 2 hours.
6. Serve with gremolata and risotto.''',
                    'prep_time': 20,
                    'cook_time': 120,
                    'servings': 4,
                    'difficulty': 'hard',
                    'image': 'images/recipes/italian-osso-buco.jpg'
                },
                {
                    'title': 'Mexican Street Tacos',
                    'slug': 'mexican-street-tacos',
                    'description': 'Authentic street-style tacos with seasoned meat and fresh toppings.',
                    'ingredients': '''1 lb skirt steak, thinly sliced
12 corn tortillas
1 white onion, finely diced
1/2 cup fresh cilantro, chopped
2 limes, cut into wedges
Salsa verde
Mexican crema
2 tablespoons cumin
1 tablespoon chili powder
Salt and pepper to taste''',
                    'instructions': '''1. Season steak with cumin, chili powder, salt, and pepper.
2. Heat skillet over high heat and cook steak 2-3 minutes per side.
3. Warm tortillas on griddle until lightly charred.
4. Slice steak against the grain.
5. Fill tortillas with meat, onion, and cilantro.
6. Serve with lime wedges, salsa, and crema.''',
                    'prep_time': 15,
                    'cook_time': 10,
                    'servings': 4,
                    'difficulty': 'easy',
                    'image': 'images/recipes/mexican-street-tacos.jpg'
                }
            ],
            'holiday': [
                {
                    'title': 'Traditional Roast Turkey',
                    'slug': 'traditional-roast-turkey',
                    'description': 'Perfect holiday centerpiece - golden, juicy roast turkey with herb butter.',
                    'ingredients': '''12-14 lb whole turkey
1/2 cup butter, softened
2 tablespoons fresh sage, chopped
2 tablespoons fresh thyme
1 tablespoon fresh rosemary
2 lemons, quartered
1 onion, quartered
4 celery stalks
Salt and pepper to taste
Turkey stock for gravy''',
                    'instructions': '''1. Preheat oven to 325°F.
2. Remove giblets and pat turkey dry.
3. Mix butter with herbs, salt, and pepper.
4. Loosen skin and spread herb butter under skin.
5. Stuff cavity with lemon, onion, and celery.
6. Roast 3-4 hours until internal temp reaches 165°F.
7. Let rest 20 minutes before carving.''',
                    'prep_time': 30,
                    'cook_time': 240,
                    'servings': 12,
                    'difficulty': 'hard',
                    'image': 'images/recipes/traditional-roast-turkey.jpg'
                },
                {
                    'title': 'Gingerbread Cookies',
                    'slug': 'gingerbread-cookies',
                    'description': 'Classic holiday cookies perfect for decorating and gift-giving.',
                    'ingredients': '''3 cups all-purpose flour
2 teaspoons ground ginger
1 teaspoon cinnamon
1/2 teaspoon nutmeg
1/2 teaspoon cloves
1 teaspoon baking soda
1/2 cup butter, softened
1/2 cup brown sugar
1/2 cup molasses
1 egg
Royal icing for decorating''',
                    'instructions': '''1. Mix flour, spices, and baking soda in a bowl.
2. Cream butter and brown sugar until fluffy.
3. Beat in molasses and egg.
4. Gradually mix in dry ingredients.
5. Wrap dough and chill for 2 hours.
6. Roll out and cut with cookie cutters.
7. Bake at 350°F for 8-10 minutes.
8. Cool completely before decorating.''',
                    'prep_time': 30,
                    'cook_time': 10,
                    'servings': 24,
                    'difficulty': 'medium',
                    'image': 'images/recipes/gingerbread-cookies.jpg'
                },
                {
                    'title': 'Cranberry Orange Bread',
                    'slug': 'cranberry-orange-bread',
                    'description': 'Festive quick bread bursting with tart cranberries and bright orange flavor.',
                    'ingredients': '''2 cups all-purpose flour
3/4 cup sugar
1 1/2 teaspoons baking powder
1/2 teaspoon salt
1/4 cup butter, melted
1 egg, beaten
3/4 cup orange juice
Zest of 1 orange
1 cup fresh cranberries
1/2 cup chopped walnuts''',
                    'instructions': '''1. Preheat oven to 350°F and grease a loaf pan.
2. Mix flour, sugar, baking powder, and salt.
3. Combine butter, egg, orange juice, and zest.
4. Add wet ingredients to dry, stir until just combined.
5. Fold in cranberries and walnuts.
6. Pour into prepared pan.
7. Bake 55-60 minutes until toothpick comes out clean.
8. Cool in pan 10 minutes before removing.''',
                    'prep_time': 15,
                    'cook_time': 60,
                    'servings': 10,
                    'difficulty': 'easy',
                    'image': 'images/recipes/cranberry-orange-bread.jpg'
                }
            ]
        }
        
        added_count = 0
        for category in empty_categories:
            if category.slug in category_recipes:
                self.stdout.write(f'\nAdding recipes for {category.name}:')
                for recipe_data in category_recipes[category.slug]:
                    # Add author and category to recipe data
                    recipe_data['author'] = author
                    recipe_data['category'] = category
                    
                    # Check if recipe already exists
                    if not Recipe.objects.filter(slug=recipe_data['slug']).exists():
                        Recipe.objects.create(**recipe_data)
                        added_count += 1
                        self.stdout.write(f"  ✓ Added: {recipe_data['title']}")
                    else:
                        self.stdout.write(f"  - Skipped (already exists): {recipe_data['title']}")
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully added {added_count} new recipes across {len(empty_categories)} categories!')
        )
        
        # Provide image upload instructions
        self.stdout.write(
            self.style.WARNING(f'\nImage Upload Instructions:')
        )
        self.stdout.write('Please upload the following images to static/images/recipes/:')
        
        for category in empty_categories:
            if category.slug in category_recipes:
                self.stdout.write(f'\n{category.name} category:')
                for recipe_data in category_recipes[category.slug]:
                    self.stdout.write(f"  - {recipe_data['image']}")