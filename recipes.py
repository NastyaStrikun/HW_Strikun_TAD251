class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = []
        if ingredients:
            for i in ingredients:
                self.add_ingredient(i)

    def add_ingredient(self, ingredient):
        for i in self.ingredients:
            if i == ingredient:
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(
            Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
        )

    @staticmethod
    def is_valid_ratio(ratio):
        return (isinstance(ratio, int) or isinstance(ratio, float)) and ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэф ratio должен быть положительным числом")
        scaled = [
            Ingredient(i.name, i.quantity * ratio, i.unit) for i in self.ingredients
        ]
        return Recipe(self.title, scaled)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        spisok = "\n".join(str(i) for i in self.ingredients)
        return f"{self.title}:\n{spisok}"


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        for i in recipe.scale(portions).ingredients:
            self._items.append((i, recipe.title))

    def remove_recipe(self, title):
        new_items = []
        for i in self._items:
            if i[1] != title:
                new_items.append(i)
        self._items = new_items

    def get_list(self):
        res = {}
        for i in self._items:
            if (i[0].name, i[0].unit) in res:
                res[(i[0].name, i[0].unit)] += i[0].quantity
            else:
                res[(i[0].name, i[0].unit)] = i[0].quantity
        total = [
            Ingredient(name, quantity, unit) for (name, unit), quantity in res.items()
        ]
        return sorted(total, key=lambda x: x.name)

    def __add__(self, other):
        shop_list = ShoppingList()
        shop_list._items = self._items.copy() + other._items.copy()
        return shop_list


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"
