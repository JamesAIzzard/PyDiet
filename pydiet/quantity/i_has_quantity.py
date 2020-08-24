import abc


class IHasQuantity(abc.ABC):

    @abc.abstractproperty
    def density_g_per_ml(self) -> float:
        raise NotImplementedError

