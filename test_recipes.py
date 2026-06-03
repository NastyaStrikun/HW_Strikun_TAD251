import pytest
from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList


def test_creation_ing():
    ingredient = Ingredient("Мука", 500, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == float(500)
    assert ingredient.unit == "г"


def test_str_ing():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"


def test_eq_ing():
    assert Ingredient("Мука", 500, "г") == Ingredient("Мука", 100, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Крахмал", 500, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Мука", 500, "кг")


def test_creation_rec():
    ingredient = Ingredient("Мука", 500, "г")
    recipe = Recipe("Тесто", [ingredient])
    assert recipe.title == "Тесто"
    assert recipe.ingredients == [ingredient]


def test_add_rec():
    recipe = Recipe("Хлеб", [])
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 100, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 600.0


def test_scale_rec():
    recipe = Recipe("Хлеб", [Ingredient("Мука", 500, "г")])
    scaled = recipe.scale(10)
    assert scaled is not recipe
    assert scaled.ingredients[0].quantity == 5000.0
    assert recipe.ingredients[0].quantity == 500.0
    with pytest.raises(ValueError):
        recipe.scale(0)


def test_len_rec():
    recipe = Recipe(
        "Хлеб",
        [
            Ingredient("Мука", 500, "г"),
            Ingredient("Мука", 500, "г"),
            Ingredient("Вода", 500, "г"),
        ],
    )
    assert len(recipe) == 2


def test_add_rec_shopping():
    recipe = Recipe(
        "Хлеб", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 500, "г")]
    )
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe, 10)
    res = shop_list.get_list()
    assert len(res) == 2
    assert res[1].name == "Мука"
    assert res[1].quantity == 5000.0
    assert res[1].unit == "г"
    assert res[0].name == "Вода"
    assert res[0].quantity == 5000.0
    assert res[0].unit == "г"

    with pytest.raises(ValueError):
        shop_list.add_recipe(recipe, 0)


def test_remove_shopping():
    recipe = Recipe(
        "Хлеб", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 500, "г")]
    )
    wrecipe = Recipe(
        "Тесто", [Ingredient("Мука", 500, "г"), Ingredient("Яйцо", 2, "шт")]
    )
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe, 1)
    shop_list.add_recipe(wrecipe, 1)
    shop_list.remove_recipe("Хлеб")
    shop_list.remove_recipe("Пицца")
    res = shop_list.get_list()

    assert len(res) == 2
    assert res[0].name == "Мука"
    assert res[0].quantity == 500.0
    assert res[0].unit == "г"
    assert res[1].name == "Яйцо"
    assert res[1].quantity == 2.0
    assert res[1].unit == "шт"


def test_get_shopping():
    recipe = Recipe(
        "Хлеб", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 500, "г")]
    )
    wrecipe = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe, 1)
    shop_list.add_recipe(wrecipe, 1)
    res = shop_list.get_list()
    assert [i.name for i in res] == ["Вода", "Мука"]
    assert res[1].quantity == 1000.0


def test_add_shopping():
    recipe = Recipe(
        "Хлеб", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 500, "г")]
    )
    wrecipe = Recipe(
        "Тесто", [Ingredient("Мука", 500, "г"), Ingredient("Яйцо", 2, "шт")]
    )
    one = ShoppingList()
    other = ShoppingList()
    one.add_recipe(recipe, 1)
    other.add_recipe(wrecipe, 1)
    joined = one + other
    assert len(joined.get_list()) == 3
    assert len(one.get_list()) == 2
    assert len(other.get_list()) == 2
