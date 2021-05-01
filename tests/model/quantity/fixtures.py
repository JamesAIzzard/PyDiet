import model


def get_has_bulk_with_09_density() -> 'model.quantity.HasBulk':
    return model.quantity.HasBulk(model.quantity.BulkData(
        ref_qty=100,
        pref_unit='g',
        g_per_ml=0.9,
        piece_mass_g=None
    ))


def get_has_bulk_with_30_pc_mass() -> 'model.quantity.HasBulk':
    return model.quantity.HasBulk(model.quantity.BulkData(
        ref_qty=100,
        pref_unit='g',
        g_per_ml=None,
        piece_mass_g=30
    ))


def get_undefined_has_quantity() -> 'model.quantity.HasQuantityOf':
    return model.quantity.HasQuantityOf(
        subject=model.quantity.HasBulk(),
        get_quantity_in_g=lambda: None,
        get_quantity_pref_unit=lambda: 'g'
    )


def get_has_3kg() -> 'model.quantity.HasQuantityOf':
    return model.quantity.HasQuantityOf(
        subject=model.quantity.HasBulk(),
        get_quantity_in_g=lambda: 3000,
        get_quantity_pref_unit=lambda: 'kg'
    )


def get_undefined_has_settable_quantity() -> 'model.quantity.HasSettableQuantityOf':
    return model.quantity.HasSettableQuantityOf(subject=model.quantity.HasBulk())
