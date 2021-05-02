from typing import Optional

import model


class HasFlagsTestable(model.flags.HasFlags):
    def __init__(self, flag_dofs: Optional['model.flags.FlagDOFData'] = None):
        self.flag_dofs = flag_dofs

    @property
    def _flag_dofs(self) -> 'FlagDOFData':
        return self.flag_dofs