from products.utils import convert_unit


def can_make_recipe(recipe, fridge_products):
    fridge_map = {
        (fp.product_id, fp.unit): fp.quantity
        for fp in fridge_products
    }

    for ingredient in recipe.ingredients.all():
        found = False

        # sprawdzenie czy jest w lodowce
        for(pid, unit), qty in fridge_map.items():
            if pid == ingredient.product_id:
                try:
                    fridge_qty = convert_unit(qty, unit, ingredient.unit)
                except ValueError:
                    continue

                if fridge_qty >= ingredient.quantity:
                    found=True
                    break
                
        if not found:
            return False
        
    return True