G_CONVERSIONS = {
    "ug": 1e-6,  # 1 microgram = 0.000001 grams
    "mg": 1e-3,  # 1 milligram = 0.001 grams
    "g": 1,  # 1 gram = 1 gram! :)
    "kg": 1e3,  # 1 kilogram = 1000 grams
    "lb": 453.6  # 1lb = 453.6 grams
}

ML_CONVERSIONS = {
    "ml": 1,
    "cm3": 1,
    "l": 1e3,  # 1L = 1000 ml
    "m3": 1e6,
    "quart": 946.4,
    "tsp": 4.929,
    "tbsp": 14.79,
    "pint": 473.2
}

MASS_UNITS = list(G_CONVERSIONS.keys())
VOL_UNITS = list(ML_CONVERSIONS.keys())
PC_UNITS = ["pc"]
QTY_UNITS = MASS_UNITS + VOL_UNITS + PC_UNITS
