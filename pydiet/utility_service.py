def convert_mass(mass, start_units, end_units):
    # Define conversions
    g_conversions = {
        "ug": 1e-6,  # 1 microgram = 0.000001 grams
        "mg": 1e-3,  # 1 milligram = 0.001 grams
        "g": 1,  # 1 gram = 1 gram! :)
        "kg": 1e3,  # 1 kilogram = 1000 grams
    }
    # Convert value to grams first
    mass_in_g = g_conversions[start_units]*mass
    return mass_in_g/g_conversions[end_units]
