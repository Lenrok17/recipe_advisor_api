from decimal import Decimal
from .models import Unit

# Uśrednione wartości (w gramach i mililitrach)
UNIT_CONVERSION = {
    # Kilogramy i gramy
    (Unit.KILOGRAM, Unit.GRAM): 1000,
    (Unit.GRAM, Unit.KILOGRAM): 0.001,

    # Litry i mililitry
    (Unit.LITER, Unit.MILLILITER): 1000,
    (Unit.MILLILITER, Unit.LITER): 0.001,

    # Łyżka stołowa na mililitry
    (Unit.TABLESPOON, Unit.MILLILITER): 15,
    (Unit.MILLILITER, Unit.TABLESPOON): 1/15,

    # Łyżka stołowa na litry
    (Unit.TABLESPOON, Unit.LITER): 0.015,
    (Unit.LITER, Unit.TABLESPOON): 1000/15,

    # Łyżeczka na mililitry
    (Unit.TEASPOON, Unit.MILLILITER): 5,
    (Unit.MILLILITER, Unit.TEASPOON): 1/5,

    # Łyżeczka na litry
    (Unit.TEASPOON, Unit.LITER): 0.005,
    (Unit.LITER, Unit.TEASPOON): 200,

    # Łyżka stołowa na gramy (uśrednione, zależy od produktu, np. woda ~15g)
    (Unit.TABLESPOON, Unit.GRAM): 15,
    (Unit.GRAM, Unit.TABLESPOON): 1/15,

    # Łyżka stołowa na kilogramy
    (Unit.TABLESPOON, Unit.KILOGRAM): 0.015,
    (Unit.KILOGRAM, Unit.TABLESPOON): 1000/15,

    # Łyżeczka na gramy (uśrednione, np. woda ~5g)
    (Unit.TEASPOON, Unit.GRAM): 5,
    (Unit.GRAM, Unit.TEASPOON): 1/5,

    # Łyżeczka na kilogramy
    (Unit.TEASPOON, Unit.KILOGRAM): 0.005,
    (Unit.KILOGRAM, Unit.TEASPOON): 200,

    # Łyżeczka na lyżka
    (Unit.TEASPOON, Unit.TABLESPOON): 1/3,
    (Unit.TABLESPOON, Unit.TEASPOON): 3,
}

def convert_unit(quantity, from_unit, to_unit):
    if from_unit == to_unit:
        return quantity
    factor = UNIT_CONVERSION.get((from_unit, to_unit))
    if factor is None:
        raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")
    return quantity*Decimal(str(factor))