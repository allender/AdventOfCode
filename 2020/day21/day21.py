import re
from collections import defaultdict
from collections import Counter

test_data="""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    allergens = defaultdict(list)
    ingredients_set = set()
    ingredients_list = [ ]

    data = input_data.split('\n')

    for l in data:
        mo = re.match( r'(.*) \(contains (.*)\)', l)
        ingredients = mo.group(1).split(' ')
        ingredients_list.extend(ingredients)
        ingredients_set = ingredients_set.union( set(ingredients) )
        for allergen in mo.group(2).split(', '):
            allergens[allergen] = [ i for i in ingredients if i in allergens[allergen] or len(allergens[allergen]) == 0 ]

    # iterate through allergens and we just find which ingredient is which
    # allergen
    while True:
        single_allergens = [ i[0] for i in allergens.values() if len(i) == 1 ]
        if len(single_allergens) == len(allergens):
            break
        for allergen, ingredients in allergens.items():
            for i in single_allergens:
                if i in ingredients and len(ingredients) > 1:
                    ingredients.remove(i)

    allergic_incredients = [ a[0] for a in allergens.values() ]
    safe_ingredients = [ i for i in ingredients_set if i not in allergic_incredients ]
    print(sum([ingredients_list.count(i) for i in safe_ingredients]) )

    allergic_ingredients = [ list(allergens[i])[0] for i in sorted(allergens) ]
    print(','.join(allergic_ingredients))
    