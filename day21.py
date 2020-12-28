import fileinput
import re
from collections import defaultdict, Counter

def find_allergens(foods):
    eliminated_ingredients = set()
    eliminated_lookup = defaultdict(set)

    ingredient_lookup = defaultdict(list)
    for ingredients, allergens in foods:
        for allergen in allergens:
            ingredient_lookup[allergen].append(set(ingredients))

    for allergen, ingredient_lists in ingredient_lookup.items():
        if len(ingredient_lists) > 1:
            ingredient_counter = Counter()
            for ingredient_list in ingredient_lists:
                ingredient_counter.update(ingredient_list)

            # eliminate ingredients that occur in all foods that have the same allergen designation
            ingredient_containing_allergen = set.intersection(*ingredient_lists)
            eliminated_ingredients.update(set.intersection(*ingredient_lists))
            eliminated_lookup[allergen].update(ingredient_containing_allergen)
        else:
            # only one food contains the allergen so any of that foods ingredients could be the allergen
            for ingredient in ingredient_lists[0]:
                eliminated_ingredients.add(ingredient)
                eliminated_lookup[allergen].add(ingredient)

    # part 1
    occurence_count = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient not in eliminated_ingredients:
                occurence_count += 1
    # part 2
    while any(len(t) > 1 for t in eliminated_lookup.values()):
        for allergen1, es1 in eliminated_lookup.items():
            if len(es1) == 1:
                for allergen2, es2 in eliminated_lookup.items():
                    if allergen1 != allergen2:
                        es2 -= es1

    return occurence_count, ",".join([list(ingredient)[0] for _, ingredient in sorted(eliminated_lookup.items())])


food_labels = []
for line in fileinput.input():
    ingredients = [w for w in re.findall(r'(\w+)\s', line) if w != "contains"]
    allergens = re.findall(r'(\w+)[,)]', line)
    food_labels.append((ingredients, allergens))

print(find_allergens(food_labels))


